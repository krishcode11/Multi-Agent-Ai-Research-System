import streamlit as st
import time
import sys
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    color: #f0f6fc;
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem;
    line-height: 1.15;
}
.hero-sub {
    color: #8b949e;
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

/* ── Pipeline rail ── */
.pipeline-rail {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2rem 0 2.5rem;
    padding: 1.5rem 2rem;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
}
.step-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}
.step-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    border: 2px solid #30363d;
    background: #0d1117;
    color: #484f58;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
}
.step-icon.active {
    border-color: #3b82f6;
    background: #0f2749;
    color: #93c5fd;
    box-shadow: 0 0 18px rgba(59,130,246,0.4);
    animation: pulse-blue 1.8s ease-in-out infinite;
}
.step-icon.done {
    border-color: #238636;
    background: #0f2d1f;
    color: #3fb950;
    box-shadow: 0 0 10px rgba(35,134,54,0.25);
}
@keyframes pulse-blue {
    0%, 100% { box-shadow: 0 0 12px rgba(59,130,246,0.35); }
    50%       { box-shadow: 0 0 24px rgba(59,130,246,0.7); }
}
.step-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    color: #484f58;
    text-align: center;
    text-transform: uppercase;
}
.step-label.active  { color: #93c5fd; }
.step-label.done    { color: #3fb950; }
.step-connector {
    height: 2px;
    flex: 0.4;
    background: #21262d;
    margin-bottom: 1.2rem;
}
.step-connector.done { background: #238636; }

/* ── Input area ── */
.input-section {
    margin-bottom: 2rem;
}

/* Streamlit input overrides */
.stTextInput > div > div > input {
    background: #161b22 !important;
    border: 1.5px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
.stTextInput > label {
    color: #8b949e !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.4rem !important;
}

/* Run button */
.stButton > button {
    background: #3b82f6 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.01em !important;
    transition: background 0.2s, transform 0.1s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #2563eb !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Output cards ── */
.output-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    margin-bottom: 1rem;
    overflow: hidden;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.9rem 1.25rem;
    border-bottom: 1px solid #21262d;
    background: #0d1117;
}
.card-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    text-transform: uppercase;
    font-weight: 600;
}
.badge-search   { background: #0f2749; color: #3b82f6; }
.badge-reader   { background: #1c1039; color: #a78bfa; }
.badge-writer   { background: #0f2d1f; color: #3fb950; }
.badge-critic   { background: #2d1a00; color: #f59e0b; }
.badge-running  { background: #1a1a00; color: #facc15; }

.card-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e6edf3;
}
.card-body {
    padding: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.75;
    color: #adbac7;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 380px;
    overflow-y: auto;
}
.card-body::-webkit-scrollbar { width: 5px; }
.card-body::-webkit-scrollbar-track { background: #0d1117; }
.card-body::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }

/* Final report gets richer styling */
.card-body.report {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    line-height: 1.9;
    color: #e6edf3;
    max-height: 600px;
}

/* ── Status bar ── */
.status-bar {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #3b82f6;
    padding: 0.5rem 0 1rem;
    letter-spacing: 0.04em;
}

/* ── Complete banner ── */
.complete-banner {
    background: linear-gradient(135deg, #0f2d1f 0%, #0d1117 100%);
    border: 1px solid #238636;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.complete-banner .icon { font-size: 1.5rem; }
.complete-banner .text { color: #3fb950; font-weight: 600; font-size: 0.95rem; }
.complete-banner .sub  { color: #8b949e; font-size: 0.8rem; margin-top: 0.2rem; }

/* ── Error state ── */
.error-card {
    background: #2d0f0f;
    border: 1px solid #6e2b2b;
    border-radius: 10px;
    padding: 1.25rem;
    color: #f85149;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
}

/* Spinner override */
.stSpinner > div { border-top-color: #3b82f6 !important; }

/* Expander override */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────────
for key in ["pipeline_state", "running", "current_step", "error", "elapsed"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "running" not in st.session_state:
    st.session_state.running = False

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent System</div>
    <h1>Research Pipeline</h1>
    <p class="hero-sub">Search → Read → Write → Review, orchestrated automatically</p>
</div>
""", unsafe_allow_html=True)

# ── Pipeline rail renderer ─────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search",  "search"),
    ("📖", "Reader",  "reader"),
    ("✍️",  "Writer",  "writer"),
    ("🧐", "Critic",  "critic"),
]

def render_rail(current_step: int):
    """Render the 4-step pipeline progress rail. current_step: 0=idle, 1-4=active."""
    nodes_html = ""
    for i, (icon, label, _) in enumerate(STEPS, start=1):
        if current_step > i:
            icon_cls, label_cls = "done", "done"
            icon_display = "✓"
        elif current_step == i:
            icon_cls, label_cls = "active", "active"
            icon_display = icon
        else:
            icon_cls, label_cls = "", ""
            icon_display = icon

        connector_cls = "done" if current_step > i else ""
        node_html = f"""
        <div class="step-node">
            <div class="step-icon {icon_cls}">{icon_display}</div>
            <div class="step-label {label_cls}">{label}</div>
        </div>"""
        nodes_html += node_html
        if i < len(STEPS):
            nodes_html += f'<div class="step-connector {connector_cls}"></div>'

    st.markdown(f'<div class="pipeline-rail">{nodes_html}</div>', unsafe_allow_html=True)

render_rail(st.session_state.current_step or 0)

# ── Input ──────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1.2])
with col_input:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='height:0.15rem'></div>", unsafe_allow_html=True)
    run_clicked = st.button("Run Pipeline", use_container_width=True)

# ── Pipeline runner ────────────────────────────────────────────────────────────
def stream_output(placeholder, text: str, title: str, badge_class: str, card_class: str = ""):
    """Render an output card with streamed-in text."""
    placeholder.markdown(f"""
<div class="output-card">
    <div class="card-header">
        <span class="card-badge {badge_class}">{title.split()[0]}</span>
        <span class="card-title">{title}</span>
    </div>
    <div class="card-body {card_class}">{text}</div>
</div>
""", unsafe_allow_html=True)


def run_pipeline(topic: str):
    st.session_state.running = True
    st.session_state.error = None
    st.session_state.pipeline_state = {}

    try:
        from pipeline import run_research_pipeline
    except ImportError as e:
        st.session_state.error = (
            f"Could not import pipeline.py: {e}\n\n"
            "Make sure pipeline.py (and agents.py) are in the same directory as app.py."
        )
        st.session_state.running = False
        return

    start = time.time()

    # Placeholders for live cards
    rail_ph     = st.empty()
    status_ph   = st.empty()
    search_ph   = st.empty()
    reader_ph   = st.empty()
    writer_ph   = st.empty()
    critic_ph   = st.empty()
    banner_ph   = st.empty()

    # ── We monkey-patch the pipeline to capture intermediate state ──
    # Because pipeline.py returns the full state dict, we call it directly.
    # For live step updates we use a thin wrapper approach.

    import pipeline as pl
    import agents as ag

    state = {}

    # STEP 1 – Search
    st.session_state.current_step = 1
    render_placeholder = rail_ph
    status_ph.markdown(
        '<div class="status-bar">⟳ Step 1/4 — Search Agent scanning the web…</div>',
        unsafe_allow_html=True,
    )
    search_ph.markdown("""
<div class="output-card">
    <div class="card-header">
        <span class="card-badge badge-running">Running</span>
        <span class="card-title">Search Agent — gathering sources…</span>
    </div>
    <div class="card-body">Querying the web for relevant sources...</div>
</div>""", unsafe_allow_html=True)

    try:
        search_agent = ag.build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Search for recent, reliable sources on: {topic}")]
        })
        state["search_result"] = search_result["messages"][-1].content
    except Exception as e:
        st.session_state.error = f"Search Agent failed:\n{e}"
        st.session_state.running = False
        return

    stream_output(
        search_ph,
        state["search_result"],
        "🔍 Search Agent — sources found",
        "badge-search",
    )

    # STEP 2 – Reader
    st.session_state.current_step = 2
    status_ph.markdown(
        '<div class="status-bar">⟳ Step 2/4 — Reader Agent scraping content…</div>',
        unsafe_allow_html=True,
    )
    reader_ph.markdown("""
<div class="output-card">
    <div class="card-header">
        <span class="card-badge badge-running">Running</span>
        <span class="card-title">Reader Agent — scraping top resources…</span>
    </div>
    <div class="card-body">Reading and extracting key insights from sources...</div>
</div>""", unsafe_allow_html=True)

    try:
        reader_agent = ag.build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user", f"""
Read and understand the following search results and provide:
1. Cleaned raw notes and search results about '{topic}' strictly related to the topic and avoid unnecessary information.
2. Bullet points of key insights and scrape it for deeper content.
3. List of unique URLs to read
Search Results:\n
{state['search_result'][:800]}
""")]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
    except Exception as e:
        st.session_state.error = f"Reader Agent failed:\n{e}"
        st.session_state.running = False
        return

    stream_output(
        reader_ph,
        state["scraped_content"],
        "📖 Reader Agent — insights extracted",
        "badge-reader",
    )

    # STEP 3 – Writer
    st.session_state.current_step = 3
    status_ph.markdown(
        '<div class="status-bar">⟳ Step 3/4 — Writer Agent drafting the report…</div>',
        unsafe_allow_html=True,
    )
    writer_ph.markdown("""
<div class="output-card">
    <div class="card-header">
        <span class="card-badge badge-running">Running</span>
        <span class="card-title">Writer Agent — composing the report…</span>
    </div>
    <div class="card-body">Synthesising research into a structured report...</div>
</div>""", unsafe_allow_html=True)

    try:
        research_combined = (
            f"Search Results:\n{state['search_result']}\n\n"
            f"Detailed Scraped Content:\n{state['scraped_content']}"
        )
        state["report"] = ag.writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
    except Exception as e:
        st.session_state.error = f"Writer Agent failed:\n{e}"
        st.session_state.running = False
        return

    stream_output(
        writer_ph,
        state["report"],
        "✍️ Writer Agent — report ready",
        "badge-writer",
        "report",
    )

    # STEP 4 – Critic
    st.session_state.current_step = 4
    status_ph.markdown(
        '<div class="status-bar">⟳ Step 4/4 — Critic Agent reviewing the report…</div>',
        unsafe_allow_html=True,
    )
    critic_ph.markdown("""
<div class="output-card">
    <div class="card-header">
        <span class="card-badge badge-running">Running</span>
        <span class="card-title">Critic Agent — reviewing quality…</span>
    </div>
    <div class="card-body">Evaluating the report for accuracy, depth, and clarity...</div>
</div>""", unsafe_allow_html=True)

    try:
        state["feedback"] = ag.critic_chain.invoke({"report": state["report"]})
    except Exception as e:
        st.session_state.error = f"Critic Agent failed:\n{e}"
        st.session_state.running = False
        return

    stream_output(
        critic_ph,
        state["feedback"],
        "🧐 Critic Agent — review complete",
        "badge-critic",
    )

    # Done
    elapsed = round(time.time() - start, 1)
    st.session_state.current_step = 5   # all done
    st.session_state.pipeline_state = state
    st.session_state.elapsed = elapsed
    st.session_state.running = False

    status_ph.empty()
    banner_ph.markdown(f"""
<div class="complete-banner">
    <span class="icon">✅</span>
    <div>
        <div class="text">Pipeline complete — report ready</div>
        <div class="sub">Finished in {elapsed}s · Search → Read → Write → Review</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.session_state.topic_done = topic


# ── Trigger ────────────────────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic before running.")
    else:
        run_pipeline(topic.strip())
        st.rerun()

# ── Show persisted results on re-render ───────────────────────────────────────
if st.session_state.pipeline_state:
    s = st.session_state.pipeline_state
    render_rail(5)

    st.markdown(f"""
<div class="complete-banner">
    <span class="icon">✅</span>
    <div>
        <div class="text">Pipeline complete</div>
        <div class="sub">Finished in {st.session_state.elapsed}s · Topic: {st.session_state.get('topic_done', '')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    def card(html_ph, content, title, badge, card_cls=""):
        st.markdown(f"""
<div class="output-card">
    <div class="card-header">
        <span class="card-badge {badge}">{title.split()[0]}</span>
        <span class="card-title">{title}</span>
    </div>
    <div class="card-body {card_cls}">{content}</div>
</div>""", unsafe_allow_html=True)

    card(None, s.get("search_result", ""),   "🔍 Search Agent — sources",            "badge-search")
    card(None, s.get("scraped_content", ""), "📖 Reader Agent — insights",           "badge-reader")
    card(None, s.get("report", ""),          "✍️ Writer Agent — full report",         "badge-writer", "report")
    card(None, s.get("feedback", ""),        "🧐 Critic Agent — review & feedback",  "badge-critic")

    # Download button
    st.markdown("<br>", unsafe_allow_html=True)
    full_output = f"""RESEARCH PIPELINE OUTPUT
========================
Topic: {st.session_state.get('topic_done', '')}
Generated in: {st.session_state.elapsed}s

SEARCH RESULTS
--------------
{s.get('search_result', '')}

SCRAPED INSIGHTS
----------------
{s.get('scraped_content', '')}

FINAL REPORT
------------
{s.get('report', '')}

CRITIC FEEDBACK
---------------
{s.get('feedback', '')}
"""
    st.download_button(
        label="⬇ Download full report as .txt",
        data=full_output,
        file_name=f"research_{st.session_state.get('topic_done','output').replace(' ','_')[:40]}.txt",
        mime="text/plain",
    )

# ── Error display ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f"""
<div class="error-card">
⚠ Error encountered:<br><br>{st.session_state.error}
</div>
""", unsafe_allow_html=True)