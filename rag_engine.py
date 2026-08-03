from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PaperAnalysisRAG:

    def __init__(self, groq_api_key):

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.2
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        self.vector_store = None

        self.parsed_papers = {}

    # ----------------------------------------------------
    # INGEST PAPERS
    # ----------------------------------------------------

    def ingest_papers(self, paper_dict):

        self.parsed_papers = paper_dict

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        docs = []

        for paper_name, sections in paper_dict.items():

            for section_name, text in sections.items():

                chunks = splitter.split_text(text)

                for chunk in chunks:

                    docs.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                "paper": paper_name,
                                "section": section_name
                            }
                        )
                    )

        self.vector_store = FAISS.from_documents(
            docs,
            self.embeddings
        )

    # ----------------------------------------------------
    # EXTRACT SPECIFIC SECTIONS
    # ----------------------------------------------------

    def extract_specific_sections(
        self,
        paper_name,
        target_sections
    ):

        if paper_name not in self.parsed_papers:

            return "Paper not found."

        sections = self.parsed_papers[paper_name]

        output = []

        for sec in target_sections:

            if sec in sections:

                output.append(
                    f"## {sec}\n\n{sections[sec]}"
                )

            else:

                output.append(
                    f"## {sec}\n\nSection not found."
                )

        return "\n\n".join(output)
