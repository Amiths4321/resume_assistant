# resume_ai.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST  = os.getenv("OLLAMA_HOST",  "http://10.22.39.192:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5vl:latest")

FENCE = "```"


def call_llm(prompt: str, max_tokens: int = 2048) -> str:
    resp = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model":   OLLAMA_MODEL,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": 0.2, "num_predict": max_tokens}
        },
        timeout=180
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


# ── 1. Job fit scoring ────────────────────────────────────────────────────────

def score_job_fit(resume_text: str, job_description: str) -> dict:
    """
    Score how well the resume fits the job description.
    Returns structured scoring dict.
    """
    prompt = (
        "You are an expert recruiter and career coach.\n"
        "Analyse how well this resume matches the job description.\n\n"
        f"RESUME:\n{resume_text[:3000]}\n\n"
        f"JOB DESCRIPTION:\n{job_description[:2000]}\n\n"
        "Provide your analysis in this EXACT JSON format:\n"
        f"{FENCE}json\n"
        "{\n"
        '  "overall_score": 75,\n'
        '  "verdict": "Strong match / Good match / Partial match / Weak match",\n'
        '  "matching_skills": ["skill1", "skill2"],\n'
        '  "missing_skills": ["skill1", "skill2"],\n'
        '  "matching_experience": ["point1", "point2"],\n'
        '  "gaps": ["gap1", "gap2"],\n'
        '  "strengths": ["strength1", "strength2"],\n'
        '  "recommendations": ["rec1", "rec2"]\n'
        "}\n"
        f"{FENCE}\n\n"
        "Be specific and honest. Score from 0 to 100."
    )

    raw = call_llm(prompt, max_tokens=1024)

    # Parse JSON
    try:
        if FENCE in raw:
            parts = raw.split(FENCE)
            for part in parts:
                if part.startswith("json"):
                    raw = part[4:].strip()
                    break
        result = json.loads(raw.strip())
        return result
    except Exception:
        # Fallback
        return {
            "overall_score":       60,
            "verdict":             "Partial match",
            "matching_skills":     [],
            "missing_skills":      [],
            "matching_experience": [],
            "gaps":                [],
            "strengths":           [],
            "recommendations":     ["Could not fully parse — see raw response above"]
        }


# ── 2. Resume rewriter ────────────────────────────────────────────────────────

def rewrite_resume(resume_text: str, job_description: str) -> str:
    """Rewrite resume tailored to the specific job."""
    prompt = (
        "You are an expert resume writer and career coach.\n"
        "Rewrite this resume to be perfectly tailored for the job description below.\n\n"
        "RULES:\n"
        "- Keep all factual information accurate — do NOT invent experience\n"
        "- Reorder bullet points to highlight most relevant experience first\n"
        "- Use keywords from the job description naturally\n"
        "- Strengthen weak action verbs (e.g. 'helped with' → 'led', 'worked on' → 'delivered')\n"
        "- Add metrics where they can be inferred (e.g. 'improved performance' → 'improved performance by ~30%')\n"
        "- Ensure ATS compatibility — no tables, no graphics\n"
        "- Keep the same sections but optimise content\n\n"
        f"ORIGINAL RESUME:\n{resume_text[:3000]}\n\n"
        f"TARGET JOB DESCRIPTION:\n{job_description[:2000]}\n\n"
        "Write the complete rewritten resume below. "
        "Use markdown formatting with ## for section headings and - for bullets:"
    )
    return call_llm(prompt, max_tokens=3000)


# ── 3. Cover letter generator ─────────────────────────────────────────────────

def generate_cover_letter(
    resume_text:     str,
    job_description: str,
    company_name:    str = "",
    hiring_manager:  str = "",
    tone:            str = "professional"
) -> str:
    """Generate a personalised cover letter."""
    tone_map = {
        "professional": "formal and professional",
        "enthusiastic": "enthusiastic and energetic",
        "concise":      "brief and direct — 3 paragraphs max"
    }
    tone_instruction = tone_map.get(tone, tone_map["professional"])

    prompt = (
        "You are an expert cover letter writer.\n"
        f"Write a {tone_instruction} cover letter tailored to this specific role.\n\n"
        f"APPLICANT RESUME SUMMARY:\n{resume_text[:2000]}\n\n"
        f"JOB DESCRIPTION:\n{job_description[:2000]}\n\n"
        f"COMPANY: {company_name or 'the company'}\n"
        f"HIRING MANAGER: {hiring_manager or 'Hiring Manager'}\n\n"
        "Write a compelling cover letter that:\n"
        "- Opens with a strong hook (not 'I am applying for...')\n"
        "- Connects specific experience to specific job requirements\n"
        "- Shows genuine interest in the company and role\n"
        "- Includes a confident call to action\n"
        "- Is 3-4 paragraphs, under 400 words\n\n"
        "COVER LETTER:"
    )
    return call_llm(prompt, max_tokens=1024)


# ── 4. Interview prep ─────────────────────────────────────────────────────────

def predict_interview_questions(
    resume_text:     str,
    job_description: str
) -> list[dict]:
    """Predict likely interview questions with answer frameworks."""
    prompt = (
        "You are an expert interview coach.\n"
        "Based on the resume and job description, predict the 8 most likely interview questions.\n\n"
        f"RESUME:\n{resume_text[:2000]}\n\n"
        f"JOB DESCRIPTION:\n{job_description[:1500]}\n\n"
        "For each question provide:\n"
        "- The question itself\n"
        "- Question type (Technical / Behavioural / Situational / Role-specific)\n"
        "- A suggested answer framework using the candidate's actual experience\n\n"
        f"Respond in this EXACT JSON format:\n"
        f"{FENCE}json\n"
        "[\n"
        "  {\n"
        '    "question": "...",\n'
        '    "type": "...",\n'
        '    "answer_framework": "..."\n'
        "  }\n"
        "]\n"
        f"{FENCE}"
    )

    raw = call_llm(prompt, max_tokens=2048)

    try:
        if FENCE in raw:
            parts = raw.split(FENCE)
            for part in parts:
                if part.startswith("json"):
                    raw = part[4:].strip()
                    break
                elif part.strip().startswith("["):
                    raw = part.strip()
                    break
        return json.loads(raw.strip())
    except Exception:
        return [
            {
                "question":         "Tell me about yourself.",
                "type":             "Behavioural",
                "answer_framework":  "Start with your current role, mention 2-3 key achievements relevant to this job, explain why you are interested in this opportunity."
            },
            {
                "question":         "Why are you interested in this role?",
                "type":             "Motivational",
                "answer_framework":  "Connect your career goals to what this role offers. Mention specific aspects of the JD that excite you."
            }
        ]


# ── 5. Resume improver ────────────────────────────────────────────────────────

def improve_resume(resume_text: str) -> dict:
    """
    Analyse resume standalone and provide specific improvements.
    """
    prompt = (
        "You are an expert resume writer and career coach.\n"
        "Review this resume and provide specific, actionable improvements.\n\n"
        f"RESUME:\n{resume_text[:3000]}\n\n"
        "Analyse and provide feedback in this EXACT JSON format:\n"
        f"{FENCE}json\n"
        "{\n"
        '  "overall_score": 70,\n'
        '  "summary": "One sentence overall assessment",\n'
        '  "weak_verbs": [{"original": "...", "stronger": "..."}],\n'
        '  "missing_metrics": ["suggestion1", "suggestion2"],\n'
        '  "section_order_suggestion": "...",\n'
        '  "missing_sections": ["section1"],\n'
        '  "top_5_improvements": ["improvement1", "improvement2", "improvement3", "improvement4", "improvement5"],\n'
        '  "ats_issues": ["issue1", "issue2"]\n'
        "}\n"
        f"{FENCE}\n\n"
        "Be specific and constructive."
    )

    raw = call_llm(prompt, max_tokens=1024)

    try:
        if FENCE in raw:
            parts = raw.split(FENCE)
            for part in parts:
                if part.startswith("json"):
                    raw = part[4:].strip()
                    break
        return json.loads(raw.strip())
    except Exception:
        return {
            "overall_score":           65,
            "summary":                 "Resume needs improvement in several areas.",
            "weak_verbs":             [],
            "missing_metrics":        ["Add quantifiable achievements"],
            "section_order_suggestion": "Put skills section before experience",
            "missing_sections":       [],
            "top_5_improvements":     ["Add metrics", "Use stronger verbs",
                                       "Add LinkedIn URL", "Improve summary",
                                       "Tailor for each application"],
            "ats_issues":             ["Avoid tables and columns"]
        }