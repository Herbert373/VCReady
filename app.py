"""VCReady - Founder Logic Pressure-Test Engine.

A Streamlit prototype that simulates a sharp early-stage VC and produces
a Founder Reflection Report. Built for portfolio purposes, not commercial use.
"""

import json
import os
import re
import time

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
        "dossier_card_title": "Build Founder Dossier",
        "dossier_card_subtitle": "Set up the founder profile before generating VC pressure-test questions.",
        "dossier_ready_title": "Founder Profile Ready",
        "dossier_ready_body": "Your dossier is ready. Generate VC pressure-test questions when you are ready to start the assessment.",
        "btn_build_dossier": "Build Founder Dossier",
        "btn_edit_dossier": "Edit Dossier",
        "btn_new_session": "Start New Session",
        "profile_summary_title": "Founder Profile Summary",
        "profile_status_label": "Session status",
        "profile_status_empty": "Dossier not built",
        "profile_status_ready": "Dossier ready",
        "profile_completeness_label": "Completeness",
        "profile_field_complete": "Complete",
        "profile_field_missing": "Missing",
        "field_founder_background_short": "Founder background",
        "field_project_description_short": "Project description",
        "field_current_evidence_short": "Current evidence",
        "field_funding_goal_short": "Funding or partnership goal",
        "dossier_empty_note": "Complete the dossier on the main page to unlock question generation.",
        "warn_build_dossier": "Please complete all four dossier fields before building the Founder Dossier.",
        "guided_mode_title": "Guided Question Mode",
        "question_card_title": "Question",
        "question_card_hint": "Answer one investor question at a time. Your answers are saved per question.",
        "single_answer_placeholder": "Write your answer to this question.",
        "question_progress_label": "Question progress",
        "answered_progress_label": "Answered",
        "btn_previous_question": "Previous",
        "btn_save_answer": "Save Answer",
        "btn_next_question": "Next",
        "btn_review_all_answers": "Review All Answers",
        "btn_back_to_guided": "Back to Guided Mode",
        "answer_saved_status": "Answer saved.",
        "guided_fallback_notice": "Questions could not be split into guided cards, so the original Markdown view is shown.",
        "review_placeholder_title": "Review All Answers",
        "review_placeholder_body": "Review your answers before generating the Founder Reflection Report.",
        "review_answer_placeholder": "Edit this answer before generating the report.",
        "scaffold_expander_title": "How to think about this question",
        "report_progress_preparing_profile": "Preparing founder dossier",
        "report_progress_compiling_answers": "Compiling answers",
        "report_progress_building_request": "Building assessment request",
        "report_progress_calling_model": "Calling report model",
        "report_progress_parsing_structure": "Parsing report structure",
        "report_progress_preparing_display": "Preparing report display",
        "report_progress_ready": "Report ready",
        "footer": (
            "VCReady is an AI product prototype built for the founder's portfolio. "
            "It demonstrates founder narrative pressure-testing, prompt design, and prototype implementation. "
            "The current version is for portfolio demonstration only and is not a commercial or production-deployed product."
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
        "dossier_card_title": "建立创始人档案",
        "dossier_card_subtitle": "请先完成创始人档案，再生成 VC 压力测试问题。",
        "dossier_ready_title": "创始人档案已就绪",
        "dossier_ready_body": "档案已完成。准备好后，可以生成 VC 压力测试问题并开始评估。",
        "btn_build_dossier": "建立创始人档案",
        "btn_edit_dossier": "编辑档案",
        "btn_new_session": "开始新会话",
        "profile_summary_title": "创始人档案摘要",
        "profile_status_label": "会话状态",
        "profile_status_empty": "档案未建立",
        "profile_status_ready": "档案已就绪",
        "profile_completeness_label": "完整度",
        "profile_field_complete": "已完成",
        "profile_field_missing": "未填写",
        "field_founder_background_short": "创始人背景",
        "field_project_description_short": "项目简介",
        "field_current_evidence_short": "当前证据",
        "field_funding_goal_short": "融资或合作目标",
        "dossier_empty_note": "请在主页面完成创始人档案，以解锁问题生成。",
        "warn_build_dossier": "请先填写完整四个档案字段，再建立创始人档案。",
        "guided_mode_title": "逐题引导模式",
        "question_card_title": "问题",
        "question_card_hint": "请一次回答一个投资人问题。每一题的回答会单独保存。",
        "single_answer_placeholder": "请回答当前这一题。",
        "question_progress_label": "问题进度",
        "answered_progress_label": "已回答",
        "btn_previous_question": "上一题",
        "btn_save_answer": "保存答案",
        "btn_next_question": "下一题",
        "btn_review_all_answers": "查看全部回答",
        "btn_back_to_guided": "返回逐题模式",
        "answer_saved_status": "回答已保存。",
        "guided_fallback_notice": "问题未能稳定拆分为逐题卡片，因此显示原始 Markdown 视图。",
        "review_placeholder_title": "查看全部回答",
        "review_placeholder_body": "请在生成创始人反思报告前复核全部回答。",
        "review_answer_placeholder": "生成报告前可在这里修改这道题的回答。",
        "scaffold_expander_title": "如何思考这个问题",
        "report_progress_preparing_profile": "正在整理创始人档案",
        "report_progress_compiling_answers": "正在汇总全部回答",
        "report_progress_building_request": "正在构建评估请求",
        "report_progress_calling_model": "正在调用报告模型",
        "report_progress_parsing_structure": "正在解析报告结构",
        "report_progress_preparing_display": "正在准备报告展示",
        "report_progress_ready": "报告已生成",
        "footer": (
            "VCReady 是作者作品集构建的 AI 产品原型，用于展示创始人叙事压力测试、Prompt 设计与原型实现能力。"
            "当前版本仅用于作品集展示，并非商业化产品或生产环境部署。"
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


def parse_questions(markdown_text: str) -> list[str]:
    """Extract numbered questions from Markdown while keeping the raw text usable."""
    if not isinstance(markdown_text, str) or not markdown_text.strip():
        return []

    try:
        question_pattern = re.compile(r"^\s*(\d{1,2})[\.\)、]\s*(.+?)\s*$")
        questions: list[str] = []
        current_parts: list[str] = []

        for line in markdown_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue

            match = question_pattern.match(stripped)
            if match:
                if current_parts:
                    questions.append(" ".join(current_parts).strip())
                current_parts = [match.group(2).strip()]
            elif current_parts:
                current_parts.append(stripped)

        if current_parts:
            questions.append(" ".join(current_parts).strip())

        return [question for question in questions if question]
    except Exception:
        return []


def parse_report_markdown_sections(markdown_text: str) -> dict:
    """Split a Markdown report into heading-based sections when possible."""
    if not isinstance(markdown_text, str) or not markdown_text.strip():
        return {}

    try:
        sections: dict[str, str] = {}
        current_title = ""
        current_lines: list[str] = []
        heading_pattern = re.compile(r"^\s{0,3}#{1,4}\s+(.+?)\s*$")

        for line in markdown_text.splitlines():
            match = heading_pattern.match(line)
            if match:
                if current_title and current_lines:
                    sections[current_title] = "\n".join(current_lines).strip()
                current_title = match.group(1).strip()
                current_lines = []
            elif current_title:
                current_lines.append(line)

        if current_title and current_lines:
            sections[current_title] = "\n".join(current_lines).strip()

        return {key: value for key, value in sections.items() if key and value}
    except Exception:
        return {}


def safe_parse_report_json(text: str) -> dict:
    """Parse a JSON object from model output without breaking the Streamlit page."""
    if not isinstance(text, str) or not text.strip():
        return {}

    def _loads_dict(candidate: str) -> dict:
        try:
            parsed = json.loads(candidate.strip())
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}

    try:
        fenced_blocks = re.findall(
            r"```(?:json|JSON)?\s*(.*?)```",
            text,
            flags=re.DOTALL,
        )
        for block in fenced_blocks:
            parsed = _loads_dict(block)
            if parsed:
                return parsed

        parsed = _loads_dict(text)
        if parsed:
            return parsed

        decoder = json.JSONDecoder()
        for start_index, char in enumerate(text):
            if char != "{":
                continue
            try:
                parsed, _ = decoder.raw_decode(text[start_index:])
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                continue

        return {}
    except Exception:
        return {}


# ---------- Session state ----------

def init_state() -> None:
    st.session_state.setdefault("questions_markdown", "")
    st.session_state.setdefault("answers_text", "")
    st.session_state.setdefault("report_markdown", "")
    st.session_state.setdefault("founder_background", "")
    st.session_state.setdefault("project_description", "")
    st.session_state.setdefault("current_evidence", "")
    st.session_state.setdefault("funding_goal", "")
    st.session_state.setdefault("flow_step", "profile")
    st.session_state.setdefault("founder_profile", {})
    st.session_state.setdefault("questions_list", [])
    st.session_state.setdefault("current_question_index", 0)
    st.session_state.setdefault("answers_by_question", {})
    st.session_state.setdefault("answer_mode", "guided")
    st.session_state.setdefault("report_sections", {})
    st.session_state.setdefault("report_json", {})
    st.session_state.setdefault("report_ready", False)
    st.session_state.setdefault("report_progress_value", 0)
    st.session_state.setdefault("report_progress_label", "")
    if st.session_state.flow_step == "dossier":
        st.session_state.flow_step = "profile"


FOUNDER_PROFILE_FIELDS = (
    "founder_background",
    "project_description",
    "current_evidence",
    "funding_goal",
)


def current_founder_profile() -> dict:
    return {
        key: st.session_state.get(key, "")
        for key in FOUNDER_PROFILE_FIELDS
    }


def profile_is_complete(profile: dict) -> bool:
    return all(str(profile.get(key, "")).strip() for key in FOUNDER_PROFILE_FIELDS)


def reset_guided_answer_widgets() -> None:
    for key in list(st.session_state.keys()):
        key_text = str(key)
        if (
            key_text.startswith("answer_q_")
            or key_text.startswith("guided_answer_")
            or key_text.startswith("review_answer_")
        ):
            st.session_state[key] = ""


def reset_guided_session_state() -> None:
    st.session_state.founder_profile = {}
    st.session_state.questions_markdown = ""
    st.session_state.questions_list = []
    st.session_state.current_question_index = 0
    st.session_state.answers_by_question = {}
    st.session_state.answer_mode = "guided"
    st.session_state.answers_text = ""
    st.session_state.report_markdown = ""
    st.session_state.report_sections = {}
    st.session_state.report_json = {}
    st.session_state.report_ready = False
    st.session_state.report_progress_value = 0
    st.session_state.report_progress_label = ""
    st.session_state.founder_background = ""
    st.session_state.project_description = ""
    st.session_state.current_evidence = ""
    st.session_state.funding_goal = ""
    st.session_state.flow_step = "profile"
    if "answers_textarea" in st.session_state:
        st.session_state.answers_textarea = ""
    reset_guided_answer_widgets()


def sync_current_answer(question_index: int, answer_text: str) -> None:
    if question_index < 0:
        return
    answers = dict(st.session_state.answers_by_question)
    answers[question_index] = answer_text
    st.session_state.answers_by_question = answers


def sync_review_answers() -> None:
    answers = dict(st.session_state.answers_by_question)
    for index in range(len(st.session_state.questions_list)):
        review_key = f"review_answer_{index}"
        if review_key in st.session_state:
            answers[index] = st.session_state[review_key]
    st.session_state.answers_by_question = answers


def build_review_answers_text() -> str:
    blocks = []
    for index, question in enumerate(st.session_state.questions_list):
        answer = st.session_state.answers_by_question.get(index, "")
        blocks.append(
            f"Q{index + 1}: {question}\nA{index + 1}: {answer}".strip()
        )
    return "\n\n".join(blocks).strip()


def get_answer_scaffold(question_text: str, language: str) -> list[str]:
    text = question_text.lower()
    keyword_groups = {
        "competition_or_moat": (
            "advantage", "moat", "compete", "competition", "competitor", "incumbent",
            "defensible", "differentiation", "凭什么", "优势", "护城河", "竞争", "竞品",
            "美团", "饿了么", "大厂", "壁垒",
        ),
        "founder_advantage": (
            "founder-market", "founder market", "why you", "domain expertise",
            "background", "unique insight", "founder advantage", "创始人", "为什么是你",
            "背景", "经验", "洞察", "匹配",
        ),
        "problem_urgency": (
            "urgent", "pain", "problem", "must-have", "why now", "priority",
            "痛点", "紧迫", "刚需", "问题", "为什么现在", "优先级",
        ),
        "execution_evidence": (
            "traction", "evidence", "pilot", "prototype", "loi", "user interview",
            "execution", "验证", "证据", "试点", "原型", "访谈", "进展", "执行",
        ),
        "go_to_market": (
            "go-to-market", "gtm", "distribution", "acquire", "customer acquisition",
            "channel", "sales", "增长", "获客", "渠道", "销售", "推广", "市场进入",
        ),
        "funding_use": (
            "funding", "capital", "raise", "use of funds", "milestone", "runway",
            "融资", "资金", "募资", "钱怎么用", "里程碑", "跑道",
        ),
        "resilience_or_commitment": (
            "resilience", "commitment", "persist", "failure", "setback", "risk",
            "韧性", "承诺", "坚持", "失败", "挫折", "风险", "投入",
        ),
    }

    scaffold_texts = {
        "en": {
            "founder_advantage": [
                "Connect your background to the specific problem, not just to the industry.",
                "Name the insight you have that an outsider would likely miss.",
                "Show evidence that you can access users, partners, or data others cannot easily reach.",
                "Explain why your team can learn faster or execute better in this niche.",
            ],
            "problem_urgency": [
                "Describe who has the problem and when it becomes painful enough to act.",
                "Separate nice-to-have pain from must-solve urgency.",
                "Use concrete moments, costs, delays, or risks to show urgency.",
                "Explain why the problem matters now rather than later.",
            ],
            "execution_evidence": [
                "List the strongest proof you have already created.",
                "Separate real user behavior from opinions or compliments.",
                "Mention pilots, interviews, prototypes, LOIs, revenue, or repeat usage if available.",
                "Be honest about what is not validated yet and what experiment comes next.",
            ],
            "competition_or_moat": [
                "Acknowledge the incumbent's strengths instead of ignoring them.",
                "Define the narrower wedge or user segment you are targeting.",
                "Explain why larger players may not prioritize this specific use case.",
                "Provide concrete evidence of user access, speed, insight, or execution.",
                "If the advantage is unproven, state how you will test it next.",
            ],
            "go_to_market": [
                "Start with the first reachable user segment, not the total market.",
                "Explain the channel you can actually access now.",
                "Show why the acquisition path is credible for your current stage.",
                "Name the first conversion or retention signal you will measure.",
            ],
            "funding_use": [
                "Tie the funding request to specific milestones.",
                "Explain what risk the capital will reduce.",
                "Separate product, hiring, validation, and go-to-market uses.",
                "State what progress should be visible by the next financing point.",
            ],
            "resilience_or_commitment": [
                "Name the hard part you expect rather than giving a generic commitment statement.",
                "Use a specific example of persistence, recovery, or learning under pressure.",
                "Explain what would make you change direction versus keep going.",
                "Show that commitment is backed by behavior, not only intention.",
            ],
            "generic": [
                "Answer the investor's underlying concern, not only the literal wording.",
                "Use specific evidence before broad claims.",
                "State the strongest assumption in your answer and how you will test it.",
                "Be clear about what is proven, what is uncertain, and what comes next.",
            ],
        },
        "zh": {
            "founder_advantage": [
                "把你的背景和这个具体问题连接起来，而不是只说行业相关。",
                "说清楚你有哪些外部人不容易看到的洞察。",
                "说明你是否能接触到别人难以触达的用户、伙伴或数据。",
                "解释为什么你或团队能在这个细分场景里学得更快、执行得更好。",
            ],
            "problem_urgency": [
                "说明谁有这个问题，以及什么时候痛到必须行动。",
                "区分锦上添花的需求和必须解决的紧迫问题。",
                "用具体成本、延误、风险或场景说明紧迫性。",
                "解释为什么这个问题现在必须解决，而不是以后再解决。",
            ],
            "execution_evidence": [
                "列出你已经拿到的最强验证证据。",
                "区分真实用户行为和口头认可。",
                "如果有试点、访谈、原型、意向书、收入或复用行为，要具体说明。",
                "诚实说明哪些还没验证，以及下一步准备用什么实验验证。",
            ],
            "competition_or_moat": [
                "先承认现有玩家或竞品的资源优势，不要假装它们不存在。",
                "说明你切入的是哪个更窄、更具体的场景。",
                "解释为什么大平台或成熟玩家暂时不会优先解决这个场景。",
                "给出你更接近用户、更快验证或更能执行的具体证据。",
                "如果优势还没验证，说明下一步准备用什么实验验证。",
            ],
            "go_to_market": [
                "先说清楚最先能触达的用户群，而不是泛泛说整个市场。",
                "解释你现在真正能使用的获客渠道。",
                "说明这个获客路径为什么符合当前阶段。",
                "指出第一批要验证的转化或留存信号。",
            ],
            "funding_use": [
                "把融资需求和具体里程碑对应起来。",
                "说明这笔资金要降低哪个关键风险。",
                "区分产品、招聘、验证和市场进入等不同用途。",
                "说明到下一轮融资前应该看到什么进展。",
            ],
            "resilience_or_commitment": [
                "说出你预期最难的部分，而不是泛泛表态会坚持。",
                "用一个具体例子说明你如何在压力下恢复、学习或推进。",
                "说明什么情况下你会调整方向，什么情况下会继续坚持。",
                "让投入和承诺体现在行为上，而不只是意愿上。",
            ],
            "generic": [
                "回答投资人真正担心的问题，而不只是回应字面问题。",
                "先给具体证据，再做概括判断。",
                "说清楚你答案里最关键的假设，以及准备如何验证。",
                "区分已经证明的事、仍不确定的事和下一步行动。",
            ],
        },
    }

    matched_type = "generic"
    for scaffold_type, keywords in keyword_groups.items():
        if any(keyword in text for keyword in keywords):
            matched_type = scaffold_type
            break

    safe_language = language if language in scaffold_texts else "en"
    return scaffold_texts[safe_language].get(
        matched_type,
        scaffold_texts[safe_language]["generic"],
    )


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
        padding-top: 1.6rem;
        padding-bottom: 2.2rem;
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
        margin-top: 0.25rem;
        margin-bottom: 1.35rem;
        background: var(--vc-panel);
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
    }

    div[data-testid="stExpander"] summary {
        color: var(--vc-text);
        font-size: 0.92rem;
        font-weight: 650;
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
        margin: 0;
    }

    .vc-section + .vc-section {
        margin-top: 1.35rem;
    }

    .vc-page-sections {
        margin-top: 1.55rem;
        margin-bottom: 1.25rem;
    }

    .vc-section-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 0 0 0.75rem 0;
        color: var(--vc-text);
        font-size: 0.86rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .vc-section-title::before {
        content: "";
        width: 0.36rem;
        height: 0.36rem;
        border-radius: 999px;
        background: var(--vc-accent-2);
        box-shadow: 0 0 0 3px rgba(214, 179, 106, 0.11);
    }

    .vc-hero {
        margin: 0 0 1.55rem 0;
        padding: 1.75rem 1.9rem 1.65rem 1.9rem;
        border: 1px solid rgba(214, 179, 106, 0.24);
        border-radius: 8px;
        background:
            linear-gradient(135deg, rgba(214, 179, 106, 0.09), rgba(79, 124, 255, 0.045) 44%, rgba(214, 179, 106, 0)),
            linear-gradient(180deg, rgba(18, 34, 56, 0.99), rgba(10, 20, 35, 0.99));
        box-shadow: 0 24px 54px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.03);
    }

    .vc-hero-title {
        margin: 0;
        font-size: clamp(2.2rem, 4.2vw, 3.35rem);
        line-height: 1.05;
        font-weight: 820;
        letter-spacing: 0;
    }

    .vc-hero-tagline {
        margin: 0.55rem 0 0 0;
        color: #e3ebf8;
        font-size: 1.05rem;
        font-weight: 680;
        line-height: 1.35;
    }

    .vc-hero-description {
        max-width: 46rem;
        margin: 0.7rem 0 0 0;
        color: var(--vc-muted);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .vc-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 1.15rem;
        margin-bottom: 0.2rem;
    }

    .vc-badge {
        display: inline-flex;
        align-items: center;
        min-height: 1.85rem;
        padding: 0.18rem 0.7rem;
        border: 1px solid rgba(214, 179, 106, 0.2);
        border-radius: 999px;
        background: rgba(8, 17, 31, 0.34);
        color: #dfe7f4;
        font-size: 0.74rem;
        font-weight: 600;
        line-height: 1.2;
        white-space: nowrap;
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
        margin: 1.35rem 0;
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(18, 34, 56, 0.96), rgba(15, 27, 45, 0.98));
        overflow: hidden;
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.18);
    }

    @media (max-width: 760px) {
        section.main > div {
            padding-top: 1rem;
        }

        .vc-hero {
            padding: 1.35rem 1.05rem 1.25rem 1.05rem;
            margin-bottom: 1.25rem;
        }

        .vc-hero-title {
            font-size: 2.15rem;
        }

        .vc-hero-tagline {
            font-size: 0.98rem;
        }

        .vc-badges {
            gap: 0.45rem;
        }

        .vc-badge {
            white-space: normal;
        }

        .vc-page-sections {
            margin-top: 1.2rem;
        }
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

    .vc-dossier-shell {
        margin: 1.35rem 0;
        border-color: rgba(214, 179, 106, 0.22);
    }

    .vc-dossier-body {
        padding: 1rem 1.05rem 1.05rem 1.05rem;
    }

    .vc-profile-status {
        margin: 0.8rem 0 0.9rem 0;
        padding: 0.75rem 0.8rem;
        border: 1px solid var(--vc-border);
        border-radius: 8px;
        background: rgba(8, 17, 31, 0.28);
    }

    .vc-profile-status-label {
        margin: 0 0 0.25rem 0;
        color: var(--vc-muted);
        font-size: 0.75rem;
    }

    .vc-profile-status-value {
        margin: 0;
        color: var(--vc-text);
        font-size: 0.9rem;
        font-weight: 700;
    }

    .vc-report-shell {
        margin-top: 1.55rem;
        border-color: rgba(214, 179, 106, 0.24);
        box-shadow: 0 22px 42px rgba(0, 0, 0, 0.22);
    }

    .vc-report-shell .vc-memo-header {
        padding: 1.15rem 1.15rem 0.95rem 1.15rem;
    }

    .vc-report-shell .vc-memo-title {
        font-size: 1.12rem;
        font-weight: 760;
    }

    .vc-report-body {
        padding: 1.15rem 1.15rem 1.2rem 1.15rem;
        background: rgba(8, 17, 31, 0.18);
    }

    .vc-report-body > div[data-testid="stMarkdownContainer"] {
        max-width: 50rem;
    }

    .vc-report-body h1,
    .vc-report-body h2,
    .vc-report-body h3,
    .vc-report-body h4 {
        margin: 1.1rem 0 0.55rem 0;
        color: #f2f5fa;
        line-height: 1.28;
        letter-spacing: 0;
    }

    .vc-report-body h1:first-child,
    .vc-report-body h2:first-child,
    .vc-report-body h3:first-child,
    .vc-report-body h4:first-child {
        margin-top: 0;
    }

    .vc-report-body h1,
    .vc-report-body h2 {
        font-size: 1.03rem;
        font-weight: 760;
    }

    .vc-report-body h3,
    .vc-report-body h4 {
        font-size: 0.95rem;
        font-weight: 720;
        color: #e7edf7;
    }

    .vc-report-body p {
        margin: 0.45rem 0 0.82rem 0;
        color: #d9e0eb;
        font-size: 0.93rem;
        line-height: 1.72;
    }

    .vc-report-body ul,
    .vc-report-body ol {
        margin: 0.35rem 0 1rem 1.15rem;
        padding: 0;
    }

    .vc-report-body li {
        margin: 0 0 0.5rem 0;
        color: #dee5ef;
        font-size: 0.92rem;
        line-height: 1.66;
        padding-left: 0.08rem;
    }

    .vc-report-body li::marker {
        color: var(--vc-accent-2);
    }

    .vc-report-body strong {
        color: #f7f1e4;
        font-weight: 720;
    }

    .vc-report-body hr {
        margin: 1rem 0 1.05rem 0;
        border: 0;
        border-top: 1px solid rgba(34, 50, 74, 0.95);
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
    <div class="vc-page-sections">
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
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander(t["how_it_works_title"], expanded=False):
    st.markdown(t["how_it_works_body"])


# ---------- Founder Dossier setup ----------

def inputs_ready() -> bool:
    return profile_is_complete(current_founder_profile())


profile_field_labels = {
    "founder_background": t["field_founder_background_short"],
    "project_description": t["field_project_description_short"],
    "current_evidence": t["field_current_evidence_short"],
    "funding_goal": t["field_funding_goal_short"],
}

sidebar_profile = (
    st.session_state.founder_profile
    if st.session_state.founder_profile
    else current_founder_profile()
)
completed_fields = sum(
    1 for key in FOUNDER_PROFILE_FIELDS if str(sidebar_profile.get(key, "")).strip()
)
profile_ready = profile_is_complete(st.session_state.founder_profile)


with st.sidebar:
    st.header(t["profile_summary_title"])
    status_text = t["profile_status_ready"] if profile_ready else t["profile_status_empty"]
    st.markdown(
        f"""
        <div class="vc-profile-status">
            <p class="vc-profile-status-label">{t["profile_status_label"]}</p>
            <p class="vc-profile-status-value">{status_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"{t['profile_completeness_label']}: {completed_fields}/4")
    if not profile_ready:
        st.caption(t["dossier_empty_note"])
    else:
        for field_key in FOUNDER_PROFILE_FIELDS:
            field_status = (
                t["profile_field_complete"]
                if str(sidebar_profile.get(field_key, "")).strip()
                else t["profile_field_missing"]
            )
            st.caption(f"{profile_field_labels[field_key]}: {field_status}")

    if st.button(t["btn_edit_dossier"], use_container_width=True):
        st.session_state.flow_step = "profile"
        st.rerun()

    if st.button(t["btn_new_session"], use_container_width=True):
        reset_guided_session_state()
        st.rerun()


generate_questions_clicked = False

if st.session_state.flow_step == "profile":
    st.markdown(
        f"""
        <div class="vc-memo vc-dossier-shell">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">FOUNDER DOSSIER</p>
                <h3 class="vc-memo-title">{t["dossier_card_title"]}</h3>
                <p class="vc-memo-subtitle">{t["dossier_card_subtitle"]}</p>
            </div>
            <div class="vc-memo-divider"></div>
            <div class="vc-dossier-body">
        """,
        unsafe_allow_html=True,
    )
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
    build_dossier_clicked = st.button(
        t["btn_build_dossier"], type="primary", use_container_width=True
    )
    st.markdown("</div></div>", unsafe_allow_html=True)

    if build_dossier_clicked:
        if not inputs_ready():
            st.warning(t["warn_build_dossier"])
        else:
            st.session_state.founder_profile = current_founder_profile()
            st.session_state.flow_step = "dossier_ready"
            st.rerun()

elif st.session_state.flow_step == "dossier_ready":
    st.markdown(
        f"""
        <div class="vc-memo vc-dossier-shell">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">FOUNDER DOSSIER</p>
                <h3 class="vc-memo-title">{t["dossier_ready_title"]}</h3>
                <p class="vc-memo-subtitle">{t["dossier_ready_body"]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    generate_questions_clicked = st.button(
        t["btn_questions"], type="primary", use_container_width=True
    )


# ---------- Step 1: generate questions ----------

if generate_questions_clicked:
    if not profile_is_complete(st.session_state.founder_profile):
        st.warning(t["warn_fill_fields"])
    else:
        with st.spinner(t["spinner_questions"]):
            try:
                profile = st.session_state.founder_profile
                prompt = QUESTION_PROMPT.format(
                    founder_background=profile["founder_background"],
                    project_description=profile["project_description"],
                    current_evidence=profile["current_evidence"],
                    funding_goal=profile["funding_goal"],
                    language_instruction=t["language_instruction"],
                )
                raw = call_model(prompt)
                parsed_questions = parse_questions(raw)
                st.session_state.questions_markdown = raw
                st.session_state.questions_list = parsed_questions
                st.session_state.current_question_index = 0
                st.session_state.answers_by_question = {}
                reset_guided_answer_widgets()
                st.session_state.answer_mode = "guided"
                st.session_state.report_sections = {}
                st.session_state.report_json = {}
                st.session_state.report_ready = False
                st.session_state.flow_step = (
                    "guided_answer" if parsed_questions else "questions_fallback"
                )
                st.session_state.answers_text = ""
                st.session_state.report_markdown = ""
                st.session_state.pop("answers_textarea", None)
            except Exception as e:
                st.error(f"{t['err_questions']}{e}")


# ---------- Step 2: display questions, collect answers ----------

if st.session_state.flow_step == "guided_answer" and st.session_state.questions_list:
    question_count = len(st.session_state.questions_list)
    current_index = min(
        max(st.session_state.current_question_index, 0),
        question_count - 1,
    )
    st.session_state.current_question_index = current_index
    current_question = st.session_state.questions_list[current_index]
    current_answer_key = f"guided_answer_{current_index}"
    if current_answer_key not in st.session_state:
        st.session_state[current_answer_key] = st.session_state.answers_by_question.get(
            current_index,
            "",
        )
    answered_count = sum(
        1 for answer in st.session_state.answers_by_question.values() if str(answer).strip()
    )

    st.markdown(
        f"""
        <div class="vc-memo">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">GUIDED MODE</p>
                <h3 class="vc-memo-title">{t["guided_mode_title"]}</h3>
                <p class="vc-memo-subtitle">{t["question_card_hint"]}</p>
            </div>
            <div class="vc-memo-divider"></div>
            <div class="vc-memo-body">
                <p class="vc-memo-kicker">{t["question_progress_label"]}: {current_index + 1} / {question_count}</p>
                <h3 class="vc-memo-title">{t["question_card_title"]} {current_index + 1}</h3>
                <p class="vc-memo-subtitle">{current_question}</p>
                <p class="vc-memo-subtitle">{t["answered_progress_label"]}: {answered_count} / {question_count}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander(t["scaffold_expander_title"], expanded=False):
        for scaffold_item in get_answer_scaffold(current_question, language):
            st.markdown(f"- {scaffold_item}")

    current_answer = st.text_area(
        t["answers_label"],
        key=current_answer_key,
        height=240,
        placeholder=t["single_answer_placeholder"],
    )

    nav_cols = st.columns([1, 1, 1, 1])
    with nav_cols[0]:
        previous_clicked = st.button(
            t["btn_previous_question"],
            use_container_width=True,
            disabled=current_index == 0,
        )
    with nav_cols[1]:
        save_clicked = st.button(
            t["btn_save_answer"],
            use_container_width=True,
        )
    with nav_cols[2]:
        next_clicked = st.button(
            t["btn_next_question"],
            use_container_width=True,
            disabled=current_index >= question_count - 1,
        )
    with nav_cols[3]:
        review_clicked = st.button(
            t["btn_review_all_answers"],
            type="primary",
            use_container_width=True,
        )

    if previous_clicked:
        sync_current_answer(current_index, current_answer)
        st.session_state.current_question_index = current_index - 1
        st.rerun()
    if save_clicked:
        sync_current_answer(current_index, current_answer)
        st.success(t["answer_saved_status"])
    if next_clicked:
        sync_current_answer(current_index, current_answer)
        st.session_state.current_question_index = current_index + 1
        st.rerun()
    if review_clicked:
        sync_current_answer(current_index, current_answer)
        st.session_state.flow_step = "review_all"
        st.rerun()

elif st.session_state.flow_step == "review_all":
    sync_review_answers()
    st.markdown(
        f"""
        <div class="vc-memo">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">REVIEW</p>
                <h3 class="vc-memo-title">{t["review_placeholder_title"]}</h3>
                <p class="vc-memo-subtitle">{t["review_placeholder_body"]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for index, question in enumerate(st.session_state.questions_list):
        review_key = f"review_answer_{index}"
        if review_key not in st.session_state:
            st.session_state[review_key] = st.session_state.answers_by_question.get(index, "")
        st.markdown(
            f"""
            <div class="vc-memo">
                <div class="vc-memo-header" style="padding: 0.7rem 1rem 0.55rem 1rem;">
                    <p class="vc-memo-kicker">{t["question_card_title"]} {index + 1}</p>
                    <p class="vc-memo-subtitle">{question}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.text_area(
            t["answers_label"],
            key=review_key,
            height=180,
            placeholder=t["review_answer_placeholder"],
        )

    review_cols = st.columns([1, 1])
    with review_cols[0]:
        back_to_guided_clicked = st.button(t["btn_back_to_guided"], use_container_width=True)
    with review_cols[1]:
        generate_report_clicked = st.button(t["btn_report"], type="primary", use_container_width=True)

    if back_to_guided_clicked:
        sync_review_answers()
        st.session_state.flow_step = "guided_answer"
        st.rerun()

    if generate_report_clicked:
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        progress_bar = progress_placeholder.progress(0)

        def update_report_progress(value: int, label: str, delay: float = 0.18) -> None:
            st.session_state.report_progress_value = value
            st.session_state.report_progress_label = label
            progress_bar.progress(value)
            status_placeholder.info(label)
            if delay > 0:
                time.sleep(delay)

        try:
            update_report_progress(10, t["report_progress_preparing_profile"])
            founder_profile = st.session_state.founder_profile

            update_report_progress(25, t["report_progress_compiling_answers"])
            sync_review_answers()
            st.session_state.answers_text = build_review_answers_text()
            if not st.session_state.answers_text.strip():
                progress_placeholder.empty()
                status_placeholder.empty()
                st.warning(t["warn_write_answers"])
            else:
                update_report_progress(45, t["report_progress_building_request"], delay=0.22)
                qa_transcript = (
                    "Questions:\n"
                    f"{st.session_state.questions_markdown}\n\n"
                    "Founder's answers:\n"
                    f"{st.session_state.answers_text}"
                )
                report_template = REPORT_PROMPT_EN if language == "en" else REPORT_PROMPT_ZH
                prompt = report_template.format(
                    founder_background=founder_profile.get("founder_background", st.session_state.founder_background),
                    project_description=founder_profile.get("project_description", st.session_state.project_description),
                    current_evidence=founder_profile.get("current_evidence", st.session_state.current_evidence),
                    funding_goal=founder_profile.get("funding_goal", st.session_state.funding_goal),
                    qa_transcript=qa_transcript,
                )

                update_report_progress(65, t["report_progress_calling_model"], delay=0.3)
                report_text = call_model(prompt)

                update_report_progress(85, t["report_progress_parsing_structure"], delay=0.18)
                st.session_state.report_markdown = report_text
                st.session_state.report_json = safe_parse_report_json(report_text)
                st.session_state.report_sections = parse_report_markdown_sections(report_text)

                update_report_progress(95, t["report_progress_preparing_display"], delay=0.16)
                st.session_state.report_ready = True
                st.session_state.flow_step = "report_ready"

                st.session_state.report_progress_value = 100
                st.session_state.report_progress_label = t["report_progress_ready"]
                progress_bar.progress(100)
                status_placeholder.success(st.session_state.report_progress_label)
                time.sleep(0.18)
                st.rerun()
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.session_state.report_progress_value = 0
            st.session_state.report_progress_label = ""
            st.error(f"{t['err_report']}{e}")

elif st.session_state.flow_step == "questions_fallback" and st.session_state.questions_markdown:
    st.warning(t["guided_fallback_notice"])
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
                    st.session_state.flow_step = "report_ready"
                except Exception as e:
                    st.error(f"{t['err_report']}{e}")


# ---------- Step 3: render report + download ----------

if st.session_state.flow_step == "report_ready" and st.session_state.report_markdown:
    st.markdown(
        f"""
        <div class="vc-memo vc-report-shell">
            <div class="vc-memo-header">
                <p class="vc-memo-kicker">REFLECTION REPORT</p>
                <h3 class="vc-memo-title">{t["report_subheader"]}</h3>
            </div>
            <div class="vc-memo-divider"></div>
            <div class="vc-memo-body vc-report-body">
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
