import streamlit as st
import time

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgentFlow · Research OS",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM + GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800;0,14..32,900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg-base:       #060608;
  --bg-surface:    #0e0f14;
  --bg-elevated:   #14161f;
  --bg-hover:      #1a1d28;
  --border:        #1f2133;
  --border-mid:    #272a3d;
  --border-hi:     #343855;
  --text-primary:  #f0f1f8;
  --text-secondary:#8b8fae;
  --text-muted:    #4a4e6a;
  --text-dim:      #2e3150;
  --blue:          #4f7cff;
  --blue-glow:     rgba(79,124,255,0.18);
  --cyan:          #22d3ee;
  --violet:        #8b5cf6;
  --emerald:       #10b981;
  --amber:         #f59e0b;
  --rose:          #f43f5e;
  --sans:          'Inter', system-ui, sans-serif;
  --mono:          'JetBrains Mono', monospace;
  --r-sm: 6px; --r-md: 10px; --r-lg: 14px; --r-xl: 20px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: var(--sans); }
.stApp { background: var(--bg-base) !important; color: var(--text-primary); }
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 2rem 2rem 4rem !important; max-width: 900px !important; margin: 0 auto !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Top nav ────────────────────────────────────────────────────────────── */
.af-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 2.5rem; height: 56px;
  border-bottom: 1px solid var(--border);
  background: rgba(6,6,8,0.94);
  backdrop-filter: blur(12px);
  position: sticky; top: 0; z-index: 100;
}
.af-logo { display: flex; align-items: center; gap: 0.55rem;
           font-weight: 700; font-size: 0.92rem; color: var(--text-primary); letter-spacing: -0.01em; }
.af-logo-mark {
  width: 26px; height: 26px; border-radius: 7px;
  background: linear-gradient(135deg, var(--blue) 0%, var(--violet) 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.65rem; font-weight: 800; color: #fff;
  box-shadow: 0 0 14px rgba(79,124,255,0.45);
}
.af-nav-chips { display: flex; gap: 0.4rem; align-items: center; }
.nav-chip {
  font-family: var(--mono); font-size: 0.62rem; font-weight: 500;
  letter-spacing: 0.07em; color: var(--text-muted);
  padding: 0.18rem 0.55rem; border: 1px solid var(--border-mid); border-radius: 99px;
}
.nav-chip.live {
  color: var(--emerald); border-color: rgba(16,185,129,0.25);
  background: rgba(16,185,129,0.07);
}
.nav-chip.live::before { content: '●  '; animation: blink 2s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* ── Main wrapper ───────────────────────────────────────────────────────── */
.af-main { max-width: 860px; margin: 0 auto; padding: 3.5rem 2rem 6rem; width: 100%; }

/* ── Hero ───────────────────────────────────────────────────────────────── */
.af-tag {
  display: inline-flex; align-items: center; gap: 0.4rem;
  font-family: var(--mono); font-size: 0.65rem; font-weight: 600;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--blue); padding: 0.22rem 0.7rem;
  border: 1px solid rgba(79,124,255,0.22); border-radius: 99px;
  background: rgba(79,124,255,0.06); margin-bottom: 1.2rem;
}
.af-h1 {
  font-size: 3rem; font-weight: 800; letter-spacing: -0.045em;
  line-height: 1.05; margin-bottom: 0.9rem;
  background: linear-gradient(135deg, #f0f1f8 20%, #6b7194 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.af-sub {
  font-size: 0.97rem; color: var(--text-secondary); font-weight: 400;
  line-height: 1.65; max-width: 500px; margin-bottom: 2.8rem;
}

/* ── Pipeline rail ──────────────────────────────────────────────────────── */
.af-rail {
  display: grid;
  grid-template-columns: 1fr 40px 1fr 40px 1fr 40px 1fr;
  align-items: center;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
}
.af-node { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; }
.af-orb {
  width: 50px; height: 50px; border-radius: 50%;
  border: 1.5px solid var(--border-hi);
  background: var(--bg-surface);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; color: var(--text-dim);
  transition: all 0.3s ease;
}
.af-orb.active {
  border-color: var(--blue);
  background: rgba(79,124,255,0.08);
  color: var(--text-primary);
  box-shadow: 0 0 0 4px rgba(79,124,255,0.1), 0 0 22px rgba(79,124,255,0.3);
  animation: orb-glow 2s ease-in-out infinite;
}
.af-orb.done {
  border-color: rgba(16,185,129,0.5);
  background: rgba(16,185,129,0.08);
  color: var(--emerald);
}
@keyframes orb-glow {
  0%,100%{ box-shadow: 0 0 0 4px rgba(79,124,255,0.1), 0 0 22px rgba(79,124,255,0.3); }
  50%    { box-shadow: 0 0 0 6px rgba(79,124,255,0.07), 0 0 36px rgba(79,124,255,0.45); }
}
.af-node-name {
  font-family: var(--mono); font-size: 0.58rem; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted);
}
.af-node-name.active { color: var(--blue); }
.af-node-name.done   { color: var(--emerald); }
.af-node-num {
  font-family: var(--mono); font-size: 0.52rem; font-weight: 600;
  padding: 0.15rem 0.42rem; border-radius: 3px;
}
.af-node-num.idle   { background: var(--bg-hover); color: var(--text-dim); }
.af-node-num.active { background: rgba(79,124,255,0.15); color: var(--blue); }
.af-node-num.done   { background: rgba(16,185,129,0.12); color: var(--emerald); }
.af-conn {
  height: 1.5px; background: var(--border);
  margin-bottom: 2.4rem; transition: background 0.4s;
}
.af-conn.done { background: rgba(16,185,129,0.3); }

/* ── Input area ─────────────────────────────────────────────────────────── */
.af-input-label {
  font-size: 0.68rem; font-weight: 600; letter-spacing: 0.07em;
  text-transform: uppercase; color: var(--text-muted);
  display: flex; align-items: center; gap: 0.45rem; margin-bottom: 0.55rem;
}
.af-input-label::before {
  content: ''; display: block;
  width: 5px; height: 5px; border-radius: 50%; background: var(--blue);
}

div[data-testid="stTextInput"] label { display: none !important; }
div[data-testid="stTextInput"] > div > div {
  background: var(--bg-elevated) !important;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--r-lg) !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.03) !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] > div > div:focus-within {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px var(--blue-glow), 0 1px 3px rgba(0,0,0,0.35) !important;
}
div[data-testid="stTextInput"] input {
  background: transparent !important;
  color: var(--text-primary) !important;
  font-family: var(--sans) !important;
  font-size: 1rem !important; font-weight: 400 !important;
  padding: 0.85rem 1.2rem !important;
  border: none !important; letter-spacing: -0.01em;
}
div[data-testid="stTextInput"] input::placeholder { color: var(--text-muted) !important; }

div[data-testid="stButton"] > button {
  background: var(--blue) !important;
  color: #fff !important; border: none !important;
  border-radius: var(--r-md) !important;
  font-family: var(--sans) !important;
  font-size: 0.88rem !important; font-weight: 600 !important;
  letter-spacing: -0.005em !important;
  padding: 0.7rem 1.5rem !important; width: 100% !important;
  box-shadow: 0 4px 16px rgba(79,124,255,0.35) !important;
  transition: opacity 0.15s, transform 0.1s !important;
}
div[data-testid="stButton"] > button:hover { opacity:0.86 !important; transform:translateY(-1px) !important; }
div[data-testid="stButton"] > button:active { transform:translateY(0) !important; }

/* ── Status log ─────────────────────────────────────────────────────────── */
.af-status {
  font-family: var(--mono); font-size: 0.7rem; color: var(--blue);
  letter-spacing: 0.04em; padding: 0.6rem 0 1.2rem;
  display: flex; align-items: center; gap: 0.55rem;
}
.af-status::before {
  content: ''; width: 6px; height: 6px; border-radius: 50%;
  background: var(--blue); flex-shrink: 0;
  animation: blink 1.1s ease-in-out infinite;
}

/* ── Output cards ───────────────────────────────────────────────────────── */
.af-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  margin-bottom: 0.85rem; overflow: hidden;
  transition: border-color 0.2s;
}
.af-card:hover { border-color: var(--border-hi); }
.af-card-head {
  display: flex; align-items: center; gap: 0.7rem;
  padding: 0.8rem 1.2rem;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,0.012);
}
.af-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.d-search { background: #4f7cff; box-shadow: 0 0 6px #4f7cff55; }
.d-reader { background: #8b5cf6; box-shadow: 0 0 6px #8b5cf655; }
.d-writer { background: #10b981; box-shadow: 0 0 6px #10b98155; }
.d-critic { background: #f59e0b; box-shadow: 0 0 6px #f59e0b55; }
.d-run    { background: #22d3ee; box-shadow: 0 0 6px #22d3ee55; animation: blink 1s ease-in-out infinite; }

.af-label {
  font-family: var(--mono); font-size: 0.62rem; font-weight: 600;
  letter-spacing: 0.09em; text-transform: uppercase;
  padding: 0.16rem 0.5rem; border-radius: 4px;
}
.l-search { color:#4f7cff; background: rgba(79,124,255,0.1);  }
.l-reader { color:#8b5cf6; background: rgba(139,92,246,0.1); }
.l-writer { color:#10b981; background: rgba(16,185,129,0.1); }
.l-critic { color:#f59e0b; background: rgba(245,158,11,0.1); }
.l-run    { color:#22d3ee; background: rgba(34,211,238,0.08); }

.af-card-title { font-size: 0.83rem; font-weight: 600; color: var(--text-primary);
                 letter-spacing: -0.01em; flex: 1; }
.af-card-ts   { font-family: var(--mono); font-size: 0.58rem; color: var(--text-muted); }

.af-card-body {
  padding: 1.2rem 1.5rem;
  font-family: var(--mono); font-size: 0.76rem; line-height: 1.82;
  color: #9099c0; white-space: pre-wrap; word-break: break-word;
  max-height: 340px; overflow-y: auto;
}
.af-card-body.prose {
  font-family: var(--sans); font-size: 0.9rem; line-height: 1.9;
  color: var(--text-primary); max-height: 540px;
}
.af-card-body::-webkit-scrollbar { width: 3px; }
.af-card-body::-webkit-scrollbar-track { background: transparent; }
.af-card-body::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 4px; }

/* shimmer skeleton */
.af-shimmer { padding: 1.4rem 1.5rem; display: flex; flex-direction: column; gap: 0.55rem; }
.sh { height: 9px; border-radius: 4px;
      background: linear-gradient(90deg, var(--border) 25%, var(--border-mid) 50%, var(--border) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.6s ease-in-out infinite; }
@keyframes shimmer { 0%{background-position:200%} 100%{background-position:-200%} }
.sh.w90{width:90%} .sh.w80{width:80%} .sh.w70{width:70%} .sh.w60{width:60%}

/* ── Done banner ────────────────────────────────────────────────────────── */
.af-done {
  display: flex; align-items: center; gap: 1rem;
  padding: 1rem 1.4rem;
  background: linear-gradient(135deg, rgba(16,185,129,0.06) 0%, transparent 70%);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: var(--r-lg); margin-bottom: 1.75rem;
}
.af-done-icon { font-size: 1.3rem; }
.af-done-title { font-size: 0.9rem; font-weight: 700; color: var(--emerald); letter-spacing: -0.01em; }
.af-done-sub   { font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.1rem; font-family: var(--mono); }

/* ── Error ──────────────────────────────────────────────────────────────── */
.af-err {
  background: rgba(244,63,94,0.05); border: 1px solid rgba(244,63,94,0.22);
  border-radius: var(--r-lg); padding: 1.2rem 1.5rem;
  font-family: var(--mono); font-size: 0.75rem; color: var(--rose);
  white-space: pre-wrap;
}
.af-err-head { font-weight: 700; margin-bottom: 0.4rem; font-size: 0.78rem; }

/* ── Download ───────────────────────────────────────────────────────────── */
div[data-testid="stDownloadButton"] > button {
  background: transparent !important; color: var(--text-secondary) !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: var(--r-md) !important;
  font-family: var(--sans) !important; font-size: 0.8rem !important; font-weight: 500 !important;
  padding: 0.5rem 1.2rem !important; box-shadow: none !important;
  transition: border-color 0.2s, color 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  border-color: var(--blue) !important; color: var(--blue) !important; transform:none !important;
}

div[data-testid="stAlert"] {
  background: rgba(245,158,11,0.06) !important;
  border: 1px solid rgba(245,158,11,0.2) !important;
  border-radius: var(--r-md) !important;
  color: var(--amber) !important; font-size: 0.82rem !important;
}
div[data-testid="stColumns"] { gap: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_defaults = dict(pipeline_state=None, current_step=0, running=False,
                 error=None, elapsed=None, topic_done="", ts={})
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _ts():   return time.strftime("%H:%M:%S")

def render_rail(step: int):
    step = step or 0
    NODES = [("🔍","Search","01"),("📖","Reader","02"),("✍","Writer","03"),("🔬","Critic","04")]
    parts = []
    for i,(icon,name,num) in enumerate(NODES,1):
        if step > i:   oc,nc,bc,lbl = "done","done","done","✓"
        elif step==i:  oc,nc,bc,lbl = "active","active","active",icon
        else:          oc,nc,bc,lbl = "","","idle",icon
        parts.append(f"""
        <div class="af-node">
          <div class="af-orb {oc}">{lbl}</div>
          <span class="af-node-name {nc}">{name}</span>
          <span class="af-node-num {bc}">{num}</span>
        </div>""")
        if i<len(NODES):
            cc = "done" if step>i else ""
            parts.append(f'<div class="af-conn {cc}"></div>')
    st.markdown(f'<div class="af-rail">{"".join(parts)}</div>', unsafe_allow_html=True)

def make_card(ph, dot_cls, label_cls, label_txt, title, body="", ts="", prose=False, shimmer=False):
    body_cls = "prose" if prose else ""
    if shimmer:
        inner = """<div class="af-shimmer">
          <div class="sh w90"></div><div class="sh w80"></div>
          <div class="sh w70"></div><div class="sh w60"></div>
          <div class="sh w80"></div></div>"""
    else:
        inner = f'<div class="af-card-body {body_cls}">{body}</div>'
    ph.markdown(f"""
<div class="af-card">
  <div class="af-card-head">
    <div class="af-dot {dot_cls}"></div>
    <span class="af-label {label_cls}">{label_txt}</span>
    <span class="af-card-title">{title}</span>
    <span class="af-card-ts">{ts}</span>
  </div>
  {inner}
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NAV BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="af-nav">
  <div class="af-logo">
    <div class="af-logo-mark">⬡</div>
    AgentFlow
  </div>
  <div class="af-nav-chips">
    <span class="nav-chip">v2.4</span>
    <span class="nav-chip">2026</span>
    <span class="nav-chip live">Runtime active</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="af-main">', unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="af-tag">⬡ Agentic Research OS · 2026</div>
<h1 class="af-h1">Research Pipeline</h1>
<p class="af-sub">
  Four specialized AI agents — Search, Reader, Writer, Critic — orchestrate
  a complete research workflow and deliver a verified, structured report.
</p>
""", unsafe_allow_html=True)

# Rail placeholder
rail_ph = st.empty()
with rail_ph:
    render_rail(st.session_state.current_step)

# Input
st.markdown('<div class="af-input-label">Research query · 2026</div>', unsafe_allow_html=True)
col_q, col_btn = st.columns([5, 1.1])
with col_q:
    topic = st.text_input("q", key="topic_input", label_visibility="collapsed",
        placeholder="e.g.  Agentic AI frameworks shaping enterprise software in 2026")
with col_btn:
    st.markdown("<div style='height:0.28rem'></div>", unsafe_allow_html=True)
    run_clicked = st.button("Run →", use_container_width=True)

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE RUNNER
# ─────────────────────────────────────────────────────────────────────────────
def run_pipeline(topic: str):
    st.session_state.running = True
    st.session_state.error   = None
    st.session_state.pipeline_state = None
    state, t0 = {}, time.time()

    try:
        import agents as ag
    except ImportError as e:
        st.session_state.error = f"Import error — agents.py not found:\n{e}"
        st.session_state.running = False
        return

    status_ph = st.empty()
    ph1 = st.empty(); ph2 = st.empty(); ph3 = st.empty(); ph4 = st.empty()
    banner_ph = st.empty()

    # STEP 1 ── Search
    st.session_state.current_step = 1
    rail_ph.empty()
    with rail_ph: render_rail(1)
    status_ph.markdown('<div class="af-status">Search agent initialised — querying live sources…</div>', unsafe_allow_html=True)
    make_card(ph1, "d-run","l-run","Running", "Search Agent — scanning web sources", shimmer=True)
    try:
        sa = ag.build_search_agent()
        r  = sa.invoke({"messages":[("user",f"Search for recent, reliable sources on: {topic}")]})
        state["search_result"] = r["messages"][-1].content
    except Exception as e:
        st.session_state.error = f"Search Agent failed:\n{e}"; st.session_state.running=False; return
    ts1 = _ts(); st.session_state.ts["search"] = ts1
    make_card(ph1,"d-search","l-search","Search","Search Agent — sources indexed",state["search_result"],ts=ts1)

    # STEP 2 ── Reader
    st.session_state.current_step = 2
    rail_ph.empty()
    with rail_ph: render_rail(2)
    status_ph.markdown('<div class="af-status">Reader agent active — extracting & scraping content…</div>', unsafe_allow_html=True)
    make_card(ph2,"d-run","l-run","Running","Reader Agent — scraping top resources",shimmer=True)
    try:
        ra = ag.build_reader_agent()
        r  = ra.invoke({"messages":[("user",f"""
Read and understand the following search results and provide:
1. Cleaned raw notes about '{topic}' — strictly on-topic, no filler.
2. Bullet-point key insights; scrape for deeper content where possible.
3. List of unique source URLs.
Search Results:\n{state['search_result'][:800]}""")]})
        state["scraped_content"] = r["messages"][-1].content
    except Exception as e:
        st.session_state.error = f"Reader Agent failed:\n{e}"; st.session_state.running=False; return
    ts2 = _ts(); st.session_state.ts["reader"] = ts2
    make_card(ph2,"d-reader","l-reader","Reader","Reader Agent — insights extracted",state["scraped_content"],ts=ts2)

    # STEP 3 ── Writer
    st.session_state.current_step = 3
    rail_ph.empty()
    with rail_ph: render_rail(3)
    status_ph.markdown('<div class="af-status">Writer agent composing structured report…</div>', unsafe_allow_html=True)
    make_card(ph3,"d-run","l-run","Running","Writer Agent — drafting report",shimmer=True)
    try:
        combined = f"Search Results:\n{state['search_result']}\n\nScraped Content:\n{state['scraped_content']}"
        state["report"] = ag.writer_chain.invoke({"topic":topic,"research":combined})
    except Exception as e:
        st.session_state.error = f"Writer Agent failed:\n{e}"; st.session_state.running=False; return
    ts3 = _ts(); st.session_state.ts["writer"] = ts3
    make_card(ph3,"d-writer","l-writer","Writer","Writer Agent — report compiled",state["report"],ts=ts3,prose=True)

    # STEP 4 ── Critic
    st.session_state.current_step = 4
    rail_ph.empty()
    with rail_ph: render_rail(4)
    status_ph.markdown('<div class="af-status">Critic agent reviewing quality, depth & accuracy…</div>', unsafe_allow_html=True)
    make_card(ph4,"d-run","l-run","Running","Critic Agent — quality review",shimmer=True)
    try:
        state["feedback"] = ag.critic_chain.invoke({"report":state["report"]})
    except Exception as e:
        st.session_state.error = f"Critic Agent failed:\n{e}"; st.session_state.running=False; return
    ts4 = _ts(); st.session_state.ts["critic"] = ts4
    make_card(ph4,"d-critic","l-critic","Critic","Critic Agent — review complete",state["feedback"],ts=ts4)

    # Done
    elapsed = round(time.time()-t0,1)
    st.session_state.update(dict(current_step=5,pipeline_state=state,elapsed=elapsed,
                                 topic_done=topic,running=False))
    status_ph.empty()
    rail_ph.empty()
    with rail_ph: render_rail(5)
    banner_ph.markdown(f"""
<div class="af-done">
  <div class="af-done-icon">✦</div>
  <div>
    <div class="af-done-title">Pipeline complete</div>
    <div class="af-done-sub">4 agents · {elapsed}s elapsed · {time.strftime("%d %b %Y, %H:%M")}</div>
  </div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TRIGGER
# ─────────────────────────────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("Enter a research query to start the pipeline.")
    else:
        run_pipeline(topic.strip())
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# PERSISTED RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.pipeline_state:
    s, ts = st.session_state.pipeline_state, st.session_state.ts
    render_rail(5)
    st.markdown(f"""
<div class="af-done">
  <div class="af-done-icon">✦</div>
  <div>
    <div class="af-done-title">Pipeline complete</div>
    <div class="af-done-sub">4 agents · {st.session_state.elapsed}s · {st.session_state.topic_done}</div>
  </div>
</div>""", unsafe_allow_html=True)

    def sc(d,l,lt,title,body,tk,prose=False):
        make_card(st.empty(),d,l,lt,title,body,ts=ts.get(tk,""),prose=prose)

    sc("d-search","l-search","Search","Search Agent — sources indexed",    s.get("search_result",""), "search")
    sc("d-reader","l-reader","Reader","Reader Agent — insights extracted",  s.get("scraped_content",""),"reader")
    sc("d-writer","l-writer","Writer","Writer Agent — final report",        s.get("report",""),        "writer",prose=True)
    sc("d-critic","l-critic","Critic","Critic Agent — quality review",      s.get("feedback",""),      "critic")

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    slug = st.session_state.topic_done.replace(" ","_")[:36]
    full = f"""AGENTFLOW RESEARCH OUTPUT
Generated : {time.strftime("%d %B %Y  %H:%M")}
Topic     : {st.session_state.topic_done}
Runtime   : {st.session_state.elapsed}s

{'═'*60}
SEARCH RESULTS
{'═'*60}
{s.get('search_result','')}

{'═'*60}
SCRAPED INSIGHTS
{'═'*60}
{s.get('scraped_content','')}

{'═'*60}
FINAL REPORT
{'═'*60}
{s.get('report','')}

{'═'*60}
CRITIC FEEDBACK
{'═'*60}
{s.get('feedback','')}
"""
    st.download_button("⬇  Export full report",data=full,
        file_name=f"agentflow_{slug}_{time.strftime('%Y%m%d')}.txt",mime="text/plain")

# ─────────────────────────────────────────────────────────────────────────────
# ERROR DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f"""
<div class="af-err">
  <div class="af-err-head">⚠ Agent Error</div>{st.session_state.error}
</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close af-main