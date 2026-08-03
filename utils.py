import os
import tempfile

from parser import extract_structured_sections
from rag_engine import PaperAnalysisRAG
from search import discover_papers

# Global RAG object
rag_system = None


# --------------------------------------------------------
# Initialize RAG
# --------------------------------------------------------

def initialize_rag(files, api_key):

    global rag_system

    rag_system = PaperAnalysisRAG(api_key)

    parsed_papers = {}

    paper_names = []

    for file in files:

        paper_name = file.name

        paper_names.append(paper_name)

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

            tmp.write(file.getbuffer())

            temp_pdf = tmp.name

        # Extract sections
        sections = extract_structured_sections(temp_pdf)

        parsed_papers[paper_name] = sections

        os.remove(temp_pdf)

    # Build FAISS Vector Store
    rag_system.ingest_papers(parsed_papers)

    return True, paper_names


# --------------------------------------------------------
# Extract Sections
# --------------------------------------------------------

def extract_sections_ui(paper_name, sections):

    global rag_system

    if rag_system is None:

        return "Please ingest papers first."

    return rag_system.extract_specific_sections(
        paper_name,
        sections
    )


# --------------------------------------------------------
# Comparative Analysis
# --------------------------------------------------------

def run_comparison(aspect):

    global rag_system

    if rag_system is None:

        return "Please ingest papers first."

    return rag_system.generate_comparative_matrix(aspect)


# --------------------------------------------------------
# Research Gap Analysis
# --------------------------------------------------------

def run_gap_analysis():

    global rag_system

    if rag_system is None:

        return "Please ingest papers first."

    return rag_system.identify_research_gaps()


# --------------------------------------------------------
# Question Answering
# --------------------------------------------------------

def answer_query(question, section):

    global rag_system

    if rag_system is None:

        return "Please ingest papers first."

    return rag_system.query_rag(
        question,
        section
    )


# --------------------------------------------------------
# Discover Similar Papers
# --------------------------------------------------------

def discover_papers(topic):

    return discover_papers(topic)
