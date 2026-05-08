"""VCReady — Founder Logic Pressure-Test Engine.

A Streamlit prototype that simulates a sharp early-stage VC and produces
a Founder Reflection Report. Built for portfolio purposes, not commercial use.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompts import QUESTION_PROMPT, REPORT_PROMPT

load_dotenv(override=True)


# ---------- API client ----------

def get_client() -> OpenAI:
    """Build an OpenAI-compatible client. base_url is optional for relay endpoints."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your .env file.")
    return OpenAI(api_key=api_key, base_url=base_url)


def _looks_like_html(s: str) -> bool:
    head = s.lstrip().lower()[:200]
    return head.startswith("<!doctype html") or head.startswith("<html")


def call_model(prompt: str) -> str:
    """Send a single-turn prompt and return the raw assistant text."""
    model = os.getenv("OPENAI_MODEL", "").strip()
    if not model:
        raise RuntimeError("OPENAI_MODEL is missing. Set it in your .env file.")
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    # Some relay endpoints return a plain string instead of a ChatCompletion object.
    if isinstance(response, str):
        text = response
    else:
        text = response.choices[0].message.content or ""
    if _looks_like_html(text):
        raise RuntimeError(
            "Your OPENAI_BASE_URL points to a web page, not an API endpoint. "
            "Use the OpenAI-compatible API base URL, usually ending with /v1."
        )
    return text.strip()


# ---------- Session state ----------

def init_state() -> None:
    st.session_state.setdefault("questions_markdown", "")
    st.session_state.setdefault("answers_text", "")
    st.session_state.setdefault("report_markdown", "")
    st.session_state.setdefault("founder_background", "")
    st.session_state.setdefault("project_description", "")
    st.session_state.setdefault("current_evidence", "")
    st.session_state.setdefault("funding_goal", "")


# ---------- UI ----------

st.set_page_config(page_title="VCReady", layout="wide")
init_state()

st.title("VCReady")
st.caption("Founder Logic Pressure-Test Engine")
st.write(
    "VCReady helps early-stage founders pressure-test their founder narrative "
    "before talking to investors. Fill in your context on the left, let the AI "
    "VC grill you with 7 questions, then get a Founder Reflection Report."
)

with st.expander("How it works", expanded=False):
    st.markdown(
        "1. Enter your founder background, project, current evidence, and funding goal.\n"
        "2. Click **Generate Pressure-Test Questions** to receive 7 VC-style questions.\n"
        "3. Write your honest answers in one answer box, referencing each question by number.\n"
        "4. Click **Generate Founder Reflection Report** for a diagnostic with scores and advice.\n"
        "5. Download the report as a `.txt` file."
    )
# ---------- Sidebar: founder inputs ----------

with st.sidebar:
    st.header("Founder Context")
    st.session_state.founder_background = st.text_area(
        "Founder background",
        value=st.session_state.founder_background,
        height=120,
        placeholder="Your experience, domain expertise, prior roles, why you are the person to solve this.",
    )
    st.session_state.project_description = st.text_area(
        "Project description",
        value=st.session_state.project_description,
        height=120,
        placeholder="What you are building, for whom, and the core value proposition.",
    )
    st.session_state.current_evidence = st.text_area(
        "Current evidence",
        value=st.session_state.current_evidence,
        height=120,
        placeholder="Traction, pilots, LOIs, interviews, prototypes, data — anything concrete.",
    )
    st.session_state.funding_goal = st.text_area(
        "Funding or partnership goal",
        value=st.session_state.funding_goal,
        height=100,
        placeholder="What you want from this investor or partner meeting.",
    )
    generate_questions_clicked = st.button(
        "Generate Pressure-Test Questions", type="primary", use_container_width=True
    )


# ---------- Step 1: generate questions ----------

def inputs_ready() -> bool:
    return all(
        st.session_state[k].strip()
        for k in ("founder_background", "project_description", "current_evidence", "funding_goal")
    )


if generate_questions_clicked:
    if not inputs_ready():
        st.warning("Please fill in all four founder context fields first.")
    else:
        with st.spinner("The AI VC is preparing pressure-test questions..."):
            try:
                prompt = QUESTION_PROMPT.format(
                    founder_background=st.session_state.founder_background,
                    project_description=st.session_state.project_description,
                    current_evidence=st.session_state.current_evidence,
                    funding_goal=st.session_state.funding_goal,
                )
                raw = call_model(prompt)
                st.session_state.questions_markdown = raw
                st.session_state.answers_text = ""
                st.session_state.report_markdown = ""
                st.session_state.pop("answers_textarea", None)
            except Exception as e:
                st.error(f"Failed to generate questions: {e}")
# ---------- Step 2: display questions, collect answers ----------

if st.session_state.questions_markdown:
    st.subheader("Pressure-Test Questions")
    st.caption("Answer all 7 questions below in one box. Reference each question by number. Vague answers produce vague diagnostics.")
    st.markdown(st.session_state.questions_markdown)

    st.session_state.answers_text = st.text_area(
        "Your answers",
        value=st.session_state.answers_text,
        key="answers_textarea",
        height=320,
        placeholder="1. ...\n2. ...\n3. ...\n4. ...\n5. ...\n6. ...\n7. ...",
    )

    generate_report_clicked = st.button(
        "Generate Founder Reflection Report", type="primary"
    )

    if generate_report_clicked:
        if not st.session_state.answers_text.strip():
            st.warning("Please write your answers before generating the report.")
        else:
            with st.spinner("The AI VC is writing your Founder Reflection Report..."):
                try:
                    qa_transcript = (
                        "Questions:\n"
                        f"{st.session_state.questions_markdown}\n\n"
                        "Founder's answers:\n"
                        f"{st.session_state.answers_text}"
                    )
                    prompt = REPORT_PROMPT.format(
                        founder_background=st.session_state.founder_background,
                        project_description=st.session_state.project_description,
                        current_evidence=st.session_state.current_evidence,
                        funding_goal=st.session_state.funding_goal,
                        qa_transcript=qa_transcript,
                    )
                    st.session_state.report_markdown = call_model(prompt)
                except Exception as e:
                    st.error(f"Failed to generate report: {e}")
# ---------- Step 3: render report + download ----------

if st.session_state.report_markdown:
    st.subheader("Founder Reflection Report")
    st.markdown(st.session_state.report_markdown)

    st.download_button(
        label="Download Report (.txt)",
        data=st.session_state.report_markdown,
        file_name="vcready_founder_reflection_report.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "VCReady is a working prototype built for the HKUST-GZ Red Bird MPhil application portfolio. "
    "It is not a commercial product, has no users, no funding, and is not deployed to production."
)

