import re
import fitz  # PyMuPDF

# ---------------------------------------------------------
# Section Heading Patterns
# ---------------------------------------------------------

SECTION_PATTERNS = {
    "Abstract": re.compile(r"^(abstract)", re.IGNORECASE),

    "Introduction": re.compile(
        r"^(1\.?\s*introduction|introduction)",
        re.IGNORECASE
    ),

    "Related Work": re.compile(
        r"^(\d\.?\s*related work|background)",
        re.IGNORECASE
    ),

    "Methodology": re.compile(
        r"^(\d\.?\s*methodology|proposed method|system model|architecture)",
        re.IGNORECASE
    ),

    "Results": re.compile(
        r"^(\d\.?\s*experiments|results|evaluation)",
        re.IGNORECASE
    ),

    "Discussion & Gaps": re.compile(
        r"^(\d\.?\s*discussion|limitations|threats to validity)",
        re.IGNORECASE
    ),

    "Conclusion": re.compile(
        r"^(\d\.?\s*conclusion|future work)",
        re.IGNORECASE
    ),
}


# ---------------------------------------------------------
# Extract Structured Sections
# ---------------------------------------------------------

def extract_structured_sections(pdf_path):
    """
    Extracts academic sections from a PDF.
    Returns:
        {
            "Abstract": "...",
            "Introduction": "...",
            ...
        }
    """

    doc = fitz.open(pdf_path)

    pages = []

    for page in doc:
        pages.append(page.get_text())

    doc.close()

    text = "\n".join(pages)

    lines = text.split("\n")

    sections = {
        "Abstract": "",
        "Introduction": "",
        "Related Work": "",
        "Methodology": "",
        "Results": "",
        "Discussion & Gaps": "",
        "Conclusion": "",
        "Other": ""
    }

    current_section = "Abstract"

    for line in lines:

        clean = line.strip()

        found = False

        for section_name, pattern in SECTION_PATTERNS.items():

            if pattern.match(clean) and len(clean) < 60:

                current_section = section_name
                found = True
                break

        if not found:
            sections[current_section] += line + "\n"

    cleaned_sections = {}

    for key, value in sections.items():

        if len(value.strip()) > 50:
            cleaned_sections[key] = value.strip()

    return cleaned_sections
