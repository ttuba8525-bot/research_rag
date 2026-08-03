import streamlit as st
from utils import (
    initialize_rag,
    extract_sections_ui,
    run_comparison,
    run_gap_analysis,
    answer_query,
    discover_papers
)

st.set_page_config(
    page_title="PragyanAI Academic Paper RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PragyanAI Academic Paper RAG Engine")
st.markdown(
    """
Upload multiple research papers and perform:

- 📄 Section Extraction
- 📊 Comparative Analysis
- 🔍 Research Gap Identification
- 🤖 RAG-based Question Answering
- 🌐 Discover Similar Papers
"""
)

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

if "rag_initialized" not in st.session_state:
    st.session_state.rag_initialized = False

if "papers" not in st.session_state:
    st.session_state.papers = []

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.header("Configuration")

    groq_key = st.text_input(
        "Groq API Key",
        type="password"
    )

    uploaded_files = st.file_uploader(
        "Upload Research Papers",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("🚀 Ingest Papers"):

        if not groq_key:
            st.error("Please enter your Groq API Key.")

        elif not uploaded_files:
            st.error("Upload at least one paper.")

        else:

            with st.spinner("Processing papers..."):

                success, papers = initialize_rag(
                    uploaded_files,
                    groq_key
                )

            if success:

                st.session_state.rag_initialized = True
                st.session_state.papers = papers

                st.success(
                    f"Processed {len(papers)} paper(s)."
                )

# -------------------------------------------------------
# STOP IF NOT INITIALIZED
# -------------------------------------------------------

if not st.session_state.rag_initialized:

    st.info("Upload papers and click **Ingest Papers**.")

    st.stop()

# -------------------------------------------------------
# TABS
# -------------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Extract Sections",
    "📊 Compare Papers",
    "🔍 Research Gaps",
    "🤖 Ask Questions",
    "🌐 Similar Papers"
])

# =======================================================
# TAB 1
# =======================================================

with tab1:

    paper = st.selectbox(
        "Select Paper",
        st.session_state.papers
    )

    sections = st.multiselect(

        "Select Sections",

        [
            "Abstract",
            "Introduction",
            "Related Work",
            "Methodology",
            "Results",
            "Discussion & Gaps",
            "Conclusion"
        ],

        default=[
            "Abstract",
            "Methodology",
            "Results"
        ]
    )

    if st.button("Extract"):

        output = extract_sections_ui(
            paper,
            sections
        )

        st.markdown(output)

# =======================================================
# TAB 2
# =======================================================

with tab2:

    aspect = st.text_input(

        "Comparison Focus",

        value="Methodology, Dataset, Results"

    )

    if st.button("Generate Comparison"):

        with st.spinner("Comparing papers..."):

            output = run_comparison(aspect)

        st.markdown(output)

# =======================================================
# TAB 3
# =======================================================

with tab3:

    if st.button("Identify Research Gaps"):

        with st.spinner("Finding gaps..."):

            output = run_gap_analysis()

        st.markdown(output)

# =======================================================
# TAB 4
# =======================================================

with tab4:

    question = st.text_input(
        "Ask your question"
    )

    section_filter = st.selectbox(

        "Filter Section",

        [
            "All",
            "Abstract",
            "Introduction",
            "Methodology",
            "Results",
            "Discussion & Gaps"
        ]
    )

    if st.button("Ask"):

        with st.spinner("Searching..."):

            answer = answer_query(
                question,
                section_filter
            )

        st.markdown(answer)

# =======================================================
# TAB 5
# =======================================================

with tab5:

    topic = st.text_input(
        "Research Topic"
    )

    if st.button("Find Similar Papers"):

        with st.spinner("Searching arXiv..."):

            result = discover_papers(topic)

        st.markdown(result)
