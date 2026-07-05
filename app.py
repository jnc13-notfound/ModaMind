from agents.agent_chat import chat_with_agent as chat_with_agent_backend
import gradio as gr
from main import run_pipeline
from utils.config import AVAILABLE_MODELS


# ============================================================
# FUNCTION 1: Run the full pipeline
# ============================================================

def run_modamind(brand_name, category, campaign_name,
                 competitors_text, target_audience, selected_model_name):

    if not brand_name.strip():
        yield "Please enter a brand name.", "", None, {}, {}, {}, {}, {}, {}, {}, {}
        return

    # Competitors are now truly optional
    competitors = [c.strip() for c in competitors_text.split(",") if c.strip()]

    # Resolve model name from display label to actual model string
    selected_model = AVAILABLE_MODELS.get(selected_model_name)

    status = f"Starting ModaMind pipeline...\nModel: {selected_model_name}\n\n"
    yield status, "", None, {}, {}, {}, {}, {}, {}, {}, {}

    try:
        status += "Running 8 AI agents — this takes 2–3 minutes.\n\n"
        status += "Trend Scout  →  Brand Analyst  →  Ethics Auditor\n"
        status += "Consumer Psychology  →  Influencer Matcher\n"
        status += "Synthesis  →  Critic  →  Content  →  Report\n"
        yield status, "", None, {}, {}, {}, {}, {}, {}, {}, {}

        result = run_pipeline(
            brand_name=brand_name,
            category=category,
            campaign_name=campaign_name,
            competitors=competitors,
            target_audience=target_audience,
            selected_model=selected_model
        )

        status += f"\nComplete  —  Quality Score: {result['critic'].get('score', 'N/A')}/10"

        yield (
            status,
            result['report'],
            result,
            result['trends'],
            result['brand_analysis'],
            result['ethics'],
            result['psychology'],
            result['influencers'],
            result['synthesis'],
            result['critic'],
            result['content']
        )

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            status += "\n\nQuota exceeded on this model.\nPlease select a different model from the dropdown and try again."
        else:
            status += f"\nError: {error_msg}"
        yield status, "", None, {}, {}, {}, {}, {}, {}, {}, {}


# ============================================================
# FUNCTION 2: Answer a question about the full report
# ============================================================

def answer_followup_question(question, report_text, selected_model_name):
    from utils.config import client
    model = AVAILABLE_MODELS.get(selected_model_name, "models/gemini-flash-latest")

    if not report_text.strip():
        return "Please generate a report first."
    if not question.strip():
        return "Please type a question."

    prompt = f"""
You are ModaMind's analyst. A user has a brand intelligence report and is asking 
a follow-up question. Answer using ONLY information from the report below.
Be specific and concise.

REPORT:
{report_text}

QUESTION: {question}
"""
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "Model quota exceeded. Please select a different model from the dropdown and try again."
        return f"Error: {str(e)}"


# ============================================================
# FUNCTION 3: Chat with a specific agent
# ============================================================

def chat_with_agent(agent_name, message, chat_history,
                    pipeline_state, selected_model_name):

    if not message.strip():
        return chat_history, ""

    if chat_history is None:
        chat_history = []

    if pipeline_state is None:
        return chat_history + [
            [message, "Please run the full pipeline first (Generate Report tab), then return here to chat."]
        ], ""

    # Override model if user changed it
    selected_model = AVAILABLE_MODELS.get(selected_model_name)
    if selected_model:
        import utils.config as cfg
        cfg.MODEL = selected_model

    history_as_dicts = []
    for turn in chat_history:
        if turn[0]:
            history_as_dicts.append({"role": "user", "content": turn[0]})
        if turn[1]:
            history_as_dicts.append({"role": "assistant", "content": turn[1]})

    try:
        response_text = chat_with_agent_backend(
            agent_name, message, history_as_dicts, pipeline_state
        )
    except Exception as e:
        if "429" in str(e):
            response_text = "This model's quota is exhausted. Please select a different model from the dropdown above and resend your message."
        else:
            response_text = f"Error: {str(e)}"

    chat_history = chat_history + [[message, response_text]]
    return chat_history, ""


# ============================================================
# CSS — Full desktop layout, Stripe nav feel, cream + charcoal
# ============================================================

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.gradio-container {
    background-color: #faf9f7 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    color: #1a1a1a !important;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    min-height: 100vh !important;
}

/* ── Navbar ───────────────────────────────────────── */
.mm-navbar {
    width: 100% !important;
    background-color: #faf9f7 !important;
    border-bottom: 2px solid #1a1a1a !important;
    padding: 0 4rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    height: 72px !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
}

/* ─────────────────────────────────────────────── */
/* MODAMIND LOGO */
/* ─────────────────────────────────────────────── */

.mm-logo,
.mm-logo .prose,
.mm-logo .prose *,
.mm-logo p,
.mm-logo strong{
    font-family:'Cormorant Garamond', Georgia, serif !important;
    font-size:1.8rem !important;
    font-weight:700 !important;
    letter-spacing:.20em !important;
    text-transform:uppercase !important;
    color:#1a1a1a !important;
    line-height:1 !important;
    margin:0 !important;
}
/* ─────────────────────────────────────────────── */
/* TAGLINE */
/* ─────────────────────────────────────────────── */

.mm-tagline,
.mm-tagline .prose,
.mm-tagline .prose *,
.mm-tagline p{
    font-family:'Inter',sans-serif !important;
    font-size:.72rem !important;
    font-weight:700 !important;
    letter-spacing:.30em !important;
    text-transform:uppercase !important;
    color:#1a1a1a !important;
    line-height:1.3 !important;
    margin:0 !important;
}

/* ── Main content ─────────────────────────────────── */
.mm-content {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 3rem 4rem !important;
    width: 100% !important;
}

/* ── Tabs — always dark and visible ───────────────── */
/* Modern Gradio Tabs */

button[role="tab"]{
    color:#1a1a1a !important;
    opacity:1 !important;
    font-weight:700 !important;
    text-transform:uppercase !important;
    letter-spacing:.12em !important;
}

button[role="tab"]:hover{
    color:#1a1a1a !important;
}

button[role="tab"][aria-selected="true"]{
    color:#1a1a1a !important;
    border-bottom:3px solid #1a1a1a !important;
    font-weight:700 !important;
}

button[role="tab"][aria-selected="false"]{
    color:#1a1a1a !important;
    opacity:1 !important;
}

/* ─────────────────────────────────────────────── */
/* SECTION HEADINGS */
/* ─────────────────────────────────────────────── */

.section-title,
.section-title .prose,
.section-title .prose *,
.section-title h1,
.section-title h2,
.section-title h3,
.section-title p{
    font-family:'Cormorant Garamond', Georgia, serif !important;
    font-size:2.2rem !important;
    font-weight:700 !important;
    color:#1a1a1a !important;
    line-height:1.2 !important;
    letter-spacing:.03em !important;
    margin:0 0 .4rem 0 !important;
}

/* ── Section subtitles ────────────────────────────── */
.section-subtitle p, .section-subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    color: #4a4540 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 2rem !important;
    line-height: 1.65 !important;
}

/* ── Form Labels — dark, always readable ──────────── */
label, .label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #1a1a1a !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
}

/* ── Input fields ─────────────────────────────────── */
input[type="text"], textarea {
    width: 100% !important;
    background-color: #ffffff !important;
    border: 1.5px solid #c4bfb8 !important;
    border-radius: 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.92rem !important;
    color: #1a1a1a !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.15s ease !important;
    outline: none !important;
}

input[type="text"]:focus, textarea:focus {
    border-color: #1a1a1a !important;
    box-shadow: none !important;
}

input::placeholder, textarea::placeholder {
    color: #a09890 !important;
    font-weight: 400 !important;
}

/* ── Buttons ──────────────────────────────────────── */
button.primary {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    background-color: #1a1a1a !important;
    color: #faf9f7 !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 3px !important;
    padding: 0.9rem 2rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

button.primary:hover {
    background-color: #faf9f7 !important;
    color: #1a1a1a !important;
}

button.secondary {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    background-color: transparent !important;
    color: #1a1a1a !important;
    border: 1.5px solid #4a4540 !important;
    border-radius: 3px !important;
    padding: 0.9rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

button.secondary:hover {
    border-color: #1a1a1a !important;
}

/* ── Model selector ───────────────────────────────── */
.model-selector label {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

.model-selector select {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    background-color: #ffffff !important;
    border: 1.5px solid #c4bfb8 !important;
    border-radius: 3px !important;
    color: #1a1a1a !important;
    padding: 0.5rem 1rem !important;
}

/* ── Status box ───────────────────────────────────── */
.status-box label {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

.status-box textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    color: #1a1a1a !important;
    line-height: 1.9 !important;
    background-color: #f0ede8 !important;
    border: 1.5px solid #c4bfb8 !important;
    border-radius: 3px !important;
    padding: 1rem !important;
}

/* ── Report markdown ──────────────────────────────── */
.report-area {
    padding: 2rem 0 !important;
}

.report-area h1 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 2rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    color: #1a1a1a !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid #1a1a1a !important;
    padding-bottom: 0.75rem !important;
    margin-top: 0 !important;
}

.report-area h2 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.5rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    color: #1a1a1a !important;
    border-bottom: 1px solid #c4bfb8 !important;
    padding-bottom: 0.5rem !important;
    margin-top: 2.5rem !important;
    text-transform: uppercase !important;
}

.report-area h3 {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #4a4540 !important;
    margin-top: 1.5rem !important;
}

.report-area p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 400 !important;
    line-height: 1.85 !important;
    color: #2a2520 !important;
    margin-bottom: 1rem !important;
}

.report-area li {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 400 !important;
    line-height: 1.85 !important;
    color: #2a2520 !important;
    margin-bottom: 0.4rem !important;
}

.report-area strong {
    font-weight: 700 !important;
    color: #1a1a1a !important;
}

/* ── Accordion labels ─────────────────────────────── */
.accordion .label-wrap, details summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #1a1a1a !important;
    padding: 1.2rem 0 !important;
    background: transparent !important;
    cursor: pointer !important;
}

.accordion, details {
    border: none !important;
    border-bottom: 1px solid #c4bfb8 !important;
    border-radius: 0 !important;
    background: transparent !important;
}

/* ── Chatbot ──────────────────────────────────────── */
.chatbot-area .bot.message {
    background-color: #ede9e3 !important;
    border-radius: 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    color: #1a1a1a !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
}

.chatbot-area .user.message {
    background-color: #1a1a1a !important;
    color: #faf9f7 !important;
    border-radius: 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    padding: 1rem 1.2rem !important;
}

/* ── Chatbot black box fix ────────────────────────── */
.chatbot-area, .chatbot-area > div {
    background-color: #faf9f7 !important;
    border: 1.5px solid #c4bfb8 !important;
    border-radius: 3px !important;
}

/* ── HR dividers ──────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid #c4bfb8 !important;
    margin: 2.5rem 0 !important;
}

/* ── Hide Gradio footer ───────────────────────────── */
footer { display: none !important; }
.built-with { display: none !important; }

/* ── Remove default box styles ────────────────────── */
.block, .panel, .form {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
}

/* ── JSON display ─────────────────────────────────── */
.json-holder {
    font-family: 'Inter', monospace !important;
    font-size: 0.8rem !important;
    color: #1a1a1a !important;
    background-color: #f0ede8 !important;
    border: 1px solid #c4bfb8 !important;
    border-radius: 3px !important;
    padding: 1rem !important;
}

/* ── Dropdown text ────────────────────────────────── */
.svelte-1gfkn6j, span, p {
    color: #1a1a1a !important;
}
"""

# ============================================================
# UI LAYOUT
# ============================================================

with gr.Blocks(
    title="ModaMind",
    css=custom_css,
    theme=gr.themes.Default(
        primary_hue="orange",
        neutral_hue="stone"
    )
) as app:

    # ── Top Navigation Bar ────────────────────────────────────
    with gr.Row(elem_classes="mm-navbar"):
        with gr.Column(scale=3):
            gr.Markdown("**MODAMIND**", elem_classes="mm-logo")
            gr.Markdown(
                "Multi-Agent Fashion Brand Intelligence",
                elem_classes="mm-tagline"
            )
        with gr.Column(scale=1):
            # Model selector — always visible in the navbar
            # so users can switch models the moment quota hits
            model_selector = gr.Dropdown(
                choices=list(AVAILABLE_MODELS.keys()),
                value="Gemini Flash (Latest)",
                label="Model",
                elem_classes="model-selector",
                container=True
            )

    # State — holds full pipeline result across all tabs
    pipeline_state = gr.State(value=None)

    # ── Main Content ──────────────────────────────────────────
    with gr.Column(elem_classes="mm-content"):

        with gr.Tabs():

            # ── TAB 1: GENERATE REPORT ────────────────────────
            with gr.Tab("Generate Report"):

                gr.Markdown("### Brand Intelligence", elem_classes="section-title")
                gr.Markdown(
                    "Enter the brand you want to analyze. "
                    "Competitors are optional — if left blank, agents will research them automatically.",
                    elem_classes="section-subtitle"
                )

                with gr.Row():

                    # Left column — inputs
                    with gr.Column(scale=2):
                        with gr.Row():
                            brand_input = gr.Textbox(
                                label="Brand Name",
                                placeholder="Nike",
                                scale=1
                            )
                            category_input = gr.Textbox(
                                label="Category",
                                placeholder="Sportswear",
                                scale=1
                            )

                        campaign_input = gr.Textbox(
                            label="Campaign to Analyze",
                            placeholder="Just Do It 2024 — leave blank if unknown"
                        )

                        with gr.Row():
                            competitors_input = gr.Textbox(
                                label="Competitors  (optional — agents will auto-research if blank)",
                                placeholder="Adidas, Puma, New Balance",
                                scale=2
                            )
                            audience_input = gr.Textbox(
                                label="Target Audience",
                                placeholder="Gen Z fitness enthusiasts in India",
                                scale=2
                            )

                        run_btn = gr.Button(
                            "Run ModaMind Pipeline",
                            variant="primary"
                        )

                    # Right column — status
                    with gr.Column(scale=1):
                        status_output = gr.Textbox(
                            label="Pipeline Status",
                            lines=12,
                            elem_classes="status-box",
                            interactive=False
                        )

                gr.Markdown("---")
                report_output = gr.Markdown(
                    value="*Your brand intelligence report will appear here after running the pipeline.*",
                    elem_classes="report-area"
                )

            # ── TAB 2: AGENT BREAKDOWN ────────────────────────
            with gr.Tab("Agent Breakdown"):

                gr.Markdown("### Individual Agent Findings", elem_classes="section-title")
                gr.Markdown(
                    "Run the pipeline first, then expand any agent below "
                    "to inspect its raw findings before synthesis.",
                    elem_classes="section-subtitle"
                )

                with gr.Accordion("Trend Scout — Emerging market signals", open=False):
                    trend_display = gr.JSON()

                with gr.Accordion("Brand Analyst — Positioning & competitive gaps", open=False):
                    brand_display = gr.JSON()

                with gr.Accordion("Ethics Auditor — Sustainability claim verification", open=False):
                    ethics_display = gr.JSON()

                with gr.Accordion("Consumer Psychology — Why campaigns work", open=False):
                    psychology_display = gr.JSON()

                with gr.Accordion("Influencer Matcher — Creator recommendations", open=False):
                    influencer_display = gr.JSON()

                with gr.Accordion("Synthesis — Cross-agent strategic brief", open=False):
                    synthesis_display = gr.JSON()

                with gr.Accordion("Critic — Quality review", open=False):
                    critic_display = gr.JSON()

                with gr.Accordion("Content — Campaign-ready copy", open=False):
                    content_display = gr.JSON()

            # ── TAB 3: CHAT WITH AN AGENT ─────────────────────
            with gr.Tab("Chat with an Agent"):

                gr.Markdown("### Agent Conversations", elem_classes="section-title")
                gr.Markdown(
                    "Select a specialist agent and ask it anything about its findings. "
                    "Run the pipeline first — agents will respond with context from your specific brand analysis.",
                    elem_classes="section-subtitle"
                )

                # Agent selector row — like Stripe's product sub-navigation
                with gr.Row():
                    agent_selector = gr.Dropdown(
                        label="Specialist Agent",
                        choices=[
                            "Trend Scout",
                            "Brand Analyst",
                            "Ethics Auditor",
                            "Consumer Psychology",
                            "Influencer Matcher",
                            "Synthesis",
                            "Critic",
                            "Content"
                        ],
                        value="Content",
                        scale=2
                    )
                    # Per-tab model selector for quick switching when quota hits
                    chat_model_selector = gr.Dropdown(
                        choices=list(AVAILABLE_MODELS.keys()),
                        value="Gemini Flash (Latest)",
                        label="Model  (switch if quota exceeded)",
                        elem_classes="model-selector",
                        scale=1
                    )

                agent_chatbot = gr.Chatbot(
                    label="",
                    height=420,
                    elem_classes="chatbot-area",
                    show_label=False
                )

                with gr.Row():
                    agent_message_input = gr.Textbox(
                        label="",
                        placeholder="Ask the agent anything about its findings...",
                        show_label=False,
                        scale=5
                    )
                    agent_send_btn = gr.Button(
                        "Send",
                        variant="primary",
                        scale=1
                    )

            # ── TAB 4: REPORT Q&A ─────────────────────────────
            with gr.Tab("Report Analysis"):

                gr.Markdown("### Ask the Report", elem_classes="section-title")
                gr.Markdown(
                    "Ask any question about the full brand intelligence report. "
                    "This uses the complete report as context, not individual agent findings.",
                    elem_classes="section-subtitle"
                )

                with gr.Row():
                    question_input = gr.Textbox(
                        label="Your Question",
                        placeholder="Which influencer has the highest fit score? What is the primary risk?",
                        show_label=True,
                        scale=4
                    )
                    qa_model_selector = gr.Dropdown(
                        choices=list(AVAILABLE_MODELS.keys()),
                        value="Gemini Flash (Latest)",
                        label="Model",
                        elem_classes="model-selector",
                        scale=1
                    )

                ask_btn = gr.Button("Ask", variant="primary")

                gr.Markdown("---")
                answer_output = gr.Markdown(
                    value="*Your answer will appear here.*",
                    elem_classes="report-area"
                )

    # ── Wire everything ───────────────────────────────────────

    run_btn.click(
        fn=run_modamind,
        inputs=[
            brand_input, category_input, campaign_input,
            competitors_input, audience_input, model_selector
        ],
        outputs=[
            status_output, report_output, pipeline_state,
            trend_display, brand_display, ethics_display,
            psychology_display, influencer_display,
            synthesis_display, critic_display, content_display
        ]
    )

    ask_btn.click(
        fn=answer_followup_question,
        inputs=[question_input, report_output, qa_model_selector],
        outputs=[answer_output]
    )

    agent_send_btn.click(
        fn=chat_with_agent,
        inputs=[
            agent_selector, agent_message_input,
            agent_chatbot, pipeline_state, chat_model_selector
        ],
        outputs=[agent_chatbot, agent_message_input]
    )


# ── Launch ────────────────────────────────────────────────────

if __name__ == "__main__":
    app.launch()