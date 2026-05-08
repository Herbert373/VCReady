"""VCReady - Founder Logic Pressure-Test Engine.

A Streamlit prototype that simulates a sharp early-stage VC and produces
a Founder Reflection Report. Built for portfolio purposes, not commercial use.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompts import QUESTION_PROMPT, REPORT_PROMPT_EN, REPORT_PROMPT_ZH

load_dotenv(override=True)


# ---------- UI text (both languages) ----------

TEXTS = {
    "en": {
        "subtitle": "Founder Logic Pressure-Test Engine",
        "assessment_title": "Assessment Framework",
        "assessment_items": [
            "Founder-Market Fit",
            "Problem Urgency",
            "Execution Evidence",
            "Resilience",
            "Unfair Advantage",
        ],
        "workflow_title": "Workflow",
        "workflow_steps": [
            "Build Founder Dossier",
            "Generate VC Pressure-Test Questions",
            "Answer Under Investor Logic",
            "Produce Founder Reflection Report",
        ],
        "description": (
            "VCReady helps early-stage founders pressure-test their founder narrative "
            "before talking to investors. Fill in your context on the left, let the AI "
            "VC grill you with 7 questions, then get a Founder Reflection Report."
        ),
        "how_it_works_title": "How it works",
        "how_it_works_body": (
            "1. Enter your founder background, project, current evidence, and funding goal.\n"
            "2. Click **Generate Pressure-Test Questions** to receive 7 VC-style questions.\n"
            "3. Write your honest answers in one answer box, referencing each question by number.\n"
            "4. Click **Generate Founder Reflection Report** for a diagnostic with scores and advice.\n"
            "5. Download the report as a `.txt` file."
        ),
        "sidebar_header": "Founder Context",
        "founder_bg_label": "Founder background",
        "founder_bg_placeholder": "Your experience, domain expertise, prior roles, why you are the person to solve this.",
        "project_desc_label": "Project description",
        "project_desc_placeholder": "What you are building, for whom, and the core value proposition.",
        "evidence_label": "Current evidence",
        "evidence_placeholder": "Traction, pilots, LOIs, interviews, prototypes, data - anything concrete.",
        "goal_label": "Funding or partnership goal",
        "goal_placeholder": "What you want from this investor or partner meeting.",
        "btn_questions": "Generate Pressure-Test Questions",
        "warn_fill_fields": "Please fill in all four founder context fields first.",
        "spinner_questions": "The AI VC is preparing pressure-test questions...",
        "err_questions": "Failed to generate questions: ",
        "questions_subheader": "Pressure-Test Questions",
        "answers_caption": "Answer all 7 questions below in one box. Reference each question by number. Vague answers produce vague diagnostics.",
        "answers_label": "Your answers",
        "answers_placeholder": "1. ...\n2. ...\n3. ...\n4. ...\n5. ...\n6. ...\n7. ...",
        "btn_report": "Generate Founder Reflection Report",
        "warn_write_answers": "Please write your answers before generating the report.",
        "spinner_report": "The AI VC is writing your Founder Reflection Report...",
        "err_report": "Failed to generate report: ",
        "report_subheader": "Founder Reflection Report",
        "btn_download": "Download Report (.txt)",
        "footer": (
            "VCReady is a working prototype built for the HKUST-GZ Red Bird MPhil application portfolio. "
            "It is not a commercial product, has no users, no funding, and is not deployed to production."
        ),
        "language_instruction": "Please answer in English.",
    },
    "zh": {
        "subtitle": "创始人逻辑压力测试引擎",
        "description": (
            "VCReady 帮助早期创始人在见投资人之前压力测试自己的创始人叙事。"
            "在左侧填写你的背景信息，让 AI VC 用 7 个问题追问你，然后获得一份创始人反思报告。"
        ),
        "how_it_works_title": "使用流程",
        "how_it_works_body": (
            "1. 输入你的创始人背景、项目简介、现有验证证据和融资或合作目标。\n"
            "2. 点击「生成压力测试问题」获得 7 个 VC 风格的追问。\n"
            "3. 在答题框中如实作答，按编号对应。\n"
            "4. 点击「生成创始人反思报告」拿到诊断与建议。\n"
            "5. 下载 .txt 报告。"
        ),
        "sidebar_header": "创始人背景",
        "founder_bg_label": "创始人背景",
        "founder_bg_placeholder": "你的经历、领域专长、过往角色，以及为什么是你来解决这个问题。",
        "project_desc_label": "项目简介",
        "project_desc_placeholder": "你在做什么、面向谁、核心价值主张是什么。",
        "evidence_label": "现有验证证据",
        "evidence_placeholder": "进展、试点、意向书、访谈、原型、数据--任何可落地的证据。",
        "goal_label": "融资或合作目标",
        "goal_placeholder": "你希望从这次投资人或合作方会议中拿到什么。",
        "btn_questions": "生成压力测试问题",
        "warn_fill_fields": "请先填写左侧四个创始人背景字段。",
        "spinner_questions": "AI VC 正在准备压力测试问题……",
        "err_questions": "生成问题失败：",
        "questions_subheader": "压力测试问题",
        "answers_caption": "请在下方一个答题框中回答全部 7 个问题，按编号对应。回答越含糊，诊断越含糊。",
        "answers_label": "你的回答",
        "answers_placeholder": "1. ……\n2. ……\n3. ……\n4. ……\n5. ……\n6. ……\n7. ……",
        "btn_report": "生成创始人反思报告",
        "warn_write_answers": "请先写完回答再生成报告。",
        "spinner_report": "AI VC 正在撰写你的创始人反思报告……",
        "err_report": "生成报告失败：",
        "report_subheader": "创始人反思报告",
        "btn_download": "下载报告 (.txt)",
        "footer": (
            "VCReady 是为香港科技大学（广州）红鸟 MPhil 申请作品集构建的可运行原型。"
            "它不是商业产品，没有真实用户，没有融资，也没有部署上线。"
        ),
        "language_instruction": "请用中文输出。",
    },
}

LANGUAGE_LABELS = {"en": "English", "zh": "中文"}

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
st.markdown(
    """
    <style>
    /* Institutional Dark theme overrides */
    :root {
        --vc-bg: #08111f;
        --vc-panel: #0f1b2d;
        --vc-panel-2: #122238;
        --vc-sidebar: #0c1728;
        --vc-border: #22324a;
        --vc-text: #f3f4f6;
        --vc-muted: #a6b0bf;
        --vc-accent: #4f7cff;
        --vc-accent-2: #d6b36a;
        --vc-input: #0e1a2b;
    }

    .stApp {
        background: var(--vc-bg);
        color: var(--vc-text);
    }

    div[data-testid="stAppViewContainer"] {
        background: var(--vc-bg);
    }

    section.main > div {
        padding-top: 1.2rem;
    }

    div[data-testid="stHeader"] {
        background: transparent;
    }

    div[data-testid="stToolbar"] {
        right: 1rem;
    }

    div[data-testid="stSidebar"] {
        background: var(--vc-sidebar);
        border-right: 1px solid var(--vc-border);
    }

    div[data-testid="stSidebar"] > div:first-child {
        background:
            linear-gradient(180deg, rgba(214, 179, 106, 0.04), rgba(214, 179, 106, 0)),
            var(--vc-sidebar);
    }

    div[data-testid="stSidebar"] * {
        color: var(--vc-text);
    }

    h1, h2, h3, h4, h5, h6,
    p, label, span, div,
    .stMarkdown, .stCaption {
        color: var(--vc-text);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--vc-muted);
    }

    div[data-testid="stExpander"] {
        background: var(--vc-panel);
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
    }

    div[data-testid="stExpander"] summary {
        color: var(--vc-text);
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: var(--vc-input);
        color: var(--vc-text);
        border: 1px solid var(--vc-border);
        border-radius: 8px;
    }

    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: var(--vc-muted);
    }

    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--vc-accent);
        box-shadow: 0 0 0 1px var(--vc-accent);
    }

    div[data-baseweb="select"] > div {
        background: var(--vc-input);
        border-color: var(--vc-border);
        min-height: 2.65rem;
    }

    div[data-baseweb="select"] * {
        color: var(--vc-text);
    }

    button[kind="primary"] {
        background: linear-gradient(180deg, var(--vc-accent), #355fd6);
        color: #f8fafc;
        border: 1px solid #6d8fff;
        border-radius: 8px;
        min-height: 2.7rem;
        font-weight: 600;
        box-shadow: 0 10px 22px rgba(34, 74, 160, 0.24);
    }

    button[kind="primary"]:hover {
        background: linear-gradient(180deg, #648cff, #416ae0);
        border-color: #8aa4ff;
        transform: translateY(-1px);
    }

    button[kind="secondary"] {
        background: var(--vc-panel-2);
        color: var(--vc-text);
        border: 1px solid var(--vc-border);
        border-radius: 8px;
    }

    button[kind="secondary"]:hover {
        border-color: var(--vc-accent-2);
        color: #fff8e7;
    }

    div[data-testid="stDownloadButton"] button {
        background: var(--vc-panel-2);
        color: var(--vc-text);
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        min-height: 2.7rem;
    }

    div[data-testid="stDownloadButton"] button:hover {
        border-color: var(--vc-accent-2);
        color: #fff8e7;
    }

    .vc-section {
        margin: 0 0 1.1rem 0;
    }

    .vc-section-title {
        margin: 0 0 0.7rem 0;
        color: var(--vc-text);
        font-size: 0.95rem;
        font-weight: 750;
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .vc-hero {
        margin: 0 0 1.15rem 0;
        padding: 1.25rem 1.3rem 1.15rem 1.3rem;
        border: 1px solid rgba(214, 179, 106, 0.22);
        border-radius: 8px;
        background:
            linear-gradient(180deg, rgba(214, 179, 106, 0.06), rgba(214, 179, 106, 0)),
            linear-gradient(180deg, rgba(18, 34, 56, 0.98), rgba(12, 23, 40, 0.98));
        box-shadow: 0 20px 44px rgba(0, 0, 0, 0.2);
    }

    .vc-hero-title {
        margin: 0;
        font-size: 2rem;
        line-height: 1.05;
        font-weight: 800;
    }

    .vc-hero-tagline {
        margin: 0.35rem 0 0 0;
        color: #dce5f5;
        font-size: 0.98rem;
        font-weight: 650;
    }

    .vc-hero-description {
        max-width: 52rem;
        margin: 0.55rem 0 0 0;
        color: var(--vc-muted);
        font-size: 0.92rem;
        line-height: 1.55;
    }

    .vc-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.8rem;
    }

    .vc-badge {
        display: inline-flex;
        align-items: center;
        min-height: 2rem;
        padding: 0.22rem 0.65rem;
        border: 1px solid rgba(79, 124, 255, 0.26);
        border-radius: 999px;
        background: rgba(79, 124, 255, 0.08);
        color: #dde7ff;
        font-size: 0.76rem;
        font-weight: 600;
    }

    .vc-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.5rem;
    }

    .vc-card {
        padding: 0.8rem 0.85rem;
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(18, 34, 56, 0.96), rgba(15, 27, 45, 0.98));
        color: var(--vc-text);
        font-size: 0.85rem;
        font-weight: 600;
        line-height: 1.3;
        min-height: 3.2rem;
        display: flex;
        align-items: center;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
    }

    .vc-step-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.5rem;
    }

    .vc-step {
        padding: 0.8rem 0.85rem;
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(20, 37, 59, 0.98), rgba(15, 27, 45, 0.98));
        color: #eaf0fa;
        font-size: 0.85rem;
        line-height: 1.35;
        min-height: 3.6rem;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
    }

    .vc-step-index {
        display: block;
        margin-bottom: 0.2rem;
        color: var(--vc-accent-2);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .vc-memo {
        margin: 1.15rem 0;
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(18, 34, 56, 0.96), rgba(15, 27, 45, 0.98));
        overflow: hidden;
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.18);
    }

    .vc-memo-header {
        padding: 1rem 1.05rem 0.9rem 1.05rem;
    }

    .vc-memo-kicker {
        margin: 0 0 0.35rem 0;
        color: var(--vc-accent-2);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .vc-memo-title {
        margin: 0;
        color: var(--vc-text);
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0;
    }

    .vc-memo-subtitle {
        margin: 0.3rem 0 0 0;
        color: var(--vc-muted);
        font-size: 0.83rem;
        line-height: 1.45;
    }

    .vc-memo-divider {
        height: 1px;
        background: var(--vc-border);
    }

    .vc-memo-body {
        padding: 1rem 1.05rem 1.05rem 1.05rem;
        background: rgba(8, 17, 31, 0.22);
    }

    .vc-memo-actions {
        margin-top: 0.85rem;
    }

    div[data-testid="stTextArea"] {
        margin-bottom: 0.25rem;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {
        transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    div[data-testid="stButton"] button:focus,
    div[data-testid="stDownloadButton"] button:focus {
        box-shadow: 0 0 0 1px rgba(214, 179, 106, 0.55);
        outline: none;
    }

    div[data-testid="stButton"] button:disabled,
    div[data-testid="stDownloadButton"] button:disabled {
        opacity: 0.58;
        box-shadow: none;
    }

    hr, div[data-testid="stDivider"] {
        border-color: var(--vc-border);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
init_state()

# Language selector - rendered first so t[] is available for everything below.
with st.sidebar:
    language = st.selectbox(
        "Language / 语言",
        options=["en", "zh"],
        index=0,
        format_func=lambda code: LANGUAGE_LABELS[code],
    )

t = TEXTS[language]

if language == "en":
    hero_tagline = "Founder Logic Pressure-Test Engine"
    hero_description = "AI-powered founder narrative assessment for early-stage investment conversations."
    hero_badges = [
        "Founder-Market Fit",
        "Execution Evidence",
        "Investor Narrative",
    ]
else:
    hero_tagline = "创始人逻辑压力测试引擎"
    hero_description = "面向早期创业者的 AI 创始人叙事评估与投资人逻辑诊断工具。"
    hero_badges = [
        "创始人-市场匹配",
        "执行证据",
        "投资人叙事",
    ]

st.markdown(
    f"""
    <div class="vc-hero">
        <h1 class="vc-hero-title">VCReady</h1>
        <p class="vc-hero-tagline">{hero_tagline}</p>
        <p class="vc-hero-description">{hero_description}</p>
        <div class="vc-badges">
            <span class="vc-badge">{hero_badges[0]}</span>
            <span class="vc-badge">{hero_badges[1]}</span>
            <span class="vc-badge">{hero_badges[2]}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if language == "en":
    assessment_title = "Assessment Framework"
    assessment_items = [
        "Founder-Market Fit",
        "Problem Urgency",
        "Execution Evidence",
        "Resilience",
        "Unfair Advantage",
    ]
    workflow_title = "Workflow"
    workflow_steps = [
        "Build Founder Dossier",
        "Generate VC Pressure-Test Questions",
        "Answer Under Investor Logic",
        "Produce Founder Reflection Report",
    ]
else:
    assessment_title = "评估框架"
    assessment_items = [
        "创始人-市场匹配",
        "问题紧迫性",
        "执行证据",
        "韧性",
        "独特优势",
    ]
    workflow_title = "工作流程"
    workflow_steps = [
        "建立创始人档案",
        "生成 VC 高压追问",
        "在投资人逻辑下作答",
        "生成创始人反思报告",
    ]

st.markdown(
    f"""
    <div class="vc-section">
        <div class="vc-section-title">{assessment_title}</div>
        <div class="vc-grid">
            <div class="vc-card">{assessment_items[0]}</div>
            <div class="vc-card">{assessment_items[1]}</div>
            <div class="vc-card">{assessment_items[2]}</div>
            <div class="vc-card">{assessment_items[3]}</div>
            <div class="vc-card">{assessment_items[4]}</div>
        </div>
    </div>
    <div class="vc-section">
        <div class="vc-section-title">{workflow_title}</div>
        <div class="vc-step-grid">
            <div class="vc-step"><span class="vc-step-index">Step 1</span>{workflow_steps[0]}</div>
            <div class="vc-step"><span class="vc-step-index">Step 2</span>{workflow_steps[1]}</div>
            <div class="vc-step"><span class="vc-step-index">Step 3</span>{workflow_steps[2]}</div>
            <div class="vc-step"><span class="vc-step-index">Step 4</span>{workflow_steps[3]}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander(t["how_it_works_title"], expanded=False):
    st.markdown(t["how_it_works_body"])


# ---------- Sidebar: founder inputs ----------

def inputs_ready() -> bool:
    return all(
        st.session_state[k].strip()
        for k in ("founder_background", "project_description", "current_evidence", "funding_goal")
    )


with st.sidebar:
    st.header(t["sidebar_header"])
    st.session_state.founder_background = st.text_area(
        t["founder_bg_label"],
        value=st.session_state.founder_background,
        height=120,
        placeholder=t["founder_bg_placeholder"],
    )
    st.session_state.project_description = st.text_area(
        t["project_desc_label"],
        value=st.session_state.project_description,
        height=120,
        placeholder=t["project_desc_placeholder"],
    )
    st.session_state.current_evidence = st.text_area(
        t["evidence_label"],
        value=st.session_state.current_evidence,
        height=120,
        placeholder=t["evidence_placeholder"],
    )
    st.session_state.funding_goal = st.text_area(
        t["goal_label"],
        value=st.session_state.funding_goal,
        height=100,
        placeholder=t["goal_placeholder"],
    )
    generate_questions_clicked = st.button(
        t["btn_questions"], type="primary", use_container_width=True
    )


# ---------- Step 1: generate questions ----------

if generate_questions_clicked:
    if not inputs_ready():
        st.warning(t["warn_fill_fields"])
    else:
        with st.spinner(t["spinner_questions"]):
            try:
                prompt = QUESTION_PROMPT.format(
                    founder_background=st.session_state.founder_background,
                    project_description=st.session_state.project_description,
                    current_evidence=st.session_state.current_evidence,
                    funding_goal=st.session_state.funding_goal,
                    language_instruction=t["language_instruction"],
                )
                raw = call_model(prompt)
                st.session_state.questions_markdown = raw
                st.session_state.answers_text = ""
                st.session_state.report_markdown = ""
                st.session_state.pop("answers_textarea", None)
            except Exception as e:
                st.error(f"{t['err_questions']}{e}")


# ---------- Step 2: display questions, collect answers ----------

if st.session_state.questions_markdown:
    st.markdown(
        f"""
        <div class="vc-memo">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">VC MEMO</p>
                <h3 class="vc-memo-title">{t["questions_subheader"]}</h3>
                <p class="vc-memo-subtitle">{t["answers_caption"]}</p>
            </div>
            <div class="vc-memo-divider"></div>
            <div class="vc-memo-body">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state.questions_markdown)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="vc-memo-header" style="padding: 0.2rem 0 0.6rem 0;">
            <p class="vc-memo-kicker">FOUNDER RESPONSE</p>
            <h3 class="vc-memo-title">{t["answers_label"]}</h3>
            <p class="vc-memo-subtitle">{t["answers_caption"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.answers_text = st.text_area(
        t["answers_label"],
        value=st.session_state.answers_text,
        key="answers_textarea",
        height=320,
        placeholder=t["answers_placeholder"],
    )

    generate_report_clicked = st.button(t["btn_report"], type="primary")

    if generate_report_clicked:
        if not st.session_state.answers_text.strip():
            st.warning(t["warn_write_answers"])
        else:
            with st.spinner(t["spinner_report"]):
                try:
                    qa_transcript = (
                        "Questions:\n"
                        f"{st.session_state.questions_markdown}\n\n"
                        "Founder's answers:\n"
                        f"{st.session_state.answers_text}"
                    )
                    report_template = REPORT_PROMPT_EN if language == "en" else REPORT_PROMPT_ZH
                    prompt = report_template.format(
                        founder_background=st.session_state.founder_background,
                        project_description=st.session_state.project_description,
                        current_evidence=st.session_state.current_evidence,
                        funding_goal=st.session_state.funding_goal,
                        qa_transcript=qa_transcript,
                    )
                    st.session_state.report_markdown = call_model(prompt)
                except Exception as e:
                    st.error(f"{t['err_report']}{e}")


# ---------- Step 3: render report + download ----------

if st.session_state.report_markdown:
    st.markdown(
        f"""
        <div class="vc-memo">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">REFLECTION REPORT</p>
                <h3 class="vc-memo-title">{t["report_subheader"]}</h3>
            </div>
            <div class="vc-memo-divider"></div>
            <div class="vc-memo-body">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state.report_markdown)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.download_button(
        label=t["btn_download"],
        data=st.session_state.report_markdown,
        file_name="vcready_founder_reflection_report.txt",
        mime="text/plain",
    )

st.divider()
st.caption(t["footer"])
