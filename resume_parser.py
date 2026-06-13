# resume_parser.py
import fitz
from pathlib import Path


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF resume."""
    doc   = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            pages.append(text)
    doc.close()
    return "\n\n".join(pages)


def extract_sections(resume_text: str) -> dict:
    """
    Roughly identify resume sections by common headings.
    Returns dict of section name → content.
    """
    section_keywords = {
        "contact":    ["contact", "email", "phone", "linkedin", "github"],
        "summary":    ["summary", "objective", "profile", "about"],
        "experience": ["experience", "work history", "employment", "career"],
        "education":  ["education", "qualification", "degree", "university"],
        "skills":     ["skills", "technologies", "tools", "expertise"],
        "projects":   ["projects", "portfolio", "achievements"],
        "certifications": ["certifications", "certificates", "courses"],
    }

    lines    = resume_text.split("\n")
    sections = {}
    current  = "header"
    buffer   = []

    for line in lines:
        line_lower = line.lower().strip()

        # Check if this line is a section heading
        matched_section = None
        for section, keywords in section_keywords.items():
            if any(kw in line_lower for kw in keywords) and len(line.strip()) < 40:
                matched_section = section
                break

        if matched_section:
            if buffer:
                sections[current] = "\n".join(buffer).strip()
            current = matched_section
            buffer  = []
        else:
            if line.strip():
                buffer.append(line)

    if buffer:
        sections[current] = "\n".join(buffer).strip()

    return sections