Markdown
# 📄 AI Resume & Job Application Assistant

An intelligent, enterprise-grade job search acceleration engine. By uploading your master resume along with a target job description, this local pipeline parses, evaluates, and dynamically tailors your application materials. 

The system leverages your remote **Ollama GPU node (Qwen 2.5)** to securely perform semantic match analysis, draft targeted cover letters, and generate predictive interview preparation scripts without exposing private professional history to external third-party APIs.

---

## ⚡ Core Features

* **📊 Resume Fit Scoring:** Runs a semantic vector gap analysis between the resume text and job description to output a compatibility rating.
* **✍️ Tailored Resume Optimization:** Rewrites specific achievement blocks and skills matrices to align directly with target keywords and ATS tracking parameters.
* **✉️ Contextual Cover Letter Generator:** Drafts high-impact, custom cover letters matching the exact tone, tech stack, and responsibilities of the role.
* **🎯 Predictive Interview Simulator:** Extrapolates likely technical and behavioral interview questions based on systemic gaps found in your profile relative to the job description.
* **🛠️ Gap Mitigation Suggestions:** Identifies missing certifications, software tools, or methodologies highlighted in the job post, offering clear paths for resume improvement.

---

## 📂 Project Directory Structure

```text
ai_job_assistant/
│
├── core/
│   ├── parser.py           # Extracts structured text from uploaded Resumes (PDF/DOCX)
│   ├── analyzer.py         # Handles gap-analysis, scoring, and query formulation
│   └── generator.py        # Dispatches payloads to Qwen for tailored output synthesis
│
├── .env                    # Infrastructural remote GPU endpoint definitions
├── main.py                 # Interface / application orchestration pipeline
├── requirements.txt        # Package configuration dependencies
└── README.md               # System documentation
🛠️ Installation & Setup
1. Configure the Remote Infrastructure Environment
Create a .env file in the root directory to point the engine toward your active remote hardware setup:

Plaintext
OLLAMA_BASE_URL="[http://10.22.39.192:11434](http://10.22.39.192:11434)"
OLLAMA_MODEL_NAME="qwen2.5-coder:14b"
2. Install Required Packages
Install the required text extraction, parsing, and web utilities:

PowerShell
pip install pypdf docx2txt requests python-dotenv
(Optional: Include streamlit if you choose to attach a clean frontend UI wrapper to this framework).

🚀 Execution Workflow
To execute the optimization pipeline, run the application controller from your terminal window:

PowerShell
python main.py
📊 System Analysis Pipeline Visual Layout
Plaintext
[ Upload Resume + JD ] ──> Structural Text Extraction
                                     │
                                     ▼
[ Pipeline Processing ] ──> Gap Analysis Matrix Execution
                                     │
                                     ▼
[ Remote GPU Node ]     ──> Qwen 2.5 Processing Engines:
                                    ├── Score & Keyword Matching
                                    ├── Profile Adaptation Matrix
                                    ├── Cover Letter Generation
                                    └── Interview Q&A Prediction
📝 Expected Output Layout
When executing successfully, the engine compiles structured operational logs and tailored text blocks:

Plaintext
============================================================
      💼  SYSTEM DIAGNOSTICS: AI JOB APPLICATION ASSISTANT
============================================================
[+] Target Document Parsing Completed.
[+] Connected to Remote GPU Processing Cluster.
[+] Running Analytics Layer via Qwen...

📊 APPLICATION COMPLIANCE SCORE: 72% / 100%

❌ Missing Systemic Keywords: Fast-API, Document Automation, MongoDB Aggregation

------------------------------------------------------------
🔥 REWRITTEN PROFILE MATRICES (ATS OPTIMIZED)
------------------------------------------------------------
"Successfully engineered backend data ingestion microservices utilizing FastAPI 
and optimized MongoDB aggregation arrays, improving document processing throughput 
rates across high-volume validation pipelines."

------------------------------------------------------------
🎯 PREDICTIVE INTERVIEW PREPARATION
------------------------------------------------------------
1. Technical: "Can you describe a scenario where you encountered severe latency or port conflicts while building automated validation engines, and how you refactored the runtime?"
2. Behavioral: "The job description highlights cross-functional communication with clients. Describe how you reframe technical complexities into high-level business briefings."
============================================================
