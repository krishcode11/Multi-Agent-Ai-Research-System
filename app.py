import streamlit as st
from pipeline import run_research_pipeline

# Set up the page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #1E3A8A;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
    }
    .info-box {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🤖 Multi-Agent AI Research System")
st.markdown("""
<div class="info-box">
    This system utilizes a multi-agent architecture to autonomously research, read, write, and review content on any given topic. 
    Simply enter your topic below and let the agents do the heavy lifting!
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown("### What would you like to research today?")
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input("Research Topic", label_visibility="collapsed", placeholder="e.g., The future of solid-state batteries in EVs...")

with col2:
    start_research = st.button("🚀 Start Research", use_container_width=True)

st.divider()

# Execution and Results
if start_research:
    if not topic.strip():
        st.warning("⚠️ Please enter a research topic before starting.")
    else:
        # Create a status container to show progress
        status_container = st.container()
        
        with status_container:
            with st.spinner(f"Agents are actively researching **'{topic}'**... This may take a few minutes."):
                try:
                    # Run the research pipeline (this will block until complete)
                    state = run_research_pipeline(topic)
                    
                    st.success("🎉 Research completed successfully!")
                    
                    # Display the results using tabs for clean organization
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📄 Final Report", 
                        "🧐 Critic Feedback", 
                        "🔍 Search Results", 
                        "📝 Scraped Content"
                    ])
                    
                    with tab1:
                        st.markdown("### Final Research Report")
                        # The report is likely formatted in Markdown, so st.markdown renders it well
                        st.markdown(state.get("report", "No report generated."))
                        
                    with tab2:
                        st.markdown("### Critic's Review")
                        st.info("The Critic Agent analyzes the report for accuracy, tone, and completeness.")
                        st.markdown(state.get("feedback", "No feedback available."))
                        
                    with tab3:
                        st.markdown("### Raw Search Results")
                        with st.expander("Expand to view raw search context"):
                            st.text(state.get("search_result", "No search results."))
                            
                    with tab4:
                        st.markdown("### Cleaned Scraped Content")
                        with st.expander("Expand to view scraped content"):
                            st.text(state.get("scraped_content", "No scraped content."))
                            
                except Exception as e:
                    st.error(f"❌ An error occurred during the research process:\n\n{str(e)}")
                    st.info("Please check the terminal for more detailed error logs.")
