"""VCReady - Founder Logic Pressure-Test Engine.

A Streamlit prototype that simulates a sharp early-stage VC and produces
a Founder Reflection Report. Built for portfolio purposes, not commercial use.
"""

import json
import html
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
        "assessment_context_title": "Assessment Context",
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
        "project_sector_label": "Project sector",
        "current_stage_label": "Current stage",
        "evaluation_goal_label": "Evaluation goal",
        "commercialization_horizon_label": "Commercialization horizon",
        "context_not_set": "Not set",
        "sector_consumer": "Consumer",
        "sector_saas_enterprise": "SaaS / Enterprise Software",
        "sector_marketplace": "Marketplace",
        "sector_hardware": "Hardware",
        "sector_deeptech": "DeepTech",
        "sector_embodied_ai_robotics": "Embodied AI / Robotics",
        "sector_biotech_healthcare": "Biotech / Healthcare",
        "sector_fintech": "FinTech",
        "sector_other": "Other",
        "stage_idea": "Idea",
        "stage_prototype": "Prototype",
        "stage_pilot": "Pilot",
        "stage_pre_seed": "Pre-seed",
        "stage_seed": "Seed",
        "stage_revenue_stage": "Revenue stage",
        "goal_founder_self_diagnosis": "Founder self-diagnosis",
        "goal_investor_meeting_preparation": "Investor meeting preparation",
        "goal_pitch_deck_improvement": "Pitch deck improvement",
        "goal_mentor_feedback": "Mentor feedback",
        "goal_pilot_customer_preparation": "Pilot customer preparation",
        "goal_application_portfolio_demo": "Application portfolio demo",
        "goal_other": "Other",
        "horizon_immediate_revenue_expected": "Immediate revenue expected",
        "horizon_six_to_twelve_months": "6-12 months",
        "horizon_twelve_to_twenty_four_months": "12-24 months",
        "horizon_long_cycle_pre_commercial": "Long-cycle / pre-commercial",
        "horizon_research_to_market_uncertain": "Research-to-market uncertain",
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
        "assessment_context_title": "评估上下文",
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
        "project_sector_label": "项目类型",
        "current_stage_label": "当前阶段",
        "evaluation_goal_label": "评估目标",
        "commercialization_horizon_label": "商业化周期",
        "context_not_set": "未设置",
        "sector_consumer": "Consumer",
        "sector_saas_enterprise": "SaaS / Enterprise Software",
        "sector_marketplace": "Marketplace",
        "sector_hardware": "Hardware",
        "sector_deeptech": "DeepTech",
        "sector_embodied_ai_robotics": "Embodied AI / Robotics",
        "sector_biotech_healthcare": "Biotech / Healthcare",
        "sector_fintech": "FinTech",
        "sector_other": "Other",
        "stage_idea": "Idea",
        "stage_prototype": "Prototype",
        "stage_pilot": "Pilot",
        "stage_pre_seed": "Pre-seed",
        "stage_seed": "Seed",
        "stage_revenue_stage": "Revenue stage",
        "goal_founder_self_diagnosis": "Founder self-diagnosis",
        "goal_investor_meeting_preparation": "Investor meeting preparation",
        "goal_pitch_deck_improvement": "Pitch deck improvement",
        "goal_mentor_feedback": "Mentor feedback",
        "goal_pilot_customer_preparation": "Pilot customer preparation",
        "goal_application_portfolio_demo": "Application portfolio demo",
        "goal_other": "Other",
        "horizon_immediate_revenue_expected": "Immediate revenue expected",
        "horizon_six_to_twelve_months": "6-12 months",
        "horizon_twelve_to_twenty_four_months": "12-24 months",
        "horizon_long_cycle_pre_commercial": "Long-cycle / pre-commercial",
        "horizon_research_to_market_uncertain": "Research-to-market uncertain",
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


def apply_inline_report_formatting(text: str) -> str:
    """Apply minimal inline formatting to escaped report text."""
    safe_text = html.escape(text.strip())
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe_text)


def format_report_markdown_for_card(text: str) -> str:
    """Render simple Markdown-like text as safe HTML for report cards."""
    raw_text = str(text).strip()
    if not raw_text:
        return ""

    try:
        ordered_pattern = re.compile(r"^\s*\d+\s*[\.\)\u3001]\s+")
        bullet_pattern = re.compile(r"^\s*[-*]\s+")
        html_parts = []
        paragraph_lines = []
        list_type = ""

        def flush_paragraph() -> None:
            if paragraph_lines:
                paragraph = " ".join(paragraph_lines)
                html_parts.append(f"<p>{paragraph}</p>")
                paragraph_lines.clear()

        def close_list() -> None:
            nonlocal list_type
            if list_type:
                html_parts.append(f"</{list_type}>")
                list_type = ""

        def open_list(next_type: str) -> None:
            nonlocal list_type
            if list_type == next_type:
                return
            close_list()
            flush_paragraph()
            html_parts.append(f"<{next_type}>")
            list_type = next_type

        for raw_line in raw_text.splitlines():
            line = raw_line.strip()
            if not line:
                close_list()
                flush_paragraph()
                continue

            if ordered_pattern.match(line):
                open_list("ol")
                item_text = ordered_pattern.sub("", line, count=1)
                html_parts.append(f"<li>{apply_inline_report_formatting(item_text)}</li>")
                continue

            if bullet_pattern.match(line):
                open_list("ul")
                item_text = bullet_pattern.sub("", line, count=1)
                html_parts.append(f"<li>{apply_inline_report_formatting(item_text)}</li>")
                continue

            close_list()
            paragraph_lines.append(apply_inline_report_formatting(line))

        close_list()
        flush_paragraph()
        return "".join(html_parts) if html_parts else html.escape(raw_text).replace("\n", "<br>")
    except Exception:
        return html.escape(raw_text).replace("\n", "<br>")


def format_report_card_body(body: str, variant: str = "normal") -> str:
    """Format report body text for card display."""
    raw_body = str(body).strip()
    if not raw_body:
        return ""

    try:
        if variant == "scores":
            score_rows = []
            for line in raw_body.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                cleaned = re.sub(r"^\s*[-*]\s+", "", stripped)
                match = re.match(r"^(.+?)(?:[:\uFF1A-])\s*([1-5]\s*/\s*5)\b(.*)$", cleaned)
                if match:
                    label = apply_inline_report_formatting(match.group(1))
                    score = html.escape(match.group(2).replace(" ", ""))
                    note = match.group(3).strip()
                    note_html = (
                        f'<div class="vc-report-score-note">{format_report_markdown_for_card(note)}</div>'
                        if note else ""
                    )
                    score_rows.append(
                        '<div class="vc-report-score-row">'
                        f'<span class="vc-report-score-label">{label}</span>'
                        f'<span class="vc-report-score-value">{score}</span>'
                        f"{note_html}"
                        "</div>"
                    )
            if score_rows:
                return f'<div class="vc-report-score-rows">{"".join(score_rows)}</div>'

        return format_report_markdown_for_card(raw_body)
    except Exception:
        return html.escape(raw_body).replace("\n", "<br>")


def render_report_section_card(title: str, body: str, variant: str = "normal") -> str:
    """Build one complete escaped report section card."""
    if not str(title).strip() or not str(body).strip():
        return ""

    safe_title = html.escape(str(title).strip())
    safe_body = format_report_card_body(body, variant)
    safe_variant = html.escape(str(variant).strip() or "normal")
    return (
        f'<section class="vc-report-card vc-report-card-{safe_variant}">'
        f'<h4 class="vc-report-card-title">{safe_title}</h4>'
        f'<div class="vc-report-card-body">{safe_body}</div>'
        "</section>"
    )


def render_report_dashboard(
    report_markdown: str,
    report_sections: dict,
    t: dict,
    language: str,
) -> None:
    """Render a contained report dashboard, falling back to raw Markdown."""
    try:
        if not isinstance(report_sections, dict) or not report_sections:
            st.markdown(report_markdown)
            return

        def normalize_section_title(value: str) -> str:
            normalized = re.sub(r"^[#\s\d\.\)\:：-]+", "", str(value).strip())
            normalized = re.sub(r"[*_`]+", "", normalized)
            normalized = re.sub(r"\s+", " ", normalized)
            return normalized.strip().lower()

        normalized_sections = {
            normalize_section_title(title): body
            for title, body in report_sections.items()
            if str(title).strip() and str(body).strip()
        }

        section_specs = [
            {
                "slot": "assessment_lens",
                "variant": "normal",
                "titles": {
                    "en": "Assessment Lens",
                    "zh": "\u8bc4\u4f30\u89c6\u89d2",
                },
                "aliases": [
                    "assessment lens",
                    "\u8bc4\u4f30\u89c6\u89d2",
                ],
            },
            {
                "slot": "diagnosis",
                "variant": "primary",
                "titles": {
                    "en": "One-sentence diagnosis",
                    "zh": "一句话诊断",
                },
                "aliases": [
                    "one-sentence diagnosis",
                    "one sentence diagnosis",
                    "一句话诊断",
                ],
            },
            {
                "slot": "logic_gap",
                "variant": "critical",
                "titles": {
                    "en": "Biggest logic gap",
                    "zh": "最大逻辑漏洞",
                },
                "aliases": [
                    "biggest logic gap",
                    "largest logic gap",
                    "key logic gap",
                    "最大逻辑漏洞",
                ],
            },
            {
                "slot": "strongest_part",
                "variant": "strength",
                "titles": {
                    "en": "Strongest part of the founder narrative",
                    "zh": "创始人叙事中最强的部分",
                },
                "aliases": [
                    "strongest part",
                    "strongest part of the founder narrative",
                    "strongest part of your founder narrative",
                    "创始人叙事中最强的部分",
                    "最强的部分",
                ],
            },
            {
                "slot": "scores",
                "variant": "scores",
                "titles": {
                    "en": "Scores (1-5)",
                    "zh": "\u8bc4\u5206\uff081-5 \u5206\uff09",
                },
                "aliases": [
                    "scores",
                    "scores (1-5)",
                    "scores (1-5 points)",
                    "\u8bc4\u5206",
                    "\u8bc4\u5206\uff081-5 \u5206\uff09",
                    "\u8bc4\u5206(1-5 \u5206)",
                ],
            },
            {
                "slot": "must_answer_questions",
                "variant": "questions",
                "titles": {
                    "en": "Three questions you must answer before meeting investors",
                    "zh": "\u89c1\u6295\u8d44\u4eba\u524d\u5fc5\u987b\u56de\u7b54\u7684\u4e09\u4e2a\u95ee\u9898",
                },
                "aliases": [
                    "three questions you must answer before meeting investors",
                    "must-answer questions",
                    "must answer questions",
                    "\u89c1\u6295\u8d44\u4eba\u524d\u5fc5\u987b\u56de\u7b54\u7684\u4e09\u4e2a\u95ee\u9898",
                ],
            },
            {
                "slot": "advice",
                "variant": "normal",
                "titles": {
                    "en": "Concrete advice to improve the pitch",
                    "zh": "具体修改建议",
                },
                "aliases": [
                    "concrete advice",
                    "specific advice",
                    "concrete advice to improve the pitch",
                    "concrete revision advice",
                    "具体修改建议",
                    "具体建议",
                ],
            },
        ]

        safe_language = language if language in ("en", "zh") else "en"
        cards = {}
        for spec in section_specs:
            body = ""
            for alias in spec["aliases"]:
                body = normalized_sections.get(normalize_section_title(alias), "")
                if body:
                    break
            if body:
                card_title = spec["titles"][safe_language]
                card_html = render_report_section_card(card_title, body, spec["variant"])
                if card_html:
                    cards[spec["slot"]] = card_html

        if not cards:
            st.markdown(report_markdown)
            return

        dashboard_title = html.escape(str(t.get("report_subheader", "Founder Reflection Report")))
        assessment_lens_card = cards.get("assessment_lens", "")
        diagnosis_card = cards.get("diagnosis", "")
        logic_gap_card = cards.get("logic_gap", "")
        strongest_part_card = cards.get("strongest_part", "")
        scores_card = cards.get("scores", "")
        must_answer_questions_card = cards.get("must_answer_questions", "")
        advice_card = cards.get("advice", "")

        insight_grid = ""
        if logic_gap_card or strongest_part_card:
            insight_grid = (
                '<div class="vc-report-insight-grid">'
                f"{strongest_part_card}"
                f"{logic_gap_card}"
                "</div>"
            )

        dashboard_html = (
            '<div class="vc-report-dashboard">'
            '<div class="vc-report-dashboard-header">'
            '<p class="vc-memo-kicker">REFLECTION REPORT</p>'
            f'<h3 class="vc-report-dashboard-title">{dashboard_title}</h3>'
            "</div>"
            '<div class="vc-report-dashboard-grid">'
            f"{assessment_lens_card}"
            f"{diagnosis_card}"
            f"{insight_grid}"
            f"{scores_card}"
            f"{must_answer_questions_card}"
            f"{advice_card}"
            "</div>"
            "</div>"
        )
        st.markdown(dashboard_html, unsafe_allow_html=True)
    except Exception:
        st.markdown(report_markdown)


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
    st.session_state.setdefault(
        "assessment_context",
        {
            "project_sector": "",
            "current_stage": "",
            "evaluation_goal": "",
            "commercialization_horizon": "",
        },
    )
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

ASSESSMENT_CONTEXT_FIELDS = (
    "project_sector",
    "current_stage",
    "evaluation_goal",
    "commercialization_horizon",
)

ASSESSMENT_CONTEXT_OPTIONS = {
    "project_sector": [
        {"value": "consumer", "label": {"en": "Consumer", "zh": "消费产品"}},
        {"value": "saas_enterprise", "label": {"en": "SaaS / Enterprise Software", "zh": "SaaS / 企业软件"}},
        {"value": "marketplace", "label": {"en": "Marketplace", "zh": "平台 / 双边市场"}},
        {"value": "hardware", "label": {"en": "Hardware", "zh": "硬件"}},
        {"value": "deeptech", "label": {"en": "DeepTech", "zh": "深科技"}},
        {"value": "embodied_ai_robotics", "label": {"en": "Embodied AI / Robotics", "zh": "具身智能 / 机器人"}},
        {"value": "biotech_healthcare", "label": {"en": "Biotech / Healthcare", "zh": "生物科技 / 医疗健康"}},
        {"value": "fintech", "label": {"en": "FinTech", "zh": "金融科技"}},
        {"value": "other", "label": {"en": "Other", "zh": "其他"}},
    ],
    "current_stage": [
        {"value": "idea", "label": {"en": "Idea", "zh": "想法阶段"}},
        {"value": "prototype", "label": {"en": "Prototype", "zh": "原型阶段"}},
        {"value": "pilot", "label": {"en": "Pilot", "zh": "试点阶段"}},
        {"value": "pre_seed", "label": {"en": "Pre-seed", "zh": "Pre-seed 阶段"}},
        {"value": "seed", "label": {"en": "Seed", "zh": "Seed 阶段"}},
        {"value": "revenue_stage", "label": {"en": "Revenue stage", "zh": "收入阶段"}},
    ],
    "evaluation_goal": [
        {"value": "founder_self_diagnosis", "label": {"en": "Founder self-diagnosis", "zh": "创始人自我诊断"}},
        {"value": "investor_meeting_preparation", "label": {"en": "Investor meeting preparation", "zh": "投资人面谈准备"}},
        {"value": "pitch_deck_improvement", "label": {"en": "Pitch deck improvement", "zh": "商业计划书改进"}},
        {"value": "mentor_feedback", "label": {"en": "Mentor feedback", "zh": "导师反馈"}},
        {"value": "pilot_customer_preparation", "label": {"en": "Pilot customer preparation", "zh": "试点客户准备"}},
        {"value": "application_portfolio_demo", "label": {"en": "Application portfolio demo", "zh": "申请作品集展示"}},
        {"value": "other", "label": {"en": "Other", "zh": "其他"}},
    ],
    "commercialization_horizon": [
        {"value": "immediate_revenue_expected", "label": {"en": "Immediate revenue expected", "zh": "预计立即产生收入"}},
        {"value": "six_to_twelve_months", "label": {"en": "6-12 months", "zh": "6-12 个月"}},
        {"value": "twelve_to_twenty_four_months", "label": {"en": "12-24 months", "zh": "12-24 个月"}},
        {"value": "long_cycle_pre_commercial", "label": {"en": "Long-cycle / pre-commercial", "zh": "长周期 / 商业化前"}},
        {"value": "research_to_market_uncertain", "label": {"en": "Research-to-market uncertain", "zh": "科研转商业路径不确定"}},
    ],
}


def current_founder_profile() -> dict:
    return {
        key: st.session_state.get(key, "")
        for key in FOUNDER_PROFILE_FIELDS
    }


def current_assessment_context() -> dict:
    stored_context = st.session_state.get("assessment_context", {})
    return {
        key: str(stored_context.get(key, "")).strip()
        for key in ASSESSMENT_CONTEXT_FIELDS
    }


def assessment_context_option_values(field_key: str) -> list[str]:
    return [
        option["value"]
        for option in ASSESSMENT_CONTEXT_OPTIONS.get(field_key, [])
    ]


def assessment_context_label(field_key: str, value: str, language: str) -> str:
    safe_language = language if language in ("en", "zh") else "en"
    for option in ASSESSMENT_CONTEXT_OPTIONS.get(field_key, []):
        if option["value"] == value:
            return option["label"].get(safe_language, option["label"]["en"])
    return value


def build_assessment_context_prompt_block(context: dict, language: str) -> str:
    safe_language = language if language in ("en", "zh") else "en"
    safe_context = context or {}
    context_lines = []
    field_titles = {
        "project_sector": "Project sector",
        "current_stage": "Current stage",
        "evaluation_goal": "Evaluation goal",
        "commercialization_horizon": "Commercialization horizon",
    }

    for field_key in ASSESSMENT_CONTEXT_FIELDS:
        value = str(safe_context.get(field_key, "")).strip()
        label = assessment_context_label(field_key, value, "en") if value else "Not specified"
        context_lines.append(f"- {field_titles[field_key]}: {label}")

    output_language = "English" if safe_language == "en" else "Chinese"
    return "\n".join(
        [
            "Assessment context for question generation:",
            *context_lines,
            (
                "Use this context to make the questions more relevant, but the final "
                f"question output language is still controlled by the base prompt "
                f"language instruction ({output_language})."
            ),
        ]
    )


def build_evaluation_lens(context: dict, language: str) -> str:
    safe_context = context or {}
    project_sector = str(safe_context.get("project_sector", "")).strip()
    current_stage = assessment_context_label(
        "current_stage",
        str(safe_context.get("current_stage", "")).strip(),
        "en",
    )
    commercialization_horizon = assessment_context_label(
        "commercialization_horizon",
        str(safe_context.get("commercialization_horizon", "")).strip(),
        "en",
    )
    sector_focus = {
        "embodied_ai_robotics": (
            "Do not judge this project by short-term revenue alone. Do not apply a "
            "pure SaaS or consumer internet standard mechanically. Pressure-test "
            "scenario clarity, technical feasibility, task success rate, pilot path, "
            "data loop, deployment cost, delivery complexity, industry partners, "
            "capital needs and milestones. Still question the commercialization path, "
            "but do not treat short-term revenue as the only standard."
        ),
        "deeptech": (
            "Do not judge this project by short-term revenue alone. Do not apply a "
            "pure SaaS or consumer internet standard mechanically. Pressure-test "
            "scenario clarity, technical feasibility, task success rate, pilot path, "
            "data loop, deployment cost, delivery complexity, industry partners, "
            "capital needs and milestones. Still question the commercialization path, "
            "but do not treat short-term revenue as the only standard."
        ),
        "hardware": (
            "Do not judge this project by short-term revenue alone. Do not apply a "
            "pure SaaS or consumer internet standard mechanically. Pressure-test "
            "scenario clarity, technical feasibility, task success rate, pilot path, "
            "data loop, deployment cost, delivery complexity, industry partners, "
            "capital needs and milestones. Still question the commercialization path, "
            "but do not treat short-term revenue as the only standard."
        ),
        "biotech_healthcare": (
            "Do not judge this project by short-term revenue alone. Do not apply a "
            "pure SaaS or consumer internet standard mechanically. Pressure-test "
            "scenario clarity, technical feasibility, task success rate, pilot path, "
            "data loop, deployment cost, delivery complexity, industry partners, "
            "capital needs and milestones. Still question the commercialization path, "
            "but do not treat short-term revenue as the only standard."
        ),
        "saas_enterprise": (
            "Focus on user pain, willingness to pay, retention, sales cycle, GTM, "
            "and CAC / LTV logic."
        ),
        "consumer": (
            "Focus on usage frequency, distribution, retention, brand or community "
            "momentum, network effects, and monetization path."
        ),
        "marketplace": (
            "Focus on cold start, supply-demand liquidity, trust mechanism, "
            "transaction frequency, and take rate logic."
        ),
        "fintech": (
            "Focus on compliance risk, trust, data source, acquisition cost, risk "
            "control, and the real financial pain point."
        ),
    }
    lens_lines = [
        "Evaluation lens:",
        "- Generate exactly 7 VC pressure-test questions.",
        "- Keep the existing question output format.",
        "- Do not generate a report.",
        "- Do not answer the questions.",
        "- Do not add long explanations before or after the questions.",
        "- Stay skeptical, specific, and pressure-testing.",
        "- Context-aware does not mean lenient.",
    ]

    if project_sector:
        lens_lines.append(f"- Sector-specific lens: {sector_focus.get(project_sector, 'Use a balanced early-stage venture assessment lens.')}")
    else:
        lens_lines.append("- Sector-specific lens: Use a balanced early-stage venture assessment lens.")

    if current_stage:
        lens_lines.append(f"- Adjust question depth to the current stage: {current_stage}.")
    if commercialization_horizon:
        lens_lines.append(
            f"- Calibrate commercialization expectations to this horizon: {commercialization_horizon}."
        )

    return "\n".join(lens_lines)


def build_report_evaluation_lens(context: dict, language: str) -> str:
    safe_language = language if language in ("en", "zh") else "en"
    safe_context = context or {}
    project_sector = str(safe_context.get("project_sector", "")).strip()
    commercialization_horizon = str(
        safe_context.get("commercialization_horizon", "")
    ).strip()
    current_stage_label = assessment_context_label(
        "current_stage",
        str(safe_context.get("current_stage", "")).strip(),
        "en",
    )
    commercialization_horizon_label = assessment_context_label(
        "commercialization_horizon",
        commercialization_horizon,
        "en",
    )
    section_title = "Assessment Lens" if safe_language == "en" else "\u8bc4\u4f30\u89c6\u89d2"
    required_sections = (
        "One-sentence diagnosis; Strongest part of the founder narrative; "
        "Biggest logic gap; Scores (1-5); Three questions you must answer "
        "before meeting investors; Concrete advice to improve the pitch"
        if safe_language == "en"
        else (
            "\u4e00\u53e5\u8bdd\u8bca\u65ad; "
            "\u521b\u59cb\u4eba\u53d9\u4e8b\u4e2d\u6700\u5f3a\u7684\u90e8\u5206; "
            "\u6700\u5927\u903b\u8f91\u6f0f\u6d1e; "
            "\u8bc4\u5206\uff081-5 \u5206\uff09; "
            "\u89c1\u6295\u8d44\u4eba\u524d\u5fc5\u987b\u56de\u7b54\u7684\u4e09\u4e2a\u95ee\u9898; "
            "\u5177\u4f53\u4fee\u6539\u5efa\u8bae"
        )
    )
    sector_focus = {
        "embodied_ai_robotics": (
            "Use a long-cycle technical venture lens. Do not judge failure by "
            "short-term revenue alone or apply pure SaaS / consumer internet "
            "standards mechanically. Evaluate scenario clarity, technical "
            "feasibility, task success rate, pilot path, data loop, deployment "
            "cost, delivery complexity, industry partners, capital needs and "
            "milestones, and credible commercialization path."
        ),
        "deeptech": (
            "Use a long-cycle technical venture lens. Do not judge failure by "
            "short-term revenue alone or apply pure SaaS / consumer internet "
            "standards mechanically. Evaluate scenario clarity, technical "
            "feasibility, task success rate, pilot path, data loop, deployment "
            "cost, delivery complexity, industry partners, capital needs and "
            "milestones, and credible commercialization path."
        ),
        "hardware": (
            "Use a long-cycle technical venture lens. Do not judge failure by "
            "short-term revenue alone or apply pure SaaS / consumer internet "
            "standards mechanically. Evaluate scenario clarity, technical "
            "feasibility, task success rate, pilot path, data loop, deployment "
            "cost, delivery complexity, industry partners, capital needs and "
            "milestones, and credible commercialization path."
        ),
        "biotech_healthcare": (
            "Use a long-cycle technical venture lens. Do not judge failure by "
            "short-term revenue alone or apply pure SaaS / consumer internet "
            "standards mechanically. Evaluate scenario clarity, technical "
            "feasibility, task success rate, pilot path, data loop, deployment "
            "cost, delivery complexity, industry partners, capital needs and "
            "milestones, and credible commercialization path."
        ),
        "saas_enterprise": (
            "Use a SaaS / enterprise lens focused on user pain, willingness to "
            "pay, retention, sales cycle, GTM, and CAC / LTV logic."
        ),
        "consumer": (
            "Use a consumer lens focused on usage frequency, distribution, "
            "retention, brand or community momentum, network effects, and "
            "monetization path."
        ),
        "marketplace": (
            "Use a marketplace lens focused on cold start, supply-demand "
            "liquidity, trust mechanism, transaction frequency, and take rate "
            "logic."
        ),
        "fintech": (
            "Use a fintech lens focused on compliance risk, trust, data source, "
            "acquisition cost, risk control, and the real financial pain point."
        ),
    }
    long_cycle_context = project_sector in {
        "embodied_ai_robotics",
        "deeptech",
        "hardware",
        "biotech_healthcare",
    } or commercialization_horizon in {
        "long_cycle_pre_commercial",
        "research_to_market_uncertain",
    }
    lens_lines = [
        "Report evaluation lens:",
        f"- Add a report section headed exactly: ## {section_title}",
        (
            "- In that section, explain project sector, current stage, evaluation "
            "goal, commercialization horizon, the assessment lens used, standards "
            "that should not be applied mechanically, and the standards that matter "
            "most in this review."
        ),
        f"- Keep all existing report sections: {required_sections}.",
        "- Do not remove, rename, or merge the existing report sections.",
        "- Do not generate JSON, a risk map, follow-up questions, or answers for the founder.",
        "- Context-aware does not mean lenient.",
        "- Do not excuse weak logic, missing evidence, vague milestones, or unclear customer need.",
    ]

    if project_sector:
        lens_lines.append(
            f"- Sector lens: {sector_focus.get(project_sector, 'Use a generic early-stage founder assessment lens.')}"
        )
    else:
        lens_lines.append("- Sector lens: Use a generic early-stage founder assessment lens.")

    if current_stage_label:
        lens_lines.append(f"- Stage lens: Calibrate evidence expectations to {current_stage_label}.")
    if commercialization_horizon_label:
        lens_lines.append(
            f"- Commercialization horizon lens: Calibrate timing expectations to {commercialization_horizon_label}."
        )
    if long_cycle_context:
        lens_lines.extend(
            [
                "- For this long-cycle or technical context, do not make short-term revenue, CAC, or fast profitability the only standard.",
                "- Stay strict: if scenario clarity is weak, say so.",
                "- Stay strict: if technical validation is insufficient, say so.",
                "- Stay strict: if pilot path, deployment cost, industry partners, or milestones are unclear, say so.",
            ]
        )

    return "\n".join(lens_lines)


def build_assessment_lens_markdown(context: dict, language: str) -> str:
    safe_language = language if language in ("en", "zh") else "en"
    safe_context = context or {}
    sector_value = str(safe_context.get("project_sector", "")).strip()
    stage_value = str(safe_context.get("current_stage", "")).strip()
    goal_value = str(safe_context.get("evaluation_goal", "")).strip()
    horizon_value = str(safe_context.get("commercialization_horizon", "")).strip()

    sector_label_en = assessment_context_label("project_sector", sector_value, "en") if sector_value else "Not specified"
    stage_label_en = assessment_context_label("current_stage", stage_value, "en") if stage_value else "Not specified"
    goal_label_en = assessment_context_label("evaluation_goal", goal_value, "en") if goal_value else "Not specified"
    horizon_label_en = (
        assessment_context_label("commercialization_horizon", horizon_value, "en")
        if horizon_value else "Not specified"
    )

    long_cycle_context = sector_value in {
        "embodied_ai_robotics",
        "deeptech",
        "hardware",
        "biotech_healthcare",
    } or horizon_value in {
        "long_cycle_pre_commercial",
        "research_to_market_uncertain",
    }

    if safe_language == "zh":
        body_lines = [
            "## \u8bc4\u4f30\u89c6\u89d2",
            "",
            "\u672c\u62a5\u544a\u91c7\u7528\u4ee5\u4e0b\u8bc4\u4f30\u4e0a\u4e0b\u6587\uff1a",
            f"- \u9879\u76ee\u7c7b\u578b\uff1a{sector_label_en}",
            f"- \u5f53\u524d\u9636\u6bb5\uff1a{stage_label_en}",
            f"- \u8bc4\u4f30\u76ee\u6807\uff1a{goal_label_en}",
            f"- \u5546\u4e1a\u5316\u5468\u671f\uff1a{horizon_label_en}",
            "",
        ]
        if long_cycle_context:
            body_lines.append(
                "\u672c\u62a5\u544a\u4e0d\u4f1a\u5c06\u77ed\u671f\u6536\u5165\u3001CAC \u6216\u5feb\u901f\u76c8\u5229\u4f5c\u4e3a\u552f\u4e00\u5224\u65ad\u6807\u51c6\u3002\u5bf9\u4e8e DeepTech / \u5177\u8eab\u667a\u80fd / \u786c\u4ef6 / \u751f\u7269\u79d1\u6280\u7b49\u957f\u5468\u671f\u6216\u5546\u4e1a\u5316\u524d\u9879\u76ee\uff0c\u672c\u62a5\u544a\u91cd\u70b9\u5173\u6ce8\u573a\u666f\u6e05\u6670\u5ea6\u3001\u6280\u672f\u53ef\u884c\u6027\u3001\u4efb\u52a1\u6210\u529f\u7387\u3001\u8bd5\u70b9\u8def\u5f84\u3001\u6570\u636e\u95ed\u73af\u3001\u90e8\u7f72\u6210\u672c\u3001\u4ea4\u4ed8\u590d\u6742\u5ea6\u3001\u4ea7\u4e1a\u4f19\u4f34\u3001\u8d44\u672c\u9700\u6c42\u4e0e\u91cc\u7a0b\u7891\u3002"
            )
        else:
            body_lines.append(
                "\u672c\u62a5\u544a\u4f1a\u6839\u636e\u9879\u76ee\u7c7b\u578b\u3001\u5f53\u524d\u9636\u6bb5\u3001\u8bc4\u4f30\u76ee\u6807\u548c\u5546\u4e1a\u5316\u5468\u671f\u8c03\u6574\u8bc4\u4ef7\u89c6\u89d2\uff0c\u91cd\u70b9\u68c0\u67e5\u8bc1\u636e\u5f3a\u5ea6\u3001\u7528\u6237\u75db\u70b9\u3001\u7559\u5b58\u6216\u4ea4\u6613\u673a\u5236\u3001\u5546\u4e1a\u5316\u8def\u5f84\u4e0e\u6267\u884c\u53ef\u884c\u6027\u3002"
            )
        body_lines.extend(
            [
                "",
                "但 context-aware 不等于放宽标准。如果场景不清楚、技术验证不足、试点路径不明确、部署成本不可解释或商业化里程碑不具体，报告仍然会明确指出。",
            ]
        )
    else:
        body_lines = [
            "## Assessment Lens",
            "",
            "This report uses the following assessment context:",
            f"- Project sector: {sector_label_en}",
            f"- Current stage: {stage_label_en}",
            f"- Evaluation goal: {goal_label_en}",
            f"- Commercialization horizon: {horizon_label_en}",
            "",
        ]
        if long_cycle_context:
            body_lines.append(
                "This report should not treat short-term revenue, CAC, or fast profitability as the only signals. For DeepTech / Embodied AI / Hardware / Biotech or pre-commercial projects, it focuses on scenario clarity, technical feasibility, task success rate, pilot path, data loop, deployment cost, delivery complexity, industry partners, capital needs, and milestones."
            )
        else:
            body_lines.append(
                "This report calibrates its judgment to the project sector, current stage, evaluation goal, and commercialization horizon, with emphasis on evidence strength, customer pain, retention or transaction behavior, commercialization path, and execution credibility."
            )
        body_lines.extend(
            [
                "",
                "Context-aware does not mean lenient. If scenario definition, technical validation, pilot path, deployment economics, or commercialization milestones are weak, the report should still state that clearly.",
            ]
        )

    return "\n".join(body_lines).strip()


def ensure_report_has_assessment_lens(
    report_markdown: str,
    context: dict,
    language: str,
) -> str:
    raw_report = str(report_markdown or "").strip()
    if not raw_report:
        return build_assessment_lens_markdown(context, language)

    heading_patterns = (
        r"(?mi)^\s*#{1,2}\s*Assessment Lens\s*$",
        r"(?mi)^\s*#{1,2}\s*\u8bc4\u4f30\u89c6\u89d2\s*$",
    )
    for pattern in heading_patterns:
        if re.search(pattern, raw_report):
            return raw_report

    assessment_lens_markdown = build_assessment_lens_markdown(context, language)
    return f"{assessment_lens_markdown}\n\n{raw_report}".strip()


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
    st.session_state.assessment_context = {
        "project_sector": "",
        "current_stage": "",
        "evaluation_goal": "",
        "commercialization_horizon": "",
    }
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

    priority_order = [
        "competition_or_moat",
        "execution_evidence",
        "go_to_market",
        "funding_use",
        "problem_urgency",
        "resilience_or_commitment",
        "founder_advantage",
        "generic",
    ]

    matched_type = "generic"
    for scaffold_type in priority_order:
        if scaffold_type == "generic":
            continue
        keywords = keyword_groups.get(scaffold_type, ())
        if any(keyword in text for keyword in keywords):
            matched_type = scaffold_type
            break

    safe_language = language if language in scaffold_texts else "en"
    selected_scaffold = scaffold_texts[safe_language].get(
        matched_type,
        scaffold_texts[safe_language]["generic"],
    )

    deduped_scaffold = []
    seen_lines = set()
    for item in selected_scaffold:
        normalized_item = re.sub(r"\s+", " ", item.strip().lower())
        if not normalized_item or normalized_item in seen_lines:
            continue
        seen_lines.add(normalized_item)
        deduped_scaffold.append(item)
        if len(deduped_scaffold) >= 5:
            break

    return deduped_scaffold or scaffold_texts[safe_language]["generic"][:4]


SCAFFOLD_CATEGORY_PRIORITY = [
    "competition_or_moat",
    "execution_evidence",
    "go_to_market",
    "funding_use",
    "problem_urgency",
    "resilience_or_commitment",
    "founder_advantage",
    "generic",
]

SCAFFOLD_KEYWORDS = {
    "competition_or_moat": (
        "凭什么", "优势", "护城河", "竞争", "竞品", "美团", "饿了么", "壁垒",
        "advantage", "moat", "compete", "competition", "competitor", "incumbent",
        "defensible", "differentiation",
    ),
    "execution_evidence": (
        "证据", "验证", "试点", "原型", "用户访谈", "访谈", "数据", "进展",
        "traction", "evidence", "prototype", "pilot", "loi", "user interview",
        "validation", "validated",
    ),
    "go_to_market": (
        "获客", "用户增长", "渠道", "销售", "转化", "留存", "cac",
        "distribution", "growth", "go-to-market", "gtm", "channel",
        "customer acquisition", "sales",
    ),
    "funding_use": (
        "融资", "钱怎么花", "资金", "里程碑", " runway", "募资",
        "funding", "capital", "raise", "use of funds", "milestone", "runway",
    ),
    "problem_urgency": (
        "痛点", "紧迫", "刚需", "优先级", "为什么现在", "问题紧迫",
        "urgent", "urgency", "pain", "must-have", "why now", "problem urgency",
        "priority",
    ),
    "resilience_or_commitment": (
        "韧性", "坚持", "失败", "挫折", "风险", "承诺", "投入",
        "resilience", "commitment", "persist", "failure", "setback", "risk",
    ),
    "founder_advantage": (
        "创始人", "为什么是你", "背景", "经历", "洞察", "匹配",
        "founder-market", "founder market", "why you", "domain expertise",
        "background", "unique insight", "founder advantage",
    ),
    "generic": (),
}

SCAFFOLD_BANK = {
    "en": {
        "competition_or_moat": [
            [
                "Name the incumbent or substitute you are being compared against.",
                "Explain the narrow wedge where your approach is meaningfully better.",
                "Show the evidence that users would switch or start with you.",
                "State what part of the advantage is still unproven.",
            ],
            [
                "Separate temporary speed from a durable advantage.",
                "Describe the user access, data, workflow, or insight others lack.",
                "Acknowledge why large players may ignore this niche for now.",
                "Name the test that would prove your moat is real.",
            ],
        ],
        "execution_evidence": [
            [
                "List the strongest concrete proof you already have.",
                "Separate real behavior from compliments or opinions.",
                "Mention pilots, interviews, usage, LOIs, revenue, or prototypes if available.",
                "Name the next experiment that would reduce the biggest uncertainty.",
            ],
            [
                "Start with what has been validated, not what you hope is true.",
                "Describe who gave the signal and what they actually did.",
                "Call out weak evidence honestly before the investor does.",
                "Tie each claim to one observable metric or user action.",
            ],
        ],
        "go_to_market": [
            [
                "Start with the first reachable user segment.",
                "Name the channel you can access now, not later at scale.",
                "Explain why this channel should convert for your current stage.",
                "Identify the first acquisition or retention signal you will track.",
            ],
            [
                "Avoid total-market language; describe the first repeatable path.",
                "State who makes the buying or adoption decision.",
                "Explain the cost, friction, or trust barrier in the channel.",
                "Name the smallest campaign or pilot that can test the channel.",
            ],
        ],
        "funding_use": [
            [
                "Tie the funding request to specific milestones.",
                "Explain which risk the capital reduces first.",
                "Separate product, hiring, validation, and go-to-market uses.",
                "State what should be true by the next financing point.",
            ],
            [
                "Translate money into time, experiments, and measurable outcomes.",
                "Prioritize one or two critical risks instead of listing everything.",
                "Explain what you would not spend on yet.",
                "Define the evidence investors should see after this round.",
            ],
        ],
        "problem_urgency": [
            [
                "Describe who has the problem and when it becomes painful.",
                "Separate nice-to-have interest from must-solve urgency.",
                "Use concrete costs, delays, risks, or workflow breakdowns.",
                "Explain why this matters now instead of later.",
            ],
            [
                "Name the moment that forces the user to act.",
                "Show what happens if the user keeps the current workaround.",
                "Clarify whether the buyer and the sufferer are the same person.",
                "Use a specific scenario instead of a broad market claim.",
            ],
        ],
        "resilience_or_commitment": [
            [
                "Name the hard part you realistically expect.",
                "Use a specific example of persistence or learning under pressure.",
                "Explain what would make you persist versus change direction.",
                "Show commitment through behavior, not only intention.",
            ],
            [
                "Describe the tradeoff you have already accepted to pursue this.",
                "Show how you respond when evidence contradicts your plan.",
                "Name the support system or operating habit that keeps execution stable.",
                "Avoid heroic claims; use one concrete decision or action.",
            ],
        ],
        "founder_advantage": [
            [
                "Connect your background to this specific problem.",
                "Name the insight an outsider would likely miss.",
                "Show how your access to users, partners, or data is different.",
                "Explain why you can learn faster in this niche.",
            ],
            [
                "Avoid a generic biography; focus on relevant earned insight.",
                "Describe the moment that made you see the problem differently.",
                "State what capability you have that the project depends on.",
                "Tie founder-market fit to evidence, not identity alone.",
            ],
        ],
        "generic": [
            [
                "Answer the investor's underlying concern, not only the literal wording.",
                "Use specific evidence before broad claims.",
                "State the strongest assumption and how you will test it.",
                "Separate what is proven, uncertain, and next.",
            ],
            [
                "Start with the direct answer in one sentence.",
                "Add one concrete example or data point.",
                "Name the risk your answer does not fully solve yet.",
                "End with the next action or validation step.",
            ],
        ],
    },
    "zh": {
        "competition_or_moat": [
            [
                "先说清楚投资人会把你和谁比较。",
                "说明你切入的具体场景为什么更窄、更有效。",
                "给出用户愿意切换或优先选择你的证据。",
                "说清楚哪些优势还没有被验证。",
            ],
            [
                "区分短期速度和长期壁垒。",
                "说明你独有的用户入口、数据、流程或洞察。",
                "解释为什么大玩家暂时不会优先解决这个细分场景。",
                "说出下一步如何验证护城河是否真实。",
            ],
        ],
        "execution_evidence": [
            [
                "先列出已经拿到的最强证据。",
                "区分真实行为和口头认可。",
                "如果有试点、访谈、使用数据、意向书、收入或原型，要具体说明。",
                "指出下一步实验要降低哪一个最大不确定性。",
            ],
            [
                "先说已经验证的事实，不要先说愿景。",
                "说明信号来自谁，以及对方实际做了什么。",
                "主动承认薄弱证据，避免被投资人追问时被动。",
                "把每个关键判断对应到一个可观察指标或用户行为。",
            ],
        ],
        "go_to_market": [
            [
                "先说最先能触达的用户群，而不是总市场。",
                "说明现在就能使用的渠道。",
                "解释这个渠道为什么适合当前阶段。",
                "指出第一个获客或留存信号是什么。",
            ],
            [
                "不要泛泛说市场很大，要说第一条可重复路径。",
                "说明谁做购买或采用决策。",
                "解释渠道里的成本、阻力或信任门槛。",
                "说出最小的一次渠道实验或试点。",
            ],
        ],
        "funding_use": [
            [
                "把融资需求对应到具体里程碑。",
                "说明这笔钱优先降低哪一个风险。",
                "区分产品、招聘、验证和市场进入等用途。",
                "说清楚下一轮融资前应该看到什么证据。",
            ],
            [
                "把钱翻译成时间、实验和可衡量结果。",
                "优先说明一两个关键风险，不要罗列所有事项。",
                "说明现阶段不会把钱花在哪里。",
                "定义这轮之后投资人应该看到的验证结果。",
            ],
        ],
        "problem_urgency": [
            [
                "说明谁有这个问题，以及什么时候痛到必须行动。",
                "区分锦上添花的兴趣和必须解决的紧迫需求。",
                "用具体成本、延误、风险或流程崩溃来说明痛点。",
                "解释为什么现在必须解决，而不是以后再说。",
            ],
            [
                "说出迫使用户采取行动的具体时刻。",
                "说明如果继续用现有替代方案，会发生什么损失。",
                "区分付费决策者和真正承受痛点的人。",
                "用一个具体场景代替宽泛市场判断。",
            ],
        ],
        "resilience_or_commitment": [
            [
                "说出你预期最难的部分。",
                "用一个具体例子说明你如何在压力下学习或恢复。",
                "解释什么情况下会坚持，什么情况下会调整方向。",
                "用行为证明投入，而不是只表达态度。",
            ],
            [
                "说明你已经为这件事接受了什么取舍。",
                "展示当证据和计划冲突时你如何反应。",
                "说出支撑持续执行的习惯或机制。",
                "避免空泛表态，用一个具体决定或行动来证明。",
            ],
        ],
        "founder_advantage": [
            [
                "把你的背景和这个具体问题连接起来。",
                "说出外部人容易忽略、但你看到的洞察。",
                "说明你接触用户、伙伴或数据的方式有什么不同。",
                "解释为什么你能在这个细分场景里学得更快。",
            ],
            [
                "不要写泛泛履历，要聚焦相关的真实洞察。",
                "描述你什么时候开始用不同方式理解这个问题。",
                "说出项目最依赖你的哪项能力。",
                "把创始人匹配度落到证据上，而不是身份标签上。",
            ],
        ],
        "generic": [
            [
                "回答投资人真正担心的问题，而不只是回应字面问题。",
                "先给具体证据，再做概括判断。",
                "说清楚最关键的假设，以及准备如何验证。",
                "区分已经证明的事、仍不确定的事和下一步行动。",
            ],
            [
                "先用一句话直接回答问题。",
                "补充一个具体例子或数据点。",
                "指出这个答案还没有完全解决的风险。",
                "最后给出下一步验证或行动。",
            ],
        ],
    },
}


SCAFFOLD_EXTRA_CATEGORY_PRIORITY = [
    "technical_or_deeptech_validation",
    "competition_or_moat",
    "execution_evidence",
    "go_to_market",
    "funding_use",
    "problem_urgency",
    "resilience_or_commitment",
    "founder_advantage",
    "generic",
]

SCAFFOLD_EXTRA_KEYWORDS = {
    "technical_or_deeptech_validation": (
        "\u6280\u672f", "\u7b97\u6cd5", "\u786c\u4ef6", "\u673a\u5668\u4eba",
        "\u5177\u8eab\u667a\u80fd", "\u90e8\u7f72", "\u4efb\u52a1\u6210\u529f\u7387",
        "\u6570\u636e\u95ed\u73af", "\u8bd5\u70b9",
        "technical", "algorithm", "hardware", "robotics", "embodied ai",
        "deployment", "task success", "data loop", "pilot",
    ),
    "competition_or_moat": (
        "\u7ade\u4e89", "\u62a4\u57ce\u6cb3", "\u4f18\u52bf", "\u51ed\u4ec0\u4e48",
        "\u66ff\u4ee3", "\u590d\u5236", "\u7f8e\u56e2", "\u997f\u4e86\u4e48",
        "compete", "competitor", "moat", "advantage", "defensibility",
        "replicate", "copy",
    ),
    "execution_evidence": (
        "\u8bc1\u636e", "\u9a8c\u8bc1", "\u6570\u636e", "\u8bbf\u8c08",
        "\u539f\u578b", "\u8bd5\u70b9", "\u7528\u6237",
        "evidence", "traction", "validation", "prototype", "pilot",
        "interview", "user test",
    ),
    "go_to_market": (
        "\u83b7\u5ba2", "\u6e20\u9053", "\u589e\u957f", "\u7559\u5b58",
        "cac", "\u5206\u53d1",
        "acquisition", "channel", "distribution", "cac", "retention", "growth",
    ),
    "funding_use": (
        "\u878d\u8d44", "\u94b1\u600e\u4e48\u82b1", "\u8d44\u91d1\u7528\u9014",
        "\u91cc\u7a0b\u7891", "\u9884\u7b97",
        "funding", "use of funds", "budget", "milestone", "runway",
    ),
    "problem_urgency": (
        "\u75db\u70b9", "\u7d27\u8feb", "\u4e3a\u4ec0\u4e48\u73b0\u5728",
        "\u5fc5\u987b\u89e3\u51b3", "\u4ed8\u8d39\u610f\u613f",
        "pain", "urgency", "why now", "must solve", "willingness to pay",
    ),
    "resilience_or_commitment": (
        "\u5931\u8d25", "\u575a\u6301", "\u653e\u5f03", "\u97e7\u6027", "\u627f\u8bfa",
        "resilience", "commitment", "fail", "failure", "persist",
    ),
    "founder_advantage": (
        "\u80cc\u666f", "\u7ecf\u5386", "\u4e3a\u4ec0\u4e48\u662f\u4f60",
        "\u521b\u59cb\u4eba", "\u9002\u5408",
        "founder", "background", "why you", "founder-market fit",
    ),
    "generic": (),
}

SCAFFOLD_EXTRA_BANK = {
    "en": {
        "technical_or_deeptech_validation": [
            [
                "Anchor the answer in one real deployment scenario, not the whole technology vision.",
                "Name the technical metric that proves the system works in that scenario.",
                "Separate lab performance from field performance.",
                "Explain how pilot data will create a learning loop.",
            ],
            [
                "Describe the task, environment, user, and failure mode you are validating.",
                "State the current technical bottleneck and what evidence would clear it.",
                "Explain what must be true before commercialization is realistic.",
                "Name the dataset, hardware iteration, or deployment signal you need next.",
            ],
        ],
        "competition_or_moat": [
            [
                "Name the strongest substitute or incumbent.",
                "Explain why your wedge is hard to copy in this specific use case.",
                "Show evidence that users care about your difference.",
                "State which advantage is still only a hypothesis.",
            ],
            [
                "Separate product differentiation from defensibility.",
                "Identify the data, workflow, access, or speed advantage you can compound.",
                "Explain why a larger player would not immediately prioritize this niche.",
                "Name the test that would prove the moat is real.",
            ],
        ],
        "execution_evidence": [
            [
                "Start with the strongest verified signal, not the aspiration.",
                "Distinguish user behavior from positive feedback.",
                "Name the pilot, prototype, interview, usage, or revenue evidence.",
                "State what evidence is still missing.",
            ],
            [
                "Tie each claim to a concrete observation.",
                "Explain who produced the signal and what they actually did.",
                "Avoid treating interest as validation unless behavior changed.",
                "Name the next validation step and success threshold.",
            ],
        ],
        "go_to_market": [
            [
                "Name the first reachable customer segment.",
                "Identify the channel you can access now.",
                "Explain why the channel fits the current stage.",
                "Define the first conversion or retention signal.",
            ],
            [
                "Avoid total market claims and describe the first repeatable path.",
                "Clarify the buyer, user, and adoption blocker.",
                "State the smallest go-to-market test you can run.",
                "Explain how you will learn from failed outreach.",
            ],
        ],
        "funding_use": [
            [
                "Map the funding ask to one or two milestones.",
                "Explain which risk the money reduces first.",
                "Separate product, validation, hiring, and go-to-market spend.",
                "State what evidence should exist before the next round.",
            ],
            [
                "Translate budget into time, experiments, and measurable outputs.",
                "Name what you will not spend on yet.",
                "Prioritize the riskiest assumption instead of listing every need.",
                "Define the next financing proof point.",
            ],
        ],
        "problem_urgency": [
            [
                "Name who feels the pain and when it becomes urgent.",
                "Show the cost of doing nothing.",
                "Separate curiosity from willingness to pay.",
                "Explain why the timing matters now.",
            ],
            [
                "Use one concrete workflow or decision moment.",
                "Explain the current workaround and why it breaks.",
                "Clarify whether the buyer is also the user.",
                "Name the signal that proves urgency.",
            ],
        ],
        "founder_advantage": [
            [
                "Connect your background to the specific insight behind this project.",
                "Name the access or capability you have that others lack.",
                "Show how your learning speed is different in this market.",
                "Tie founder-market fit to evidence, not identity alone.",
            ],
            [
                "Avoid a broad biography and focus on earned insight.",
                "Describe the moment you saw the problem differently.",
                "Explain what part of execution depends on your experience.",
                "Name the credibility signal investors should trust.",
            ],
        ],
        "resilience_or_commitment": [
            [
                "Name the hardest expected obstacle.",
                "Use one example of learning under pressure.",
                "Explain when you would persist and when you would change direction.",
                "Show commitment through behavior, not intent.",
            ],
            [
                "Describe the tradeoff you have already accepted.",
                "Explain how you react when evidence contradicts the plan.",
                "Name the operating habit that keeps execution stable.",
                "Avoid heroic language; use a concrete decision.",
            ],
        ],
        "generic": [
            [
                "Answer the investor's concern directly in one sentence.",
                "Add one concrete example or data point.",
                "Name the assumption your answer depends on.",
                "End with the next validation step.",
            ],
            [
                "Start with what is already known.",
                "Separate fact, interpretation, and next action.",
                "Name the biggest remaining uncertainty.",
                "Explain what evidence would change your mind.",
            ],
            [
                "Give the short answer first.",
                "Support it with one specific signal.",
                "Acknowledge the weakest part of the answer.",
                "State what you will test next.",
            ],
        ],
    },
    "zh": {
        "technical_or_deeptech_validation": [
            [
                "\u5148\u628a\u7b54\u6848\u843d\u5230\u4e00\u4e2a\u771f\u5b9e\u90e8\u7f72\u573a\u666f\uff0c\u4e0d\u8981\u53ea\u8bf4\u6280\u672f\u613f\u666f\u3002",
                "\u8bf4\u51fa\u80fd\u8bc1\u660e\u7cfb\u7edf\u5728\u8be5\u573a\u666f\u6709\u6548\u7684\u6280\u672f\u6307\u6807\u3002",
                "\u533a\u5206\u5b9e\u9a8c\u5ba4\u8868\u73b0\u548c\u73b0\u573a\u8868\u73b0\u3002",
                "\u89e3\u91ca\u8bd5\u70b9\u6570\u636e\u5982\u4f55\u5f62\u6210\u5b66\u4e60\u95ed\u73af\u3002",
            ],
            [
                "\u8bf4\u6e05\u6b63\u5728\u9a8c\u8bc1\u7684\u4efb\u52a1\u3001\u73af\u5883\u3001\u7528\u6237\u548c\u5931\u8d25\u6a21\u5f0f\u3002",
                "\u8bf4\u51fa\u5f53\u524d\u6700\u5173\u952e\u7684\u6280\u672f\u74f6\u9888\u548c\u9a8c\u8bc1\u8bc1\u636e\u3002",
                "\u89e3\u91ca\u8ddd\u79bb\u5546\u4e1a\u5316\u8fd8\u5fc5\u987b\u6210\u7acb\u7684\u6761\u4ef6\u3002",
                "\u8bf4\u51fa\u4e0b\u4e00\u6b65\u9700\u8981\u7684\u6570\u636e\u3001\u786c\u4ef6\u8fed\u4ee3\u6216\u90e8\u7f72\u4fe1\u53f7\u3002",
            ],
        ],
        "competition_or_moat": [
            [
                "\u8bf4\u51fa\u6700\u5f3a\u7684\u66ff\u4ee3\u65b9\u6848\u6216\u73b0\u6709\u73a9\u5bb6\u3002",
                "\u89e3\u91ca\u4f60\u7684\u5207\u5165\u70b9\u5728\u8fd9\u4e2a\u573a\u666f\u4e3a\u4ec0\u4e48\u96be\u4ee5\u590d\u5236\u3002",
                "\u7ed9\u51fa\u7528\u6237\u771f\u5728\u5728\u610f\u8fd9\u4e2a\u5dee\u5f02\u7684\u8bc1\u636e\u3002",
                "\u8bf4\u6e05\u54ea\u4e2a\u4f18\u52bf\u8fd8\u53ea\u662f\u5047\u8bbe\u3002",
            ],
            [
                "\u533a\u5206\u4ea7\u54c1\u5dee\u5f02\u548c\u53ef\u9632\u5fa1\u6027\u3002",
                "\u8bf4\u51fa\u53ef\u4ee5\u7d2f\u79ef\u7684\u6570\u636e\u3001\u6d41\u7a0b\u3001\u5165\u53e3\u6216\u901f\u5ea6\u4f18\u52bf\u3002",
                "\u89e3\u91ca\u5927\u73a9\u5bb6\u4e3a\u4ec0\u4e48\u4e0d\u4f1a\u7acb\u523b\u4f18\u5148\u505a\u8fd9\u4e2a\u7ec6\u5206\u573a\u666f\u3002",
                "\u8bf4\u51fa\u5982\u4f55\u9a8c\u8bc1\u62a4\u57ce\u6cb3\u771f\u5b9e\u5b58\u5728\u3002",
            ],
        ],
        "execution_evidence": [
            [
                "\u5148\u8bf4\u5df2\u7ecf\u88ab\u9a8c\u8bc1\u7684\u6700\u5f3a\u4fe1\u53f7\u3002",
                "\u533a\u5206\u7528\u6237\u884c\u4e3a\u548c\u53e3\u5934\u8ba4\u53ef\u3002",
                "\u5177\u4f53\u8bf4\u660e\u8bd5\u70b9\u3001\u539f\u578b\u3001\u8bbf\u8c08\u3001\u4f7f\u7528\u6216\u6536\u5165\u8bc1\u636e\u3002",
                "\u8bf4\u51fa\u8fd8\u7f3a\u54ea\u4e2a\u5173\u952e\u8bc1\u636e\u3002",
            ],
            [
                "\u628a\u6bcf\u4e2a\u5224\u65ad\u5bf9\u5e94\u5230\u4e00\u4e2a\u5177\u4f53\u89c2\u5bdf\u3002",
                "\u8bf4\u660e\u4fe1\u53f7\u6765\u81ea\u8c01\uff0c\u4ee5\u53ca\u5bf9\u65b9\u5b9e\u9645\u505a\u4e86\u4ec0\u4e48\u3002",
                "\u4e0d\u8981\u628a\u5174\u8da3\u5f53\u6210\u9a8c\u8bc1\uff0c\u9664\u975e\u884c\u4e3a\u771f\u7684\u53d8\u4e86\u3002",
                "\u8bf4\u51fa\u4e0b\u4e00\u6b65\u9a8c\u8bc1\u548c\u6210\u529f\u6807\u51c6\u3002",
            ],
        ],
        "go_to_market": [
            [
                "\u8bf4\u51fa\u7b2c\u4e00\u4e2a\u80fd\u89e6\u8fbe\u7684\u5ba2\u6237\u7fa4\u3002",
                "\u6307\u51fa\u73b0\u5728\u5c31\u80fd\u4f7f\u7528\u7684\u6e20\u9053\u3002",
                "\u89e3\u91ca\u8fd9\u4e2a\u6e20\u9053\u4e3a\u4ec0\u4e48\u9002\u5408\u5f53\u524d\u9636\u6bb5\u3002",
                "\u5b9a\u4e49\u7b2c\u4e00\u4e2a\u8f6c\u5316\u6216\u7559\u5b58\u4fe1\u53f7\u3002",
            ],
            [
                "\u4e0d\u8981\u8bf4\u603b\u5e02\u573a\uff0c\u8bf4\u7b2c\u4e00\u6761\u53ef\u91cd\u590d\u8def\u5f84\u3002",
                "\u8bf4\u6e05\u4e70\u5355\u8005\u3001\u4f7f\u7528\u8005\u548c\u91c7\u7528\u963b\u529b\u3002",
                "\u8bf4\u51fa\u53ef\u4ee5\u8dd1\u7684\u6700\u5c0f\u5e02\u573a\u8bd5\u9a8c\u3002",
                "\u89e3\u91ca\u5982\u4f55\u4ece\u5931\u8d25\u7684\u5916\u8054\u4e2d\u5b66\u4e60\u3002",
            ],
        ],
        "funding_use": [
            [
                "\u628a\u878d\u8d44\u9700\u6c42\u5bf9\u5e94\u5230\u4e00\u4e24\u4e2a\u91cc\u7a0b\u7891\u3002",
                "\u8bf4\u660e\u8fd9\u7b14\u94b1\u9996\u5148\u964d\u4f4e\u54ea\u4e2a\u98ce\u9669\u3002",
                "\u533a\u5206\u4ea7\u54c1\u3001\u9a8c\u8bc1\u3001\u62db\u8058\u548c\u5e02\u573a\u8fdb\u5165\u7528\u9014\u3002",
                "\u8bf4\u6e05\u4e0b\u4e00\u8f6e\u524d\u5e94\u8be5\u6709\u4ec0\u4e48\u8bc1\u636e\u3002",
            ],
            [
                "\u628a\u9884\u7b97\u7ffb\u8bd1\u6210\u65f6\u95f4\u3001\u5b9e\u9a8c\u548c\u53ef\u8861\u91cf\u4ea7\u51fa\u3002",
                "\u8bf4\u51fa\u73b0\u9636\u6bb5\u4e0d\u4f1a\u628a\u94b1\u82b1\u5728\u54ea\u91cc\u3002",
                "\u4f18\u5148\u964d\u4f4e\u6700\u5371\u9669\u7684\u5047\u8bbe\uff0c\u4e0d\u8981\u7f57\u5217\u6240\u6709\u9700\u6c42\u3002",
                "\u5b9a\u4e49\u4e0b\u4e00\u4e2a\u878d\u8d44\u8bc1\u636e\u70b9\u3002",
            ],
        ],
        "problem_urgency": [
            [
                "\u8bf4\u51fa\u8c01\u6709\u75db\u70b9\uff0c\u4ee5\u53ca\u4ec0\u4e48\u65f6\u5019\u53d8\u5f97\u7d27\u8feb\u3002",
                "\u8bf4\u660e\u4e0d\u89e3\u51b3\u4f1a\u9020\u6210\u4ec0\u4e48\u4ee3\u4ef7\u3002",
                "\u533a\u5206\u597d\u5947\u548c\u4ed8\u8d39\u610f\u613f\u3002",
                "\u89e3\u91ca\u4e3a\u4ec0\u4e48\u65f6\u95f4\u70b9\u662f\u73b0\u5728\u3002",
            ],
            [
                "\u7528\u4e00\u4e2a\u5177\u4f53\u6d41\u7a0b\u6216\u51b3\u7b56\u65f6\u523b\u8bf4\u660e\u3002",
                "\u89e3\u91ca\u73b0\u6709\u66ff\u4ee3\u65b9\u6848\u4e3a\u4ec0\u4e48\u5931\u6548\u3002",
                "\u8bf4\u6e05\u4e70\u5355\u8005\u662f\u5426\u4e5f\u662f\u4f7f\u7528\u8005\u3002",
                "\u8bf4\u51fa\u54ea\u4e2a\u4fe1\u53f7\u80fd\u8bc1\u660e\u7d27\u8feb\u6027\u3002",
            ],
        ],
        "founder_advantage": [
            [
                "\u628a\u4f60\u7684\u80cc\u666f\u548c\u9879\u76ee\u80cc\u540e\u7684\u5177\u4f53\u6d1e\u5bdf\u8fde\u8d77\u6765\u3002",
                "\u8bf4\u51fa\u4f60\u62e5\u6709\u800c\u522b\u4eba\u7f3a\u5c11\u7684\u5165\u53e3\u6216\u80fd\u529b\u3002",
                "\u8bf4\u660e\u4f60\u5728\u8fd9\u4e2a\u5e02\u573a\u4e2d\u7684\u5b66\u4e60\u901f\u5ea6\u6709\u4ec0\u4e48\u4e0d\u540c\u3002",
                "\u628a\u521b\u59cb\u4eba\u5339\u914d\u5ea6\u843d\u5230\u8bc1\u636e\u4e0a\u3002",
            ],
            [
                "\u4e0d\u8981\u5199\u6cdb\u6cdb\u5c65\u5386\uff0c\u8981\u805a\u7126\u771f\u5b9e\u6d1e\u5bdf\u3002",
                "\u63cf\u8ff0\u4f60\u4ec0\u4e48\u65f6\u5019\u7528\u4e0d\u540c\u65b9\u5f0f\u770b\u5230\u8fd9\u4e2a\u95ee\u9898\u3002",
                "\u89e3\u91ca\u6267\u884c\u4e2d\u54ea\u4e2a\u90e8\u5206\u4f9d\u8d56\u4f60\u7684\u7ecf\u9a8c\u3002",
                "\u8bf4\u51fa\u6295\u8d44\u4eba\u5e94\u8be5\u76f8\u4fe1\u7684\u53ef\u4fe1\u53f7\u3002",
            ],
        ],
        "resilience_or_commitment": [
            [
                "\u8bf4\u51fa\u9884\u671f\u6700\u96be\u7684\u969c\u788d\u3002",
                "\u7528\u4e00\u4e2a\u5728\u538b\u529b\u4e0b\u5b66\u4e60\u7684\u4f8b\u5b50\u3002",
                "\u89e3\u91ca\u4ec0\u4e48\u65f6\u5019\u575a\u6301\uff0c\u4ec0\u4e48\u65f6\u5019\u8c03\u6574\u65b9\u5411\u3002",
                "\u7528\u884c\u4e3a\u8bc1\u660e\u6295\u5165\uff0c\u4e0d\u662f\u53ea\u8868\u8fbe\u610f\u56fe\u3002",
            ],
            [
                "\u8bf4\u660e\u4f60\u5df2\u7ecf\u63a5\u53d7\u7684\u53d6\u820d\u3002",
                "\u89e3\u91ca\u5f53\u8bc1\u636e\u548c\u8ba1\u5212\u51b2\u7a81\u65f6\u4f60\u5982\u4f55\u53cd\u5e94\u3002",
                "\u8bf4\u51fa\u4fdd\u6301\u6267\u884c\u7a33\u5b9a\u7684\u4e60\u60ef\u3002",
                "\u907f\u514d\u82f1\u96c4\u5316\u8868\u8ff0\uff0c\u7528\u5177\u4f53\u51b3\u5b9a\u8bf4\u660e\u3002",
            ],
        ],
        "generic": [
            [
                "\u7528\u4e00\u53e5\u8bdd\u76f4\u63a5\u56de\u7b54\u6295\u8d44\u4eba\u7684\u62c5\u5fc3\u3002",
                "\u8865\u5145\u4e00\u4e2a\u5177\u4f53\u4f8b\u5b50\u6216\u6570\u636e\u70b9\u3002",
                "\u8bf4\u51fa\u8fd9\u4e2a\u7b54\u6848\u4f9d\u8d56\u7684\u5047\u8bbe\u3002",
                "\u4ee5\u4e0b\u4e00\u6b65\u9a8c\u8bc1\u7ed3\u5c3e\u3002",
            ],
            [
                "\u5148\u8bf4\u5df2\u7ecf\u77e5\u9053\u7684\u4e8b\u5b9e\u3002",
                "\u533a\u5206\u4e8b\u5b9e\u3001\u89e3\u8bfb\u548c\u4e0b\u4e00\u6b65\u884c\u52a8\u3002",
                "\u8bf4\u51fa\u6700\u5927\u7684\u672a\u77e5\u95ee\u9898\u3002",
                "\u89e3\u91ca\u4ec0\u4e48\u8bc1\u636e\u4f1a\u6539\u53d8\u4f60\u7684\u5224\u65ad\u3002",
            ],
            [
                "\u5148\u7ed9\u51fa\u7b80\u77ed\u7b54\u6848\u3002",
                "\u7528\u4e00\u4e2a\u5177\u4f53\u4fe1\u53f7\u652f\u6491\u5b83\u3002",
                "\u627f\u8ba4\u7b54\u6848\u91cc\u6700\u8584\u5f31\u7684\u90e8\u5206\u3002",
                "\u8bf4\u51fa\u63a5\u4e0b\u6765\u8981\u9a8c\u8bc1\u4ec0\u4e48\u3002",
            ],
        ],
    },
}


def classify_question_for_scaffold(question_text: str) -> str:
    text = str(question_text).lower()
    for category in SCAFFOLD_EXTRA_CATEGORY_PRIORITY:
        if category == "generic":
            continue
        keywords = SCAFFOLD_EXTRA_KEYWORDS.get(category, ())
        if any(keyword.lower() in text for keyword in keywords):
            return category

    for category in SCAFFOLD_CATEGORY_PRIORITY:
        if category == "generic":
            continue
        keywords = SCAFFOLD_KEYWORDS.get(category, ())
        if any(keyword.lower() in text for keyword in keywords):
            return category
    return "generic"


def get_answer_scaffold(
    question_text: str,
    language: str,
    question_index: int = 0,
) -> list[str]:
    safe_language = language if language in SCAFFOLD_EXTRA_BANK else "en"
    category = classify_question_for_scaffold(question_text)
    extra_language_bank = SCAFFOLD_EXTRA_BANK[safe_language]
    base_language_bank = SCAFFOLD_BANK.get(safe_language, SCAFFOLD_BANK["en"])
    variants = (
        extra_language_bank.get(category)
        or base_language_bank.get(category)
        or extra_language_bank["generic"]
    )
    variant_index = question_index % len(variants)
    selected_variant = variants[variant_index]

    deduped_scaffold = []
    seen_lines = set()
    for item in selected_variant:
        normalized_item = re.sub(r"\s+", " ", item.strip().lower())
        if not normalized_item or normalized_item in seen_lines:
            continue
        seen_lines.add(normalized_item)
        deduped_scaffold.append(item)
        if len(deduped_scaffold) >= 5:
            break

    return deduped_scaffold or extra_language_bank["generic"][
        question_index % len(extra_language_bank["generic"])
    ]


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

    .vc-report-dashboard {
        width: min(calc(100vw - 3rem), 1120px);
        max-width: 1120px;
        margin: 0 auto;
        border: 1px solid rgba(214, 179, 106, 0.24);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(18, 34, 56, 0.96), rgba(15, 27, 45, 0.98));
        box-shadow: 0 22px 42px rgba(0, 0, 0, 0.22);
        overflow: hidden;
    }

    .vc-report-dashboard-header {
        padding: 1.15rem 1.15rem 0.95rem 1.15rem;
        border-bottom: 1px solid var(--vc-border);
    }

    .vc-report-dashboard-title {
        margin: 0;
        color: var(--vc-text);
        font-size: 1.12rem;
        font-weight: 760;
        letter-spacing: 0;
        line-height: 1.3;
    }

    .vc-report-dashboard-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr);
        gap: 0.9rem;
        padding: 1rem 1.1rem 1.1rem 1.1rem;
        background: rgba(8, 17, 31, 0.18);
    }

    .vc-report-insight-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.9rem;
    }

    .vc-report-card {
        border: 1px solid rgba(34, 50, 74, 0.95);
        border-radius: 8px;
        background: rgba(8, 17, 31, 0.38);
        box-shadow: 0 14px 26px rgba(0, 0, 0, 0.18);
        padding: 1rem;
        min-width: 0;
    }

    .vc-report-card-primary {
        border-color: rgba(79, 124, 255, 0.38);
    }

    .vc-report-card-critical {
        border-color: rgba(214, 179, 106, 0.36);
    }

    .vc-report-card-strength {
        border-color: rgba(100, 140, 255, 0.34);
    }

    .vc-report-card-title {
        margin: 0 0 0.65rem 0;
        color: #f7f1e4;
        font-size: 0.95rem;
        font-weight: 760;
        line-height: 1.3;
        letter-spacing: 0;
    }

    .vc-report-card-body {
        color: #d9e0eb;
        font-size: 0.93rem;
        line-height: 1.72;
        overflow-wrap: anywhere;
    }

    .vc-report-card-body p {
        margin: 0 0 0.7rem 0;
    }

    .vc-report-card-body p:last-child {
        margin-bottom: 0;
    }

    .vc-report-card-body ul,
    .vc-report-card-body ol {
        margin: 0 0 0.8rem 1.15rem;
        padding: 0;
    }

    .vc-report-card-body li {
        margin: 0 0 0.45rem 0;
    }

    .vc-report-card-body strong {
        color: #f7f1e4;
        font-weight: 720;
    }

    .vc-report-text-line,
    .vc-report-list-line {
        margin: 0 0 0.5rem 0;
    }

    .vc-report-list-line {
        padding-left: 0.15rem;
    }

    .vc-report-score-rows {
        display: grid;
        gap: 0.55rem;
    }

    .vc-report-score-row {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 0.75rem;
        align-items: center;
        padding: 0.55rem 0.65rem;
        border: 1px solid rgba(34, 50, 74, 0.75);
        border-radius: 8px;
        background: rgba(15, 27, 45, 0.58);
    }

    .vc-report-score-label {
        color: #d9e0eb;
        min-width: 0;
    }

    .vc-report-score-value {
        color: #f7f1e4;
        font-weight: 760;
        white-space: nowrap;
    }

    .vc-report-score-note {
        grid-column: 1 / -1;
        color: var(--vc-muted);
        font-size: 0.86rem;
        line-height: 1.55;
    }

    @media (max-width: 760px) {
        .vc-report-dashboard {
            width: min(calc(100vw - 1.5rem), 1120px);
        }

        .vc-report-insight-grid {
            grid-template-columns: minmax(0, 1fr);
        }
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
sidebar_context = current_assessment_context()
completed_fields = sum(
    1 for key in FOUNDER_PROFILE_FIELDS if str(sidebar_profile.get(key, "")).strip()
)
profile_ready = profile_is_complete(st.session_state.founder_profile)

assessment_context_labels = {
    "project_sector": t["project_sector_label"],
    "current_stage": t["current_stage_label"],
    "evaluation_goal": t["evaluation_goal_label"],
    "commercialization_horizon": t["commercialization_horizon_label"],
}


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

    st.caption(t["assessment_context_title"])
    for context_key in ASSESSMENT_CONTEXT_FIELDS:
        context_value = sidebar_context.get(context_key, "")
        display_value = (
            assessment_context_label(context_key, context_value, language)
            if context_value else t["context_not_set"]
        )
        st.caption(f"{assessment_context_labels[context_key]}: {display_value}")

    if st.button(t["btn_edit_dossier"], use_container_width=True):
        st.session_state.flow_step = "profile"
        st.rerun()

    if st.button(t["btn_new_session"], use_container_width=True):
        reset_guided_session_state()
        st.rerun()


generate_questions_clicked = False

if st.session_state.flow_step == "profile":
    context_value_to_index = {
        field_key: {
            value: index
            for index, value in enumerate(assessment_context_option_values(field_key))
        }
        for field_key in ASSESSMENT_CONTEXT_FIELDS
    }
    current_context = current_assessment_context()
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
    project_sector = st.selectbox(
        t["project_sector_label"],
        options=assessment_context_option_values("project_sector"),
        index=context_value_to_index["project_sector"].get(current_context["project_sector"], 0),
        format_func=lambda code: assessment_context_label("project_sector", code, language),
    )
    current_stage = st.selectbox(
        t["current_stage_label"],
        options=assessment_context_option_values("current_stage"),
        index=context_value_to_index["current_stage"].get(current_context["current_stage"], 0),
        format_func=lambda code: assessment_context_label("current_stage", code, language),
    )
    evaluation_goal = st.selectbox(
        t["evaluation_goal_label"],
        options=assessment_context_option_values("evaluation_goal"),
        index=context_value_to_index["evaluation_goal"].get(current_context["evaluation_goal"], 0),
        format_func=lambda code: assessment_context_label("evaluation_goal", code, language),
    )
    commercialization_horizon = st.selectbox(
        t["commercialization_horizon_label"],
        options=assessment_context_option_values("commercialization_horizon"),
        index=context_value_to_index["commercialization_horizon"].get(current_context["commercialization_horizon"], 0),
        format_func=lambda code: assessment_context_label("commercialization_horizon", code, language),
    )
    build_dossier_clicked = st.button(
        t["btn_build_dossier"], type="primary", use_container_width=True
    )
    st.markdown("</div></div>", unsafe_allow_html=True)

    if build_dossier_clicked:
        if not inputs_ready():
            st.warning(t["warn_build_dossier"])
        else:
            st.session_state.assessment_context = {
                "project_sector": project_sector,
                "current_stage": current_stage,
                "evaluation_goal": evaluation_goal,
                "commercialization_horizon": commercialization_horizon,
            }
            st.session_state.founder_profile = current_founder_profile()
            st.session_state.founder_profile.update(st.session_state.assessment_context)
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
                context = current_assessment_context()
                base_prompt = QUESTION_PROMPT.format(
                    founder_background=profile["founder_background"],
                    project_description=profile["project_description"],
                    current_evidence=profile["current_evidence"],
                    funding_goal=profile["funding_goal"],
                    language_instruction=t["language_instruction"],
                )
                assessment_context_block = build_assessment_context_prompt_block(
                    context,
                    language,
                )
                evaluation_lens_block = build_evaluation_lens(context, language)
                prompt = "\n\n".join(
                    block
                    for block in (
                        assessment_context_block,
                        evaluation_lens_block,
                        base_prompt,
                    )
                    if block
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
        for scaffold_item in get_answer_scaffold(current_question, language, current_index):
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
                base_report_prompt = report_template.format(
                    founder_background=founder_profile.get("founder_background", st.session_state.founder_background),
                    project_description=founder_profile.get("project_description", st.session_state.project_description),
                    current_evidence=founder_profile.get("current_evidence", st.session_state.current_evidence),
                    funding_goal=founder_profile.get("funding_goal", st.session_state.funding_goal),
                    qa_transcript=qa_transcript,
                )
                context = current_assessment_context()
                assessment_context_block = build_assessment_context_prompt_block(
                    context,
                    language,
                )
                report_evaluation_lens_block = build_report_evaluation_lens(
                    context,
                    language,
                )
                prompt = "\n\n".join(
                    block
                    for block in (
                        assessment_context_block,
                        report_evaluation_lens_block,
                        base_report_prompt,
                    )
                    if block
                )

                update_report_progress(65, t["report_progress_calling_model"], delay=0.3)
                raw_report = call_model(prompt)
                report_markdown = ensure_report_has_assessment_lens(
                    raw_report,
                    context,
                    language,
                )

                update_report_progress(85, t["report_progress_parsing_structure"], delay=0.18)
                st.session_state.report_markdown = report_markdown
                st.session_state.report_json = safe_parse_report_json(report_markdown)
                st.session_state.report_sections = parse_report_markdown_sections(report_markdown)

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
                    base_report_prompt = report_template.format(
                        founder_background=st.session_state.founder_background,
                        project_description=st.session_state.project_description,
                        current_evidence=st.session_state.current_evidence,
                        funding_goal=st.session_state.funding_goal,
                        qa_transcript=qa_transcript,
                    )
                    context = current_assessment_context()
                    assessment_context_block = build_assessment_context_prompt_block(
                        context,
                        language,
                    )
                    report_evaluation_lens_block = build_report_evaluation_lens(
                        context,
                        language,
                    )
                    prompt = "\n\n".join(
                        block
                        for block in (
                            assessment_context_block,
                            report_evaluation_lens_block,
                            base_report_prompt,
                        )
                        if block
                    )
                    raw_report = call_model(prompt)
                    st.session_state.report_markdown = ensure_report_has_assessment_lens(
                        raw_report,
                        context,
                        language,
                    )
                    st.session_state.flow_step = "report_ready"
                except Exception as e:
                    st.error(f"{t['err_report']}{e}")


# ---------- Step 3: render report + download ----------

if st.session_state.flow_step == "report_ready" and st.session_state.report_markdown:
    render_report_dashboard(
        st.session_state.report_markdown,
        st.session_state.report_sections,
        t,
        language,
    )

    st.download_button(
        label=t["btn_download"],
        data=st.session_state.report_markdown,
        file_name="vcready_founder_reflection_report.txt",
        mime="text/plain",
    )

st.divider()
st.caption(t["footer"])
