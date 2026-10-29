"""
PlacePilot Resume Parsing, Skill Extraction, and ATS Analysis Engine.
Provides high-accuracy document parsing (PDF/DOCX), boundary preservation,
context-aware skill extraction with evidence, strict certification filtering,
role-specific requirement analysis, and transparent fresher-friendly ATS scoring.
Supports OCR fallback for scanned PDFs and a dynamic extendable skill dictionary.
"""

import io
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# ==============================================================================
# DYNAMIC SKILL DICTIONARY — loaded from config/skill_dictionary.json
# Falls back to the built-in SKILL_TAXONOMY if the file is absent.
# ==============================================================================

_DICT_PATH = Path(__file__).resolve().parents[3] / "config" / "skill_dictionary.json"


def _load_skill_taxonomy() -> Dict[str, Dict[str, Any]]:
    """Load skill taxonomy from JSON config file. Returns built-in dict on failure."""
    global _DICT_PATH
    try:
        if _DICT_PATH.is_file():
            with open(_DICT_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            skills = data.get("skills", {})
            if skills:
                return {k: v for k, v in skills.items()}
    except Exception:
        pass
    return {}  # fallback to built-in below


def reload_skill_taxonomy() -> Dict[str, Dict[str, Any]]:
    """Force-reload taxonomy from JSON (called after admin updates)."""
    loaded = _load_skill_taxonomy()
    if loaded:
        SKILL_TAXONOMY.clear()
        SKILL_TAXONOMY.update(loaded)
    return SKILL_TAXONOMY


# ==============================================================================
# 1. EXTENDABLE SKILL TAXONOMY WITH CANONICAL NAMES, SYNONYMS & DOMAINS
# ==============================================================================

SKILL_TAXONOMY: Dict[str, Dict[str, Any]] = {
    # ── Programming Languages ───────────────────────────────────────────────
    "Python": {
        "category": "Programming Languages",
        "aliases": ["python", "python3", "py"],
        "regex": r"\bpython(?:3)?\b",
    },
    "Java": {
        "category": "Programming Languages",
        "aliases": ["java", "core java", "advanced java", "j2ee"],
        # Negative lookahead to avoid matching javascript
        "regex": r"\bjava\b(?!script)",
    },
    "JavaScript": {
        "category": "Programming Languages",
        "aliases": ["javascript", "js", "ecmascript", "es6"],
        "regex": r"\b(?:javascript|es6|ecmascript)\b",
    },
    "TypeScript": {
        "category": "Programming Languages",
        "aliases": ["typescript", "ts"],
        "regex": r"\btypescript\b|\bts\b(?=\s*[,/|&])",
    },
    "C++": {
        "category": "Programming Languages",
        "aliases": ["c++", "cpp"],
        "regex": r"\bc\+\+\b|\bcpp\b",
    },
    "C": {
        "category": "Programming Languages",
        "aliases": ["c language", "c programming"],
        # Context-checked separately to avoid false matches with 'c', 'etc', or grades
        "regex": r"\bc\s+programming\b|\bc\s+language\b|(?<=[,/|])\s*c\s*(?=[,/|])|\bc\/c\+\+\b",
    },
    "C#": {
        "category": "Programming Languages",
        "aliases": ["c#", "csharp", "c sharp"],
        "regex": r"\bc#\b|\bcsharp\b|\bc\s+sharp\b",
    },
    "Go": {
        "category": "Programming Languages",
        "aliases": ["golang", "go language"],
        # Avoid common verb 'go'
        "regex": r"\bgolang\b|\bgo\s+language\b",
    },
    "Rust": {
        "category": "Programming Languages",
        "aliases": ["rust", "rustlang"],
        "regex": r"\brustlang\b|\brust\s+programming\b|\brust\b(?=\s*[,/|&])",
    },
    "PHP": {
        "category": "Programming Languages",
        "aliases": ["php"],
        "regex": r"\bphp\b",
    },
    "Ruby": {
        "category": "Programming Languages",
        "aliases": ["ruby", "ruby on rails"],
        "regex": r"\bruby\b",
    },
    "SQL": {
        "category": "Programming Languages",
        "aliases": ["sql", "structured query language", "plsql", "t-sql"],
        "regex": r"\bsql\b|\bpl\/?sql\b|\bt-sql\b",
    },
    "R": {
        "category": "Programming Languages",
        "aliases": ["r language", "r programming"],
        "regex": r"\br\s+programming\b|\br\s+language\b|(?<=[,/|])\s*r\s*(?=[,/|])",
    },
    "Shell / Bash": {
        "category": "Programming Languages",
        "aliases": ["bash", "shell scripting", "powershell", "zsh"],
        "regex": r"\bbash\b|\bshell\s+script(?:ing)?\b|\bpowershell\b|\bzsh\b",
    },

    # ── Frontend Development ────────────────────────────────────────────────
    "React": {
        "category": "Frontend",
        "aliases": ["react", "react.js", "reactjs"],
        "regex": r"\breact(?:\.js|js)?\b",
    },
    "Next.js": {
        "category": "Frontend",
        "aliases": ["next.js", "nextjs", "next js"],
        "regex": r"\bnext(?:\.js|js)\b",
    },
    "Angular": {
        "category": "Frontend",
        "aliases": ["angular", "angularjs", "angular 2+"],
        "regex": r"\bangular(?:js)?\b",
    },
    "Vue.js": {
        "category": "Frontend",
        "aliases": ["vue", "vue.js", "vuejs"],
        "regex": r"\bvue(?:\.js|js)?\b",
    },
    "HTML": {
        "category": "Frontend",
        "aliases": ["html", "html5"],
        "regex": r"\bhtml5?\b",
    },
    "CSS": {
        "category": "Frontend",
        "aliases": ["css", "css3"],
        "regex": r"\bcss3?\b",
    },
    "Tailwind CSS": {
        "category": "Frontend",
        "aliases": ["tailwind", "tailwindcss", "tailwind css"],
        "regex": r"\btailwind(?:\s*css)?\b",
    },
    "Bootstrap": {
        "category": "Frontend",
        "aliases": ["bootstrap", "bootstrap 5"],
        "regex": r"\bbootstrap(?:5)?\b",
    },
    "Sass / SCSS": {
        "category": "Frontend",
        "aliases": ["sass", "scss"],
        "regex": r"\bsass\b|\bscss\b",
    },
    "Redux": {
        "category": "Frontend",
        "aliases": ["redux", "redux toolkit", "rtk"],
        "regex": r"\bredux(?:\s+toolkit)?\b|\brtk\b",
    },
    "Webpack / Vite": {
        "category": "Frontend",
        "aliases": ["webpack", "vite", "babel"],
        "regex": r"\bwebpack\b|\bvite\b|\bbabel\b",
    },
    "jQuery": {
        "category": "Frontend",
        "aliases": ["jquery"],
        "regex": r"\bjquery\b",
    },

    # ── Backend & Frameworks ────────────────────────────────────────────────
    "Node.js": {
        "category": "Backend",
        "aliases": ["node.js", "nodejs", "node js", "node"],
        "regex": r"\bnode(?:\.js|js)?\b",
    },
    "Express.js": {
        "category": "Backend",
        "aliases": ["express", "express.js", "expressjs"],
        "regex": r"\bexpress(?:\.js|js)?\b",
    },
    "Django": {
        "category": "Backend",
        "aliases": ["django", "django rest framework", "drf"],
        "regex": r"\bdjango(?:\s+rest\s+framework)?\b|\bdrf\b",
    },
    "Flask": {
        "category": "Backend",
        "aliases": ["flask"],
        "regex": r"\bflask\b",
    },
    "FastAPI": {
        "category": "Backend",
        "aliases": ["fastapi", "fast api"],
        "regex": r"\bfastapi\b|\bfast\s+api\b",
    },
    "Spring Boot": {
        "category": "Backend",
        "aliases": ["spring boot", "spring framework", "spring mvc"],
        "regex": r"\bspring\s+(?:boot|framework|mvc)\b",
    },
    "REST APIs": {
        "category": "Backend",
        "aliases": ["rest api", "restful api", "restful", "rest apis", "rest web services"],
        "regex": r"\brest(?:ful)?\s*(?:api|apis|web\s+services)?\b",
    },
    "GraphQL": {
        "category": "Backend",
        "aliases": ["graphql", "graph ql", "apollo"],
        "regex": r"\bgraphql\b|\bapollo\s+graphql\b",
    },
    "Microservices": {
        "category": "Backend",
        "aliases": ["microservices", "microservice architecture"],
        "regex": r"\bmicroservices?\b",
    },
    ".NET / ASP.NET": {
        "category": "Backend",
        "aliases": [".net", "asp.net", "dotnet", ".net core"],
        "regex": r"\b(?:\.?net|asp\.net)(?:\s*core)?\b|\bdotnet\b",
    },

    # ── Databases & Storage ─────────────────────────────────────────────────
    "MySQL": {
        "category": "Databases",
        "aliases": ["mysql"],
        "regex": r"\bmysql\b",
    },
    "PostgreSQL": {
        "category": "Databases",
        "aliases": ["postgresql", "postgres"],
        "regex": r"\bpostgres(?:ql)?\b",
    },
    "MongoDB": {
        "category": "Databases",
        "aliases": ["mongodb", "mongo"],
        "regex": r"\bmongo(?:db)?\b",
    },
    "SQLite": {
        "category": "Databases",
        "aliases": ["sqlite", "sqlite3"],
        "regex": r"\bsqlite(?:3)?\b",
    },
    "Redis": {
        "category": "Databases",
        "aliases": ["redis"],
        "regex": r"\bredis\b",
    },
    "Oracle DB": {
        "category": "Databases",
        "aliases": ["oracle", "oracle database", "oracle db"],
        "regex": r"\boracle(?:\s+(?:database|db))?\b",
    },
    "Firebase": {
        "category": "Databases",
        "aliases": ["firebase", "firestore"],
        "regex": r"\bfirebase\b|\bfirestore\b",
    },
    "Elasticsearch": {
        "category": "Databases",
        "aliases": ["elasticsearch", "elk stack"],
        "regex": r"\belasticsearch\b|\belk\s+stack\b",
    },

    # ── Cloud, DevOps & Tools ───────────────────────────────────────────────
    "AWS": {
        "category": "Cloud & DevOps",
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda"],
        "regex": r"\baws\b|\bamazon\s+web\s+services\b|\b(?:ec2|s3|lambda|dynamodb|cloudfront)\b",
    },
    "Azure": {
        "category": "Cloud & DevOps",
        "aliases": ["azure", "microsoft azure"],
        "regex": r"\b(?:microsoft\s+)?azure\b",
    },
    "Google Cloud": {
        "category": "Cloud & DevOps",
        "aliases": ["gcp", "google cloud", "google cloud platform"],
        "regex": r"\bgcp\b|\bgoogle\s+cloud(?:\s+platform)?\b",
    },
    "Docker": {
        "category": "Cloud & DevOps",
        "aliases": ["docker", "containerization"],
        "regex": r"\bdocker\b|\bcontainerization\b",
    },
    "Kubernetes": {
        "category": "Cloud & DevOps",
        "aliases": ["kubernetes", "k8s"],
        "regex": r"\bkubernetes\b|\bk8s\b",
    },
    "Git": {
        "category": "Cloud & DevOps",
        "aliases": ["git", "github", "gitlab"],
        "regex": r"\bgit\b|\bgitlab\b|\bversion\s+control\b",
    },
    "CI/CD": {
        "category": "Cloud & DevOps",
        "aliases": ["ci/cd", "continuous integration", "github actions", "jenkins"],
        "regex": r"\bci\/cd\b|\bcontinuous\s+integration\b|\bgithub\s+actions\b|\bjenkins\b",
    },
    "Linux": {
        "category": "Cloud & DevOps",
        "aliases": ["linux", "ubuntu", "centos", "redhat", "unix"],
        "regex": r"\blinux\b|\bubuntu\b|\bunix\b|\bcentos\b",
    },
    "Postman": {
        "category": "Cloud & DevOps",
        "aliases": ["postman", "api testing"],
        "regex": r"\bpostman\b|\bapi\s+testing\b",
    },

    # ── AI, Data Science & Machine Learning ─────────────────────────────────
    "Machine Learning": {
        "category": "AI / Data Science",
        "aliases": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
        "regex": r"\bmachine\s+learning\b|\bml\b(?=\s*[,/|&])",
    },
    "Deep Learning": {
        "category": "AI / Data Science",
        "aliases": ["deep learning", "neural networks", "cnn", "rnn", "lstm"],
        "regex": r"\bdeep\s+learning\b|\bneural\s+networks?\b|\bcnn\b|\brnn\b|\blstm\b",
    },
    "PyTorch": {
        "category": "AI / Data Science",
        "aliases": ["pytorch", "torch"],
        "regex": r"\bpytorch\b|\btorch\b",
    },
    "TensorFlow": {
        "category": "AI / Data Science",
        "aliases": ["tensorflow", "tf", "keras"],
        "regex": r"\btensorflow\b|\bkeras\b",
    },
    "Scikit-Learn": {
        "category": "AI / Data Science",
        "aliases": ["scikit-learn", "sklearn"],
        "regex": r"\bscikit-learn\b|\bsklearn\b",
    },
    "Pandas": {
        "category": "AI / Data Science",
        "aliases": ["pandas"],
        "regex": r"\bpandas\b",
    },
    "NumPy": {
        "category": "AI / Data Science",
        "aliases": ["numpy"],
        "regex": r"\bnumpy\b",
    },
    "Data Analysis": {
        "category": "AI / Data Science",
        "aliases": ["data analysis", "exploratory data analysis", "eda"],
        "regex": r"\bdata\s+analysis\b|\bexploratory\s+data\s+analysis\b|\beda\b",
    },
    "Data Visualization": {
        "category": "AI / Data Science",
        "aliases": ["data visualization", "matplotlib", "seaborn", "tableau", "power bi"],
        "regex": r"\bdata\s+visualization\b|\bmatplotlib\b|\bseaborn\b|\btableau\b|\bpower\s*bi\b",
    },
    "Natural Language Processing": {
        "category": "AI / Data Science",
        "aliases": ["nlp", "natural language processing", "spacy", "nltk", "hugging face", "transformers"],
        "regex": r"\bnatural\s+language\s+processing\b|\bnlp\b|\bhugging\s*face\b|\btransformers\b|\bnltk\b|\bspacy\b",
    },
    "Computer Vision": {
        "category": "AI / Data Science",
        "aliases": ["computer vision", "opencv", "object detection", "yolo"],
        "regex": r"\bcomputer\s+vision\b|\bopencv\b|\byolo\b|\bobject\s+detection\b",
    },
    "Statistics": {
        "category": "AI / Data Science",
        "aliases": ["statistics", "probability", "statistical modeling"],
        "regex": r"\bstatistics\b|\bstatistical\s+modeling\b|\bprobability\b",
    },
    "Big Data": {
        "category": "AI / Data Science",
        "aliases": ["spark", "apache spark", "hadoop", "pyspark", "bigquery"],
        "regex": r"\bapache\s+spark\b|\bspark\b|\bpyspark\b|\bhadoop\b|\bbigquery\b",
    },

    # ── Core Computer Science & Methodologies ────────────────────────────────
    "DSA": {
        "category": "Core CS & Concepts",
        "aliases": ["data structures", "algorithms", "dsa", "data structures and algorithms"],
        "regex": r"\bdata\s+structures?(?:\s*(?:&|and)\s*algorithms)?\b|\bdsa\b|\balgorithms\b",
    },
    "DBMS": {
        "category": "Core CS & Concepts",
        "aliases": ["dbms", "database management", "database management system", "normalization"],
        "regex": r"\bdbms\b|\bdatabase\s+management(?:\s+systems?)?\b|\bnormalization\b|\brdbms\b",
    },
    "OOP": {
        "category": "Core CS & Concepts",
        "aliases": ["oop", "oops", "object oriented programming", "object-oriented programming"],
        "regex": r"\boop[s]?\b|\bobject[- ]oriented\s+programming\b",
    },
    "Operating Systems": {
        "category": "Core CS & Concepts",
        "aliases": ["operating systems", "os concepts", "multithreading", "concurrency"],
        "regex": r"\boperating\s+systems?\b|\bmultithreading\b|\bconcurrency\b",
    },
    "Computer Networks": {
        "category": "Core CS & Concepts",
        "aliases": ["computer networks", "tcp/ip", "networking", "http/https"],
        "regex": r"\bcomputer\s+networks?\b|\btcp\/ip\b|\bhttp\/https\b",
    },
    "System Design": {
        "category": "Core CS & Concepts",
        "aliases": ["system design", "high level design", "low level design", "hld", "lld"],
        "regex": r"\bsystem\s+design\b|\bhigh\s+level\s+design\b|\blow\s+level\s+design\b",
    },
    "Software Testing": {
        "category": "Core CS & Concepts",
        "aliases": ["software testing", "unit testing", "selenium", "pytest", "cypress", "junit", "test automation"],
        "regex": r"\bsoftware\s+testing\b|\bunit\s+testing\b|\bselenium\b|\bpytest\b|\bcypress\b|\bjunit\b|\btest\s+automation\b",
    },
    "Agile / Scrum": {
        "category": "Core CS & Concepts",
        "aliases": ["agile", "scrum", "jira"],
        "regex": r"\bagile\b|\bscrum\b|\bjira\b",
    },
}

# Merge / override with entries from skill_dictionary.json (if present)
_json_skills = _load_skill_taxonomy()
if _json_skills:
    SKILL_TAXONOMY.update(_json_skills)


# ==============================================================================
# 2. ROLE DEFINITIONS WITH REQUIRED & PREFERRED SKILLS
# ==============================================================================

ROLE_PROFILES: Dict[str, Dict[str, Any]] = {
    "frontend developer": {
        "title": "Frontend Developer",
        "required": ["JavaScript", "HTML", "CSS", "React", "Git"],
        "preferred": ["TypeScript", "Next.js", "Redux", "Tailwind CSS", "REST APIs", "Webpack / Vite"],
    },
    "backend developer": {
        "title": "Backend Developer",
        "required": ["SQL", "REST APIs", "DBMS", "Git"],
        # Language requirement: at least one of Python/Java/Node.js/C++/Go
        "language_alternatives": ["Python", "Java", "Node.js", "C++", "Go", "C#"],
        "preferred": ["Docker", "Redis", "FastAPI", "Django", "Spring Boot", "Express.js", "Microservices", "AWS"],
    },
    "full stack developer": {
        "title": "Full Stack Developer",
        "required": ["JavaScript", "React", "Node.js", "SQL", "Git", "REST APIs"],
        "preferred": ["TypeScript", "MongoDB", "Docker", "Redux", "AWS", "Next.js", "CI/CD"],
    },
    "ai/ml engineer": {
        "title": "AI/ML Engineer",
        "required": ["Python", "Machine Learning", "Scikit-Learn", "Deep Learning", "Pandas", "NumPy"],
        "preferred": ["PyTorch", "TensorFlow", "Natural Language Processing", "Computer Vision", "SQL", "Docker", "Data Visualization"],
    },
    "data analyst": {
        "title": "Data Analyst",
        "required": ["SQL", "Python", "Data Analysis", "Data Visualization", "Statistics"],
        "preferred": ["Pandas", "NumPy", "DBMS", "Big Data", "Machine Learning"],
    },
    "software developer": {
        "title": "Software Developer",
        "required": ["DSA", "OOP", "DBMS", "Git"],
        "language_alternatives": ["Python", "Java", "C++", "JavaScript", "C#"],
        "preferred": ["Operating Systems", "Computer Networks", "REST APIs", "SQL", "System Design"],
    },
    "qa engineer": {
        "title": "QA Engineer",
        "required": ["Software Testing", "Git"],
        "language_alternatives": ["Python", "Java", "JavaScript"],
        "preferred": ["SQL", "CI/CD", "Postman", "Agile / Scrum"],
    },
}


# Standard Headings Mapping for boundary preservation
SECTION_HEADINGS = {
    "education": [
        "education", "academic background", "academic qualifications",
        "academic history", "qualifications", "educational background",
        "academics", "educational qualifications", "scholastic record",
    ],
    "skills": [
        "technical skills", "skills", "core competencies", "technical expertise",
        "skills & tools", "technologies", "key skills", "proficiencies",
        "tools & technologies", "technical summary", "areas of expertise",
        "skills and tools", "technical proficiency", "competencies",
        "skills summary", "core skills", "professional skills",
    ],
    "projects": [
        "projects", "academic projects", "personal projects", "project experience",
        "key projects", "technical projects", "capstone projects",
        "side projects", "portfolio projects", "project work",
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "employment history", "work history", "career summary",
        "professional summary", "career history",
    ],
    "internship": [
        "internship", "internships", "internship experience", "industrial training",
        "practical training", "summer internship", "training experience",
    ],
    "certifications": [
        "certifications", "certificates", "licenses and certifications",
        "licenses & certifications", "courses completed", "professional certifications",
        "online courses", "accreditations", "courses and certifications",
        "courses & certifications", "training", "training and certifications",
        "training & certifications", "credentials", "professional development",
        "courses", "certification", "certificate", "certified courses",
        "relevant certifications", "licenses", "relevant courses",
    ],
    "contact": [
        "contact", "contact information", "contact details", "personal details",
        "personal information", "bio data", "biodata",
    ],
    "achievements": [
        "achievements", "awards", "accomplishments", "honors", "extracurricular",
        "co-curricular", "coding profiles", "activities",
        "awards and achievements", "honors and awards", "extracurricular activities",
        "extra-curricular", "positions of responsibility",
    ],
    "declaration": [
        "declaration", "statement", "references",
        "disclaimer", "self declaration", "self-declaration",
    ],
    "summary": [
        "summary", "objective", "career objective", "profile summary",
        "about me", "professional summary", "profile", "about",
    ],
    "publications": [
        "publications", "research", "research papers", "papers",
        "research publications", "journal papers",
    ],
    "hobbies": [
        "hobbies", "interests", "hobbies and interests",
        "hobbies & interests", "personal interests",
    ],
    "languages": [
        "languages", "languages known", "language proficiency",
    ],
    "miscellaneous": [
        "distractor sentences", "distractors", "distractor", "miscellaneous",
        "notes", "additional notes", "other", "other information", "additional information",
    ],
}


# ==============================================================================
# 3. ROBUST DOCUMENT PARSING (PDF & DOCX)
# ==============================================================================

def extract_resume_text(filename: str, content: bytes) -> Tuple[str, List[str], bool]:
    """
    Extract readable text from a PDF or DOCX resume.
    Preserves line breaks and structure.
    For scanned/image-only PDFs, falls back to pytesseract OCR if available.
    Returns (cleaned_text, parsing_warnings, ocr_used).
    """
    warnings: List[str] = []
    ocr_used: bool = False
    extension = os.path.splitext(filename)[1].lower()

    if extension not in [".pdf", ".docx", ".doc"]:
        raise ValueError("Upload a PDF or DOCX resume.")

    if extension == ".doc":
        raise ValueError(
            "Legacy .doc format is not directly supported. "
            "Please open Word and save/export the file as .docx or .pdf."
        )

    text = ""
    try:
        if extension == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                from PyPDF2 import PdfReader

            reader = PdfReader(io.BytesIO(content))

            if reader.is_encrypted:
                raise ValueError("This PDF is password-protected. Upload an unlocked PDF.")

            page_texts = []
            for idx, page in enumerate(reader.pages):
                try:
                    ptxt = page.extract_text() or ""
                    page_texts.append(ptxt)
                except Exception:
                    warnings.append(f"Could not extract text cleanly from page {idx + 1}.")

            text = "\n\n".join(page_texts)

            # ── OCR Fallback for scanned/image-only PDFs ──────────────────────
            alpha_chars_raw = len(re.findall(r"[A-Za-z0-9]", text))
            if alpha_chars_raw < 100 and len(reader.pages) > 0:
                # Attempt OCR with pytesseract + pdf2image
                try:
                    from pdf2image import convert_from_bytes
                    import pytesseract

                    images = convert_from_bytes(content, dpi=200)
                    ocr_pages: List[str] = []
                    for img in images:
                        ocr_pages.append(pytesseract.image_to_string(img, lang="eng"))
                    ocr_text = "\n\n".join(ocr_pages).strip()

                    if len(re.findall(r"[A-Za-z0-9]", ocr_text)) > alpha_chars_raw:
                        text = ocr_text
                        ocr_used = True
                        warnings.append(
                            "This PDF appears to be scanned or image-based. "
                            "OCR (optical character recognition) was used to extract text. "
                            "Accuracy may vary — for best results, upload a digitally-created PDF."
                        )
                except ImportError:
                    warnings.append(
                        "This PDF may be scanned or image-based (very little text detected). "
                        "OCR libraries (pdf2image, pytesseract) are not installed. "
                        "For better results, upload a text-based PDF or DOCX."
                    )
                except Exception as ocr_err:
                    warnings.append(
                        f"OCR attempt failed ({ocr_err}). "
                        "Please upload a text-based PDF or DOCX for accurate parsing."
                    )

        elif extension == ".docx":
            from docx import Document

            document = Document(io.BytesIO(content))
            lines: List[str] = []

            for paragraph in document.paragraphs:
                p_text = paragraph.text.strip()
                if p_text:
                    lines.append(p_text)

            # Extract table cell texts without redundant spam
            for table in document.tables:
                for row in table.rows:
                    cells_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    # Deduplicate adjacent cells if merged
                    deduped_cells = []
                    for c in cells_text:
                        if not deduped_cells or c != deduped_cells[-1]:
                            deduped_cells.append(c)
                    if deduped_cells:
                        lines.append(" | ".join(deduped_cells))

            text = "\n".join(lines)

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Could not read this resume ({str(exc)}). Try exporting it as a new PDF or DOCX.")

    # Clean character artifacts while preserving line structure
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # Detect unreadable or scanned documents (after optional OCR)
    alpha_chars = len(re.findall(r"[A-Za-z0-9]", text))
    if alpha_chars < 60:
        raise ValueError(
            "Unreadable or scanned resume detected. "
            "The document contains insufficient extractable text (<60 characters). "
            "Please upload a text-based PDF or DOCX file."
        )

    if alpha_chars < 200:
        warnings.append(
            "Resume text is unusually sparse (<200 characters). "
            "Ensure sections and project descriptions are fully written."
        )

    return text, warnings, ocr_used


# ==============================================================================
# 4. SECTION BOUNDARY PARSER
# ==============================================================================

def normalize_heading(line: str) -> str:
    """Normalize a candidate section heading line."""
    line = re.sub(r"^[\s•\-|*#]+", "", line)
    line = re.sub(r"[:\s]+$", "", line)
    return re.sub(r"\s+", " ", line).strip().lower()


def _is_section_heading_line(stripped: str) -> bool:
    """Heuristic: heading lines are typically short, upper-case or title-case, and
    contain no bullet/sentence punctuation beyond a trailing colon."""
    if len(stripped) > 60:
        return False
    # Remove leading markers
    core = re.sub(r"^[\s•\-|*#\d.\)]+", "", stripped).strip()
    if not core:
        return False
    # Headings rarely contain commas, semicolons, or sentence-ending periods
    if re.search(r"[,;]", core):
        return False
    return True


def parse_resume_sections(text: str) -> Dict[str, List[str]]:
    """
    Parse resume into labeled sections while preserving boundary integrity.
    Prevents headings from bleeding into preceding or succeeding sections.
    Uses exact matching first, then fuzzy prefix matching for composite headings.
    """
    all_known_headings: Dict[str, str] = {}
    for stype, aliases in SECTION_HEADINGS.items():
        for alias in aliases:
            all_known_headings[alias.lower()] = stype

    sections: Dict[str, List[str]] = {stype: [] for stype in SECTION_HEADINGS}
    sections["general"] = []

    current_section = "general"
    lines = text.split("\n")

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            continue

        norm = normalize_heading(stripped)

        # Check if line is a recognized section heading
        matched_section = None
        if norm in all_known_headings:
            matched_section = all_known_headings[norm]
        else:
            # Check for patterns like "TECHNICAL SKILLS:" or "1. EDUCATION"
            clean_sub = re.sub(r"^\d+[\.\)]\s*", "", norm)
            if clean_sub in all_known_headings:
                matched_section = all_known_headings[clean_sub]

        # Fuzzy prefix matching for composite headings like
        # "CERTIFICATIONS & COURSES" or "Education Details"
        if not matched_section and _is_section_heading_line(stripped):
            for alias, stype in all_known_headings.items():
                if len(alias) >= 5 and (norm.startswith(alias) or alias.startswith(norm)):
                    matched_section = stype
                    break

        if matched_section:
            current_section = matched_section
            continue

        # Prevent section bleed in multi-column or interleaved templates
        if current_section == "certifications":
            if re.search(r"\b(hereby declare|declaration|true to the best of my knowledge)\b", stripped, re.I):
                current_section = "declaration"
                continue
            elif re.search(r"\b(?:personal\s+project|academic\s+project|capstone|web\s+application|portfolio\s+project|application\s*\[)\b|^\s*projects?\s*$", stripped, re.I):
                current_section = "projects"
                sections[current_section].append(stripped)
                continue
            elif re.search(r"^\s*(?:bachelor(?:of)?|master(?:of)?|b\.?tech|b\.?e\b|mca|bca|senior\s+secondary|secondary\s*\(|education\b)\b", stripped, re.I):
                current_section = "education"
                sections[current_section].append(stripped)
                continue
            elif re.search(r"^\s*(?:languages?|programming|frameworks?|databases?|backend|frontend|tools?|ai\s+tools|core\s+cs)\s*:", stripped, re.I):
                current_section = "skills"
                sections[current_section].append(stripped)
                continue
            elif re.search(r"^\s*(?:competitive\s+programming|achievements?|awards?|hackathons?)\b", stripped, re.I):
                current_section = "achievements"
                sections[current_section].append(stripped)
                continue
            elif re.search(r"^\s*(?:links?|profiles?)\s*:?$|^\s*(?:linkedin|github|hackerrank|leetcode)\s*:", stripped, re.I):
                current_section = "contact"
                sections[current_section].append(stripped)
                continue

        # Stop collecting into any section if declaration text appears inline
        if current_section not in ("general", "declaration"):
            if re.search(r"\b(hereby declare|i hereby|declaration|true to best)\b", stripped, re.I):
                current_section = "declaration"
                continue

        sections[current_section].append(stripped)

    return sections


# ==============================================================================
# 5. EVIDENCE-BASED CERTIFICATION EXTRACTION WITH CONFIDENCE
# ==============================================================================

# ── Certification Taxonomy: known issuers, platforms, and cert families ────────
CERTIFICATION_TAXONOMY = {
    # Cloud providers
    "aws": {"issuer": "Amazon Web Services", "patterns": [
        r"\baws\s+certified\b", r"\baws\s+cloud\s+practitioner\b",
        r"\baws\s+solutions?\s+architect\b", r"\baws\s+developer\b",
        r"\baws\s+sysops\b", r"\baws\s+devops\b",
        r"\baws\s+machine\s+learning\b", r"\baws\s+data\s+analytics\b",
        r"\bamazon\s+web\s+services\b",
    ]},
    "azure": {"issuer": "Microsoft", "patterns": [
        r"\bazure\s+(?:fundamentals|administrator|developer|solutions?\s+architect|data\s+engineer|ai\s+engineer|security)\b",
        r"\baz-\d{3}\b", r"\bms-\d{3}\b", r"\bdp-\d{3}\b",
        r"\bmicrosoft\s+certified\b",
    ]},
    "gcp": {"issuer": "Google Cloud", "patterns": [
        r"\bgoogle\s+cloud\s+(?:certified|professional|associate)\b",
        r"\bgcp\s+(?:certified|professional|associate)\b",
        r"\bprofessional\s+(?:cloud|data|machine\s+learning)\s+engineer\b",
    ]},
    "oracle": {"issuer": "Oracle", "patterns": [
        r"\boracle\s+(?:cloud\s*infrastructure|cloudinfrastructure|certified|cloud|associate|professional)\b",
        r"\boci\s+(?:certification|associate|professional|cloud)\b",
        r"\boca\b(?=.*oracle)", r"\bocp\b(?=.*oracle)",
    ]},
    "infosys": {"issuer": "Infosys Springboard", "patterns": [
        r"\binfosys(?:\s*springboard)?\b", r"\bspringboard\b",
    ]},
    # Industry vendors
    "cisco": {"issuer": "Cisco", "patterns": [
        r"\bccna\b", r"\bccnp\b", r"\bccie\b", r"\bcisco\s+certified\b",
    ]},
    "comptia": {"issuer": "CompTIA", "patterns": [
        r"\bcomptia\s+(?:a\+|network\+|security\+|cloud\+|linux\+|server\+|pentest\+|cysa\+|casp\+)\b",
        r"\bcomptia\s+certified\b",
    ]},
    "redhat": {"issuer": "Red Hat", "patterns": [
        r"\bred\s+hat\s+certified\b", r"\brhcsa\b", r"\brhce\b",
    ]},
    "ibm": {"issuer": "IBM", "patterns": [
        r"\bibm\s+(?:certified|professional|data\s+science|ai|cloud)\b",
    ]},
    "salesforce": {"issuer": "Salesforce", "patterns": [
        r"\bsalesforce\s+(?:certified|administrator|developer|consultant)\b",
    ]},
    "linux_foundation": {"issuer": "The Linux Foundation", "patterns": [
        r"\blinux\s+foundation\b", r"\bckad?\b", r"\bcks\b",
    ]},
    "hashicorp": {"issuer": "HashiCorp", "patterns": [
        r"\bhashicorp\s+certified\b", r"\bterraform\s+associate\b",
    ]},
    # MOOC / online platforms
    "coursera": {"issuer": "Coursera", "patterns": [
        r"\bcoursera\b",
    ]},
    "udemy": {"issuer": "Udemy", "patterns": [
        r"\budemy\b",
    ]},
    "edx": {"issuer": "edX", "patterns": [
        r"\bedx\b",
    ]},
    "nptel": {"issuer": "NPTEL", "patterns": [
        r"\bnptel\b", r"\bswayam\b",
    ]},
    "freecodecamp": {"issuer": "freeCodeCamp", "patterns": [
        r"\bfreecodecamp\b",
    ]},
    "udacity": {"issuer": "Udacity", "patterns": [
        r"\budacity\b", r"\bnanodegree\b",
    ]},
    "linkedin_learning": {"issuer": "LinkedIn Learning", "patterns": [
        r"\blinkedin\s+learning\b",
    ]},
    "great_learning": {"issuer": "Great Learning", "patterns": [
        r"\bgreat\s+learning\b",
    ]},
    "deeplearning_ai": {"issuer": "DeepLearning.AI", "patterns": [
        r"\bdeeplearning\.?ai\b", r"\bdeep\s+learning\.?ai\b",
    ]},
    "stanford_online": {"issuer": "Stanford Online", "patterns": [
        r"\bstanford\s+(?:online|certification)\b",
    ]},
    "meta": {"issuer": "Meta", "patterns": [
        r"\bmeta\s+(?:front[- ]?end|back[- ]?end|database|android|ios|react\s+native|marketing)\b",
        r"\bmeta\s+(?:certified|professional|developer)\b",
    ]},
    "google": {"issuer": "Google", "patterns": [
        r"\bgoogle\s+(?:certified|professional|developer|analytics|digital\s+garage|it\s+support|ux\s+design|data\s+analytics|project\s+management|cybersecurity)\b",
    ]},
    "microsoft": {"issuer": "Microsoft", "patterns": [
        r"\bmicrosoft\s+(?:certified|learn|office\s+specialist|mos)\b",
    ]},
    "hackerrank": {"issuer": "HackerRank", "patterns": [
        r"\bhackerrank\b.*(?:certific|problem\s+solving|skill|verified)\b",
        r"(?:certific|problem\s+solving|skill|verified).*\bhackerrank\b",
    ]},
    "scrum": {"issuer": "Scrum.org / Scrum Alliance", "patterns": [
        r"\bcsm\b", r"\bpsm\s*[i]+\b", r"\bcertified\s+scrum\s+master\b",
        r"\bscrum\s+(?:master|developer|product\s+owner)\s+certif\b",
    ]},
    "pmi": {"issuer": "PMI", "patterns": [
        r"\bpmp\b", r"\bcapm\b", r"\bpmi\s+(?:acp|certified)\b",
        r"\bproject\s+management\s+professional\b",
    ]},
    "itil": {"issuer": "Axelos", "patterns": [
        r"\bitil\b",
    ]},
    "istqb": {"issuer": "ISTQB", "patterns": [
        r"\bistqb\b",
    ]},
    "kaggle": {"issuer": "Kaggle", "patterns": [
        r"\bkaggle\s+(?:certificate|progression|expert|master)\b",
    ]},
}

# ── Patterns that DISQUALIFY a line from being a certification ─────────────────
NON_CERT_PATTERNS = [
    # Academic degrees and qualifications
    r"\b(?:bachelor(?:of)?|master(?:of)?|b\.?tech|b\.?e\b|m\.?tech|m\.?e\b|bca|mca|b\.?sc|m\.?sc|bba|mba|diploma|ph\.?d|doctorate)\b",
    r"\b(?:higher\s+secondary|senior\s+secondary|secondary\s*\(|secondary\s+school|sslc|hslc|hsc|cbse|icse|igcse|state\s+board)\b",
    r"\b(?:class\s*(?:x|xii|10|12|xi|11|10th|12th)|10th\b|12th\b|10\+2|plus\s+two|matric(?:ulation)?|high\s+school)\b",
    r"\b(?:degree\s+certificate|mark\s*sheet|transcript|grade\s+card|semester\s+result|provisional\s+certificate)\b",
    r"\b(?:computer\s+science\s+and\s+engineering|information\s+technology|electronics\s+and\s+communication)\b",
    # Academic institutions
    r"\b(?:college|university|institute|institution|vidyalaya|school|campus|polytechnic|academy)\b",
    r"\b(?:bannari\s+amman|vidya\s+nethrra|prg\s+velappa)\b",
    # Graduation years & terms
    r"\b(?:graduated|graduation|passing|passed\s+in|passed\s+out|year\s+of\s+passing|yop|batch\s+of)\b",
    r"\b(?:20\d\d\s*[-–—]\s*20\d\d)|(?:20\d\d\s*[-–—]\s*(?:present|ongoing|current|till\s+date))\b",
    r"^\s*20[12]\d\s*$",
    # Grades, percentages, CGPA
    r"\b(?:percentage|percent|cgpa|gpa|marks|cpi|sgpa)\s*[-:]?\s*[\d.]+%?",
    r"^\s*\d{1,3}(?:\.\d+)?\s*%\s*$",
    # Skills headers & listings
    r"^\s*(?:languages?|programming|frameworks?|libraries|databases?|backend|frontend|tools?|devops|cloud|platforms?|ai\s+tools|core\s+cs|strengths?|soft\s+skills|technical\s+skills|key\s+skills)(?:\s*(?:&|and)\s*\w+)*\s*:",
    # Summary & objective headings
    r"\b(?:professional\s+summary|career\s+summary|profile\s+summary|career\s+objective|summary\s+statement)\b",
    r"^\s*(?:summary|objective|profile|experience\s*(&|and)?\s*projects)\s*$",
    # Work Experience, Internships, Company names
    r"\b(?:internship|intern\b|technohacks|pvt\s+ltd|solutions\s+pvt|accepted\s+offer|offer\s+accepted|internship\s+offer|job\s+offer)\b",
    r"\b(?:full[- ]?stack\s+developer|software\s+engineer|web\s+developer|frontend\s+developer|backend\s+developer)\b",
    # Projects & Project Bullets
    r"\b(?:personal\s+project|academic\s+project|capstone|web\s+application|portfolio\s+project|number\s+guessing\s+game)\b",
    r"^\s*[-•●◦▪▸|*]?\s*(?:designed\s+and|developed\s+an?|built\s+responsive|built\s+real|conducted\s+user|implemented|optimized\s+database|deployed\s+on|built\s+a\s+console)\b",
    r"^\s*[-•●◦▪▸|*]?\s*(?:shows\s+feedback|includes\s+a|learned\s+basic)\b",
    r"\b(?:solved\s+\d+|problems\s+on\s+hackerrank|practicing\s+leetcode|arrays,\s*strings|linked\s+lists)\b",
    # Full URLs or bare links
    r"https?://",
    r"www\.[a-z0-9-]+\.[a-z]{2,}",
    # Profile domains
    r"\b(?:github|linkedin|hackerrank|leetcode|codechef|codeforces|geeksforgeeks|kaggle|gitlab|bitbucket|stackoverflow)\.(?:com|io|org)\b",
    r"(?:linkedin\.com|github\.com|hackerrank\.com|leetcode\.com)\/[A-Za-z0-9._-]+",
    r"^\s*(?:linkedin|github|hackerrank|leetcode|codechef|codeforces)\s*:",
    # Declarations and personal details
    r"\b(?:hereby\s+declare|i\s+hereby|declaration|particulars\s+are\s+true|true\s+to\s+the\s+best|father'?s?\s+name|mother'?s?\s+name|date\s+of\s+birth|d\.?o\.?b\.?|permanent\s+address|nationality|marital\s+status|language[s]?\s+known|blood\s+group)\b",
    r"^\s*(?:place|date|signature)\s*:\s*",
    # Bare section headings
    r"^\s*(?:certifications?|certificates?|courses?|licenses?|achievements?|skills?|education|declaration|references?|training|credentials?|links|contact|career\s+objective|summary|recognition)\s*$",
    # Standalone contacts
    r"^\s*[\+]?\d[\d\s\-]{7,15}\s*$",
    r"^\s*[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\s*$",
    # Hobbies
    r"\b(?:hobbies|interests|reading|travelling|cricket|football|music|cooking|gaming|photography|swimming|dancing|singing|drawing|painting)\b",
]

LEGIT_CERT_INDICATORS = [
    r"\b(?:certified|certification|certificate|accredited|credential|credentialed|licensed?)\b",
    r"\b(?:specialization|bootcamp|foundation|associate|practitioner|professional)\b",
    r"\b(?:nanodegree|verified|badge|completion|course\s+certificate|elite\s+certificate)\b",
    r"\b(?:ccna|ccnp|ccie|rhcsa|rhce|pmp|capm|itil|istqb|csm|psm|togaf)\b",
]

_ISSUER_PREFIX = re.compile(
    r"^\s*(?:by|issued\s+by|offered\s+by|from|platform|provider)\s*:?\s*(.+)$", re.I
)
_CREDENTIAL_ID_PATTERN = re.compile(
    r"(?:credential\s*(?:id|#)|cert(?:ificate)?\s*(?:id|#)|verification\s*(?:id|code|url)|verify\s+at)\s*:?\s*(.+)", re.I
)
_DATE_PATTERN = re.compile(
    r"^\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4})\s*$", re.I
)


def _clean_cert_line(raw: str) -> str:
    """Strip bullet markers, leading numbering, and extra whitespace from a certification line."""
    line = re.sub(r"^[\s•●◦▪▸\-|*#→➤►✓✔⮞]+", "", raw)
    line = re.sub(r"^\d+[\.\)\]]\s*", "", line)
    return line.strip()


def _is_disqualified(line: str) -> bool:
    """Check if a line matches any non-certification pattern."""
    stripped = line.strip()
    if len(stripped) < 4:
        return True
    # Disqualify sentence fragments (starts with lowercase or ends with sentence punctuation)
    if stripped[0].islower() or stripped.endswith((".", ",", ";")):
        return True
    # Disqualify unbalanced or bracketed tags like [Accepted, Offer]
    if "[" in stripped or "]" in stripped:
        return True
    # Disqualify comma-separated lists of tech tools (e.g. "React.js, Node.js, Express.js, MongoDB")
    if "," in stripped and not any(kw in stripped.lower() for kw in ["certified", "certificate", "certification", "license", "associate", "specialization"]):
        parts = [p.strip() for p in stripped.split(",") if p.strip()]
        if len(parts) >= 3:
            return True
    for pat in NON_CERT_PATTERNS:
        if re.search(pat, line, re.I):
            return True
    return False


def _has_cert_indicator(line: str) -> bool:
    """Check if a line contains a positive certification indicator."""
    return any(re.search(pat, line, re.I) for pat in LEGIT_CERT_INDICATORS)


def _identify_issuer(line: str) -> Optional[str]:
    """Try to extract the issuing organization from taxonomy matches."""
    line_lower = line.lower()
    for _key, info in CERTIFICATION_TAXONOMY.items():
        for pat in info["patterns"]:
            if re.search(pat, line_lower):
                return info["issuer"]
    return None


def _score_cert_confidence(line: str, source_section: str, has_issuer_match: bool) -> Tuple[str, float]:
    """
    Score confidence that a line is a genuine certification.
    Requires positive evidence (issuer or cert keywords) to reach high or medium.
    """
    score = 0.0

    if has_issuer_match:
        score += 0.45

    if _has_cert_indicator(line):
        score += 0.35

    if source_section == "certifications":
        score += 0.15

    cleaned_len = len(line.strip())
    if 8 <= cleaned_len <= 100:
        score += 0.10
    elif cleaned_len > 120:
        score -= 0.15

    word_count = len(line.split())
    if word_count > 15:
        score -= 0.20
    if re.search(r"\b(?:using|worked|developed|built|designed|implemented|created|managed)\b", line, re.I):
        score -= 0.30

    # Without at least an issuer match or a positive cert keyword,
    # confidence cannot exceed low / uncertain (prevents false positive verification).
    if not has_issuer_match and not _has_cert_indicator(line):
        return "low", min(0.28, max(0.10, score))

    if score >= 0.55:
        return "high", min(0.99, score)
    elif score >= 0.35:
        return "medium", score
    else:
        return "low", score


def extract_certifications(
    sections: Dict[str, List[str]], full_text: str
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    """
    Universal evidence-based certification extraction with confidence scoring.

    Returns a 3-tuple:
        - confirmed: List of high/medium-confidence certification records (dicts)
        - uncertain: List of low-confidence candidates needing review (dicts)
        - warnings: List of extraction warning strings

    Each certification record contains:
        - title: str (cleaned certification name)
        - issuer: Optional[str] (identified issuing organization)
        - source_section: str (section the cert was found in)
        - confidence: str ('high', 'medium', or 'low')
        - confidence_score: float (numeric confidence)
        - source_text: str (original line from document)
        - credential_id: Optional[str]
    """
    warnings: List[str] = []
    cert_lines = sections.get("certifications", [])
    all_candidates: List[Dict[str, Any]] = []
    seen_titles: set = set()

    def _record_candidate(
        title: str,
        issuer: Optional[str],
        source_section: str,
        source_text: str,
        credential_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        norm_title = re.sub(r"\s+", " ", title).lower().strip()
        if not norm_title or norm_title in seen_titles:
            return None
        if _is_disqualified(title):
            return None

        # Check for duplicate containment (e.g., "AWS Certified" vs "AWS Certified Cloud Practitioner")
        for existing in seen_titles:
            if norm_title in existing or existing in norm_title:
                if len(norm_title) <= len(existing):
                    return None

        seen_titles.add(norm_title)

        has_issuer = bool(issuer)
        confidence, conf_score = _score_cert_confidence(title, source_section, has_issuer)

        return {
            "title": title.strip(),
            "issuer": issuer,
            "source_section": source_section,
            "confidence": confidence,
            "confidence_score": round(conf_score, 3),
            "source_text": source_text.strip(),
            "credential_id": credential_id,
        }

    # ── Stage 1: Process lines in Certifications section with lookahead grouping ─
    cleaned_cert_lines = [_clean_cert_line(l) for l in cert_lines if _clean_cert_line(l)]
    i = 0
    while i < len(cleaned_cert_lines):
        line = cleaned_cert_lines[i]
        if _is_disqualified(line):
            i += 1
            continue

        issuer = _identify_issuer(line)
        has_kw = _has_cert_indicator(line)

        # Lookahead: is next line an issuer sub-line or title continuation?
        next_issuer = None
        next_is_continuation = False
        if i + 1 < len(cleaned_cert_lines):
            nxt = cleaned_cert_lines[i + 1]
            iss_m = _ISSUER_PREFIX.match(nxt)
            if iss_m:
                next_issuer = _identify_issuer(nxt) or iss_m.group(1).strip()
            elif (
                len(nxt) < 50
                and _has_cert_indicator(nxt)
                and not _is_disqualified(nxt)
                and not _identify_issuer(nxt)
            ):
                next_is_continuation = True

        if next_is_continuation:
            combined_title = f"{line} {cleaned_cert_lines[i + 1]}"
            combined_issuer = _identify_issuer(combined_title) or issuer
            cand = _record_candidate(
                combined_title,
                combined_issuer,
                "certifications",
                f"{line} {cleaned_cert_lines[i + 1]}"
            )
            if cand:
                all_candidates.append(cand)
            i += 2
            continue
        elif next_issuer:
            combined_issuer = next_issuer or issuer
            cand = _record_candidate(
                line,
                combined_issuer,
                "certifications",
                f"{line} {cleaned_cert_lines[i + 1]}"
            )
            if cand:
                all_candidates.append(cand)
            i += 2
            continue
        elif issuer or has_kw:
            cand = _record_candidate(line, issuer, "certifications", line)
            if cand:
                all_candidates.append(cand)
            i += 1
            continue
        else:
            # Candidate in certifications section without immediate provider/keyword:
            # Recorded as uncertain (low confidence) candidate for user review.
            cand = _record_candidate(line, None, "certifications", line)
            if cand:
                all_candidates.append(cand)
            i += 1

    # ── Stage 2: Full-text scan for high-confidence certifications ────────────
    # Catches multi-column or misparsed section layouts where valid certs fell outside
    full_lines = [_clean_cert_line(l) for l in full_text.splitlines() if _clean_cert_line(l)]
    j = 0
    while j < len(full_lines):
        line = full_lines[j]
        if _is_disqualified(line):
            j += 1
            continue

        issuer = _identify_issuer(line)
        has_kw = _has_cert_indicator(line)

        # Check for multi-line continuation in full text
        next_issuer = None
        next_is_continuation = False
        if j + 1 < len(full_lines):
            nxt = full_lines[j + 1]
            iss_m = _ISSUER_PREFIX.match(nxt)
            if iss_m:
                next_issuer = _identify_issuer(nxt) or iss_m.group(1).strip()
            elif (
                len(nxt) < 50
                and _has_cert_indicator(nxt)
                and not _is_disqualified(nxt)
                and not _identify_issuer(nxt)
            ):
                next_is_continuation = True

        if (issuer and has_kw) or (issuer and len(line) <= 60) or (next_issuer and (has_kw or len(line) <= 60)):
            if next_is_continuation:
                combined_title = f"{line} {full_lines[j + 1]}"
                cand = _record_candidate(
                    combined_title,
                    _identify_issuer(combined_title) or issuer,
                    "full_scan",
                    f"{line} {full_lines[j + 1]}"
                )
                if cand:
                    all_candidates.append(cand)
                j += 2
                continue
            elif next_issuer:
                cand = _record_candidate(
                    line,
                    next_issuer or issuer,
                    "full_scan",
                    f"{line} {full_lines[j + 1]}"
                )
                if cand:
                    all_candidates.append(cand)
                j += 2
                continue
            else:
                cand = _record_candidate(line, issuer, "full_scan", line)
                if cand:
                    all_candidates.append(cand)
                j += 1
                continue

        j += 1

    # ── Stage 3: Split into Confirmed (high/med) vs Uncertain (low) ───────────
    confirmed: List[Dict[str, Any]] = []
    uncertain: List[Dict[str, Any]] = []

    for cand in all_candidates:
        if cand["confidence"] in ("high", "medium"):
            confirmed.append(cand)
        else:
            uncertain.append(cand)

    confirmed = confirmed[:15]
    uncertain = uncertain[:10]

    # ── Stage 4: User-facing extraction warnings ──────────────────────────────
    if not cert_lines and not confirmed and not uncertain:
        pass  # No certifications found
    elif cert_lines and not confirmed and not uncertain:
        warnings.append(
            "A Certifications section was detected, but no valid certifications could be extracted. "
            "Academic degrees, college names, graduation years, and declaration statements were filtered out."
        )
    elif uncertain and not confirmed:
        warnings.append(
            f"{len(uncertain)} possible certification item(s) were found with low confidence. "
            "Please review them to verify whether they represent genuine certifications."
        )

    return confirmed, uncertain, warnings


def extract_certifications_flat(
    sections: Dict[str, List[str]], full_text: str
) -> List[str]:
    """
    Backward-compatible flat list extraction.
    Returns only confirmed certification title strings (high/medium confidence).
    Used by legacy callers that expect List[str].
    """
    confirmed, _uncertain, _warnings = extract_certifications(sections, full_text)
    return [c["title"] for c in confirmed]


# ==============================================================================
# 6. CONTEXT-AWARE SKILL EXTRACTION WITH EVIDENCE
# ==============================================================================

def extract_skills_with_evidence(
    text: str,
    sections: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Extract skills using word boundaries, multi-token regex, and context awareness.
    Provides verifiable sentence evidence and categories for each detected skill.
    Prevents false matches (e.g., 'C' in etc, 'Go' as verb, 'Java' in JavaScript).
    """
    # Remove URLs and emails before scanning so domains like reactjs.org don't create false matches
    sanitized_text = re.sub(r"https?://\S+|www\.\S+|\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", " ", text)

    detected_skills: Dict[str, Dict[str, Any]] = {}
    skills_section_text = " ".join(sections.get("skills", []))
    projects_section_text = " ".join(sections.get("projects", []))
    experience_section_text = " ".join(sections.get("experience", []) + sections.get("internship", []))

    # Split sanitized text into sentences/lines for evidence extraction
    raw_lines = [l.strip() for l in sanitized_text.splitlines() if len(l.strip()) > 3]

    def find_evidence_snippet(skill_name: str, regex_pattern: str) -> Tuple[str, str, str]:
        """Find best evidence line and identify which section it originated from."""
        best_line = ""
        found_section = "General"
        confidence = "medium"

        # Check Technical Skills section first
        for l in sections.get("skills", []):
            if re.search(regex_pattern, l, re.I):
                best_line = l
                found_section = "Skills"
                confidence = "high"
                break

        # Check Projects section (great evidence!)
        if not best_line:
            for l in sections.get("projects", []):
                if re.search(regex_pattern, l, re.I):
                    best_line = l
                    found_section = "Projects"
                    confidence = "high"
                    break

        # Check Experience / Internships
        if not best_line:
            for l in sections.get("experience", []) + sections.get("internship", []):
                if re.search(regex_pattern, l, re.I):
                    best_line = l
                    found_section = "Experience"
                    confidence = "high"
                    break

        # Check full text
        if not best_line:
            for l in raw_lines:
                if re.search(regex_pattern, l, re.I):
                    best_line = l
                    found_section = "Resume Body"
                    confidence = "medium"
                    break

        if not best_line:
            best_line = f"Mentioned in resume ({skill_name})"

        # Trim evidence length
        if len(best_line) > 160:
            best_line = best_line[:157] + "..."

        return best_line, found_section, confidence

    # Iterate through skill taxonomy
    for canonical_name, spec in SKILL_TAXONOMY.items():
        regex_pat = spec["regex"]

        # Special verification for short/tricky skills
        if canonical_name == "C":
            # Must appear in skills section, or explicit C/C++, C programming
            is_matched = False
            if re.search(r"\bc\s+programming\b|\bc\s+language\b|\bc\/c\+\+\b", sanitized_text, re.I):
                is_matched = True
            elif skills_section_text:
                for s_line in sections.get("skills", []):
                    if re.search(r"\b(?:vitamin|grade|class|physics|chemistry|supplemental|section)\b", s_line, re.I):
                        continue
                    if re.search(r"(?<![A-Za-z0-9#+])C(?![A-Za-z0-9#+])", s_line):
                        is_matched = True
                        break

            if is_matched:
                ev_line, sec, conf = find_evidence_snippet("C", r"(?<![A-Za-z0-9#+])C(?![A-Za-z0-9#+])")
                detected_skills[canonical_name] = {
                    "skill": canonical_name,
                    "category": spec["category"],
                    "evidence": ev_line,
                    "section": sec,
                    "confidence": conf,
                }
            continue

        if canonical_name == "Go":
            # Avoid verb 'go to', only accept Golang or Go inside skills/tech list
            if re.search(r"\bgolang\b|\bgo\s+language\b", sanitized_text, re.I):
                ev_line, sec, conf = find_evidence_snippet("Go", r"\bgolang\b|\bgo\s+language\b")
                detected_skills[canonical_name] = {
                    "skill": canonical_name,
                    "category": spec["category"],
                    "evidence": ev_line,
                    "section": sec,
                    "confidence": conf,
                }
            elif skills_section_text and re.search(r"(?<!\w)Go(?!\w)", skills_section_text):
                ev_line, sec, conf = find_evidence_snippet("Go", r"(?<!\w)Go(?!\w)")
                detected_skills[canonical_name] = {
                    "skill": canonical_name,
                    "category": spec["category"],
                    "evidence": ev_line,
                    "section": sec,
                    "confidence": conf,
                }
            continue

        if canonical_name == "R":
            # Avoid single letter R unless in skills section or explicit R programming
            if re.search(r"\br\s+programming\b|\br\s+language\b", sanitized_text, re.I):
                ev_line, sec, conf = find_evidence_snippet("R", r"\br\s+programming\b|\br\s+language\b")
                detected_skills[canonical_name] = {
                    "skill": canonical_name,
                    "category": spec["category"],
                    "evidence": ev_line,
                    "section": sec,
                    "confidence": conf,
                }
            elif skills_section_text and re.search(r"(?<!\w)R(?!\w)", skills_section_text):
                ev_line, sec, conf = find_evidence_snippet("R", r"(?<!\w)R(?!\w)")
                detected_skills[canonical_name] = {
                    "skill": canonical_name,
                    "category": spec["category"],
                    "evidence": ev_line,
                    "section": sec,
                    "confidence": conf,
                }
            continue

        # Standard regex matching for all other skills
        if re.search(regex_pat, sanitized_text, re.I):
            ev_line, sec, conf = find_evidence_snippet(canonical_name, regex_pat)
            detected_skills[canonical_name] = {
                "skill": canonical_name,
                "category": spec["category"],
                "evidence": ev_line,
                "section": sec,
                "confidence": conf,
            }

    # Group skills by domain category
    categorized: Dict[str, List[str]] = {}
    for skill_info in detected_skills.values():
        cat = skill_info["category"]
        categorized.setdefault(cat, []).append(skill_info["skill"])

    return {
        "skills_list": list(detected_skills.keys()),
        "skills_details": detected_skills,
        "skills_by_category": categorized,
    }


# ==============================================================================
# 7. CANDIDATE PROFILE CLASSIFIER & EXPERIENCE EVALUATION
# ==============================================================================

def evaluate_experience_and_profile(
    text: str,
    sections: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Distinguishes fresher vs experienced candidates.
    Ensures freshers with academic projects/internships are not penalized with 0.
    """
    exp_lines = sections.get("experience", [])
    intern_lines = sections.get("internship", [])
    proj_lines = sections.get("projects", [])
    edu_lines = sections.get("education", [])

    exp_content = " ".join(exp_lines).strip()
    intern_content = " ".join(intern_lines).strip()

    has_internship = False
    if len(intern_content) > 15:
        # Check that it is not placeholder
        if not re.search(r"\b(no internship|nil|n/?a|none)\b", intern_content, re.I):
            has_internship = True
    elif re.search(r"\b(intern|internship|trainee|interned)\b", exp_content, re.I):
        has_internship = True

    # Check for real professional full-time experience
    has_fulltime_experience = False
    evidence_verbs = [
        "worked as", "full-time", "software engineer", "developer", "responsibilities",
        "employed at", "team lead", "production deployment", "maintained systems",
    ]
    if len(exp_content) > 40 and not re.search(r"\b(no experience|fresher|seeking opportunity)\b", exp_content, re.I):
        if any(re.search(rf"\b{re.escape(v)}\b", exp_content, re.I) for v in evidence_verbs):
            if not re.search(r"^\s*intern", exp_content, re.I):
                has_fulltime_experience = True

    # Detect fresher signals
    is_fresher = True
    if has_fulltime_experience and not has_internship:
        is_fresher = False
    elif re.search(r"\b(fresher|entry level|graduate student|b\.?tech student|undergraduate)\b", text, re.I):
        is_fresher = True
    elif len(exp_lines) == 0 and (len(proj_lines) > 0 or len(edu_lines) > 0):
        is_fresher = True

    # Calculate experience score fairly
    if is_fresher:
        if has_internship:
            experience_score = 90
            exp_note = "Strong internship & practical training detected for fresher profile."
        elif len(proj_lines) >= 4:
            experience_score = 75
            exp_note = "Fresher profile: High practical readiness demonstrated through multiple technical projects."
        elif len(proj_lines) >= 2:
            experience_score = 65
            exp_note = "Fresher profile: Academic projects present. Consider an internship to further strengthen."
        else:
            experience_score = 50
            exp_note = "Fresher profile: Add more hands-on technical projects or internship training."
    else:
        if has_fulltime_experience:
            experience_score = 95
            exp_note = "Professional industry work experience verified."
        else:
            experience_score = 60
            exp_note = "Limited verified work experience descriptions."

    return {
        "is_fresher": is_fresher,
        "candidate_type": "Fresher / Campus Graduate" if is_fresher else "Experienced Professional",
        "has_internship": has_internship,
        "has_real_experience": has_fulltime_experience or has_internship,
        "experience_score": experience_score,
        "experience_note": exp_note,
    }


# ==============================================================================
# 8. ROLE-SPECIFIC SKILL ANALYSIS
# ==============================================================================

def analyze_role_skills(
    detected_skills: List[str],
    role_name_or_id: Optional[str] = None,
    db_requirements: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Matches detected skills against role requirements.
    Outputs: matched, missing required, missing preferred, and uncertain skills.
    """
    role_key = (role_name_or_id or "").lower().strip()

    # Find matching role profile
    matched_role_key = None
    for k in ROLE_PROFILES:
        if k in role_key or role_key in k:
            matched_role_key = k
            break

    profile = ROLE_PROFILES.get(matched_role_key) if matched_role_key else None

    # Normalization helper
    detected_lower = {s.lower(): s for s in detected_skills}

    # If role not found in pre-defined profiles, construct from db_requirements
    if not profile and db_requirements:
        custom_reqs = []
        for req in db_requirements:
            sname = str(req.get("skill_name", "")).strip()
            # Map readiness names like 'dsa' -> 'DSA', 'dbms' -> 'DBMS'
            for canon, spec in SKILL_TAXONOMY.items():
                if sname.lower() in [a.lower() for a in spec["aliases"]] or sname.lower() == canon.lower():
                    custom_reqs.append(canon)
                    break
            else:
                if sname:
                    custom_reqs.append(sname.title())

        profile = {
            "title": role_name_or_id or "Target Role",
            "required": custom_reqs or ["DSA", "SQL", "Git"],
            "preferred": ["Docker", "REST APIs", "AWS"],
        }

    if not profile:
        # General analysis fallback
        return {
            "role_title": "General Software Profile",
            "matched_skills": detected_skills,
            "missing_required": [],
            "missing_preferred": [],
            "uncertain_skills": [],
            "match_ratio": 1.0,
        }

    role_title = profile["title"]
    required_specs = profile.get("required", [])
    preferred_specs = profile.get("preferred", [])
    language_alternatives = profile.get("language_alternatives", [])

    matched_skills: List[str] = []
    missing_required: List[str] = []
    missing_preferred: List[str] = []
    uncertain_skills: List[str] = []

    # Check required skills
    for req in required_specs:
        if req.lower() in detected_lower:
            matched_skills.append(req)
        else:
            missing_required.append(req)

    # Check language alternatives (e.g. backend requires at least one of Python/Java/Node/C++)
    if language_alternatives:
        found_any_lang = False
        for lang in language_alternatives:
            if lang.lower() in detected_lower:
                if lang not in matched_skills:
                    matched_skills.append(lang)
                found_any_lang = True
        if not found_any_lang:
            missing_required.append(f"Core Language ({' / '.join(language_alternatives[:3])})")

    # Check preferred skills
    for pref in preferred_specs:
        if pref.lower() in detected_lower:
            if pref not in matched_skills:
                matched_skills.append(pref)
        else:
            missing_preferred.append(pref)

    # Check uncertain skills (detected outside main skills/projects or low frequency)
    for s in detected_skills:
        if s not in matched_skills and s not in required_specs and s not in preferred_specs:
            uncertain_skills.append(s)

    # Calculate match ratio
    total_req_count = max(1, len(required_specs) + (1 if language_alternatives else 0))
    req_matched_count = len([s for s in matched_skills if s in required_specs or s in language_alternatives])
    match_ratio = min(1.0, req_matched_count / total_req_count)

    return {
        "role_title": role_title,
        "matched_skills": matched_skills,
        "missing_required": missing_required,
        "missing_preferred": missing_preferred,
        "uncertain_skills": uncertain_skills,
        "match_ratio": round(match_ratio, 2),
    }


# ==============================================================================
# 9. ATS-STYLE SCORING WITH EXPLANATIONS
# ==============================================================================

def calculate_ats_score(
    text: str,
    sections: Dict[str, List[str]],
    detected_skills: List[str],
    role_analysis: Dict[str, Any],
    profile_info: Dict[str, Any],
    certifications: List[str],
) -> Dict[str, Any]:
    """
    Calculate transparent, weighted ATS score based on:
    - Skills (role coverage)
    - Projects (tech depth, action verbs, metrics)
    - Experience / Internships (fresher-friendly)
    - Education (degree, university, GPA)
    - Structure & Completeness (formatting, contact, readability)
    """
    text_lower = text.lower()
    is_fresher = profile_info["is_fresher"]

    # 1. Skills Score (0 - 100)
    has_role = bool(role_analysis.get("missing_required") or role_analysis.get("missing_preferred"))
    if has_role:
        match_ratio = role_analysis.get("match_ratio", 0.5)
        matched_pref = len([s for s in role_analysis.get("matched_skills", []) if s in role_analysis.get("missing_preferred", [])])
        skills_score = int(min(100, (match_ratio * 80) + (matched_pref * 5) + (len(detected_skills) * 1.5)))
    else:
        # General: scale by skill breadth
        skills_score = int(min(100, len(detected_skills) * 8 + 20))

    # 2. Projects Score (0 - 100)
    proj_lines = sections.get("projects", [])
    proj_text = " ".join(proj_lines)

    proj_score = 0
    if len(proj_lines) >= 2:
        proj_score += 45
    elif len(proj_lines) == 1:
        proj_score += 25

    # Check for strong action verbs
    action_verbs = [r"\bbuilt\b", r"\bdeveloped\b", r"\bimplemented\b", r"\bdesigned\b", r"\barchitected\b", r"\bdeployed\b"]
    verb_matches = sum(1 for v in action_verbs if re.search(v, proj_text, re.I))
    proj_score += min(25, verb_matches * 6)

    # Check for measurable metrics (% or numbers)
    if re.search(r"\b\d+%\b|\b\d+\s*(?:ms|users|requests|x|fold)\b", proj_text, re.I):
        proj_score += 20
    elif re.search(r"\b\d+\b", proj_text):
        proj_score += 10

    # Tech stack mentioned in project bullets
    if any(s.lower() in proj_text.lower() for s in detected_skills):
        proj_score += 10

    projects_score = min(100, max(20 if len(proj_lines) > 0 else 0, proj_score))

    # 3. Education Score (0 - 100)
    edu_lines = sections.get("education", [])
    edu_text = " ".join(edu_lines)

    edu_score = 0
    if len(edu_lines) > 0 or re.search(r"\b(education|academic background|degree)\b", text_lower):
        edu_score += 40

    if re.search(r"\b(b\.?tech|b\.?e|m\.?tech|mca|bca|b\.?sc|master|bachelor)\b", edu_text, re.I):
        edu_score += 30

    if re.search(r"\b(college|university|institute)\b", edu_text, re.I):
        edu_score += 15

    if re.search(r"\b(cgpa|gpa|percentage|20\d\d)\b", edu_text, re.I):
        edu_score += 15

    education_score = min(100, edu_score)

    # 4. Experience Score (from profile evaluation)
    experience_score = profile_info["experience_score"]

    # 5. Structure & Completeness Score (0 - 100)
    has_contact = bool(re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text))
    has_phone = bool(re.search(r"\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b|\b\d{10}\b", text))
    has_links = bool(re.search(r"github\.com|linkedin\.com", text, re.I))

    comp_score = 0
    if has_contact: comp_score += 20
    if has_phone: comp_score += 15
    if has_links: comp_score += 15
    if len(sections.get("skills", [])) > 0: comp_score += 15
    if len(sections.get("projects", [])) > 0: comp_score += 15
    if len(sections.get("education", [])) > 0: comp_score += 10
    if len(certifications) > 0: comp_score += 10

    completeness_score = min(100, comp_score)

    # 6. Overall Weighted ATS Score
    # For Freshers: weight projects & skills higher, do not penalize lack of fulltime corporate job
    if is_fresher:
        overall_score = round(
            (skills_score * 0.35) +
            (projects_score * 0.30) +
            (experience_score * 0.15) +
            (education_score * 0.10) +
            (completeness_score * 0.10)
        )
        formula_explanation = (
            "Fresher-Optimized Weighting: Skills (35%) + Projects (30%) + "
            "Internship/Practical Experience (15%) + Education (10%) + Structure (10%). "
            "Freshers are not penalized for lack of multi-year corporate employment."
        )
    else:
        overall_score = round(
            (skills_score * 0.30) +
            (experience_score * 0.30) +
            (projects_score * 0.20) +
            (education_score * 0.10) +
            (completeness_score * 0.10)
        )
        formula_explanation = (
            "Industry Professional Weighting: Skills (30%) + Experience (30%) + "
            "Projects (20%) + Education (10%) + Structure (10%)."
        )

    overall_score = max(10, min(99, overall_score))

    breakdown_details = {
        "skills": {
            "score": skills_score,
            "weight": "35%" if is_fresher else "30%",
            "detail": f"{len(role_analysis.get('matched_skills', []))} role skills matched. {len(detected_skills)} total skills verified.",
        },
        "projects": {
            "score": projects_score,
            "weight": "30%" if is_fresher else "20%",
            "detail": f"Evaluated project section depth, engineering verbs, and measurable impact.",
        },
        "experience": {
            "score": experience_score,
            "weight": "15%" if is_fresher else "30%",
            "detail": profile_info["experience_note"],
        },
        "education": {
            "score": education_score,
            "weight": "10%",
            "detail": "Verified degree, institution, and graduation criteria.",
        },
        "completeness": {
            "score": completeness_score,
            "weight": "10%",
            "detail": "Assessed contact info, links, ATS section headers, and formatting.",
        },
    }

    # Generate Actionable Improvement Suggestions
    suggestions: List[Dict[str, str]] = []

    if role_analysis.get("missing_required"):
        missing_top = role_analysis["missing_required"][:4]
        suggestions.append({
            "area": "Target Role Requirements",
            "tip": f"Add demonstrable project evidence for essential role skills: {', '.join(missing_top)}.",
        })

    if projects_score < 75:
        suggestions.append({
            "area": "Project Quantifiable Impact",
            "tip": "Include measurable metrics in project bullets (e.g., 'Reduced response time by 40%', 'Handled 500+ requests').",
        })

    if not has_links:
        suggestions.append({
            "area": "Professional Profiles",
            "tip": "Add active GitHub repository and LinkedIn profile links to validate your code and achievements.",
        })

    if not certifications:
        suggestions.append({
            "area": "Certifications",
            "tip": "Consider acquiring verified certifications (e.g. AWS Certified, Coursera, Meta, HackerRank) to validate core skills.",
        })

    if is_fresher and not profile_info["has_internship"]:
        suggestions.append({
            "area": "Practical Experience",
            "tip": "Complete a software internship or contribute to open-source to strengthen real-world industry experience.",
        })

    return {
        "overall_score": overall_score,
        "skills_score": skills_score,
        "projects_score": projects_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "completeness_score": completeness_score,
        "breakdown_details": breakdown_details,
        "formula_explanation": formula_explanation,
        "improvement_suggestions": suggestions,
    }
