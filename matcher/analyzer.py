
import re
import PyPDF2
from docx import Document


# Extract text from a PDF or Word resume
def extract_resume_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif filename.endswith(".docx"):
        document = Document(uploaded_file)
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + " "

        return text

    raise ValueError("Only PDF and DOCX files are supported.")


# Common names and variations for the same skill
SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "django": ["django"],
    "django rest framework": [
        "django rest framework",
        "django-rest-framework",
        "drf",
    ],
    "javascript": ["javascript", "js"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "mysql": ["mysql"],
    "sql": ["sql", "structured query language"],
    "rest api": ["rest api", "restful api", "rest apis"],
    "git": ["git"],
    "github": ["github"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "excel": ["excel", "microsoft excel"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "linux": ["linux"],
    "bootstrap": ["bootstrap"],
    "jquery": ["jquery", "j query"],
    "postman": ["postman"],
    "docker": ["docker"],
    "java": ["java"],
    "c++": ["c++"],
    "flask": ["flask"],
    "fastapi": ["fastapi", "fast api"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "power bi": ["power bi", "powerbi"],
    "communication": ["communication", "communication skills"],
    "problem solving": ["problem solving", "problem-solving"],
    "debugging": ["debugging", "debug"],
}


def contains_skill(text, aliases):
    for alias in aliases:
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


# Compare resume skills with job requirements
def calculate_match(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    required_skills = []
    matched_skills = []
    missing_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if contains_skill(job_description, aliases):
            required_skills.append(skill)

    for skill in required_skills:
        aliases = SKILL_ALIASES[skill]

        if contains_skill(resume_text, aliases):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if required_skills:
        score = round(
            len(matched_skills) / len(required_skills) * 100
        )
    else:
        score = 0

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


def get_skill_suggestions(missing_skills):
    suggestions = {
        "python": "Practice Python basics, functions, loops, and small projects.",
        "django": "Build a Django CRUD application with models, views, and templates.",
        "django rest framework": "Learn serializers, API views, and CRUD REST APIs.",
        "javascript": "Practice DOM manipulation, events, functions, and async JavaScript.",
        "html": "Learn semantic HTML, forms, and page structure.",
        "css": "Practice Flexbox, Grid, responsive design, and media queries.",
        "react": "Learn components, props, state, and React hooks.",
        "mysql": "Practice SQL queries, joins, grouping, and database relationships.",
        "sql": "Practice SELECT, INSERT, UPDATE, DELETE, and JOIN queries.",
        "rest api": "Learn HTTP methods, status codes, JSON, and API requests.",
        "git": "Practice commits, branches, merging, and resolving conflicts.",
        "github": "Upload projects and write clear README files on GitHub.",
        "machine learning": "Start with Python, pandas, scikit-learn, and basic ML models.",
        "data analysis": "Practice cleaning and analyzing datasets using pandas.",
        "excel": "Learn formulas, lookup functions, pivot tables, and charts.",
        "aws": "Learn cloud basics, IAM, storage, and deploying a simple application.",
        "azure": "Explore Azure fundamentals and deploy a basic web application.",
        "linux": "Practice terminal commands, file permissions, and process management.",
        "bootstrap": "Build responsive layouts using Bootstrap components and utilities.",
        "jquery": "Practice selectors, events, and DOM manipulation.",
        "postman": "Practice sending API requests and checking responses in Postman.",
        "docker": "Learn images, containers, Dockerfiles, and basic commands.",
        "java": "Practice Java syntax, object-oriented programming, and collections.",
        "c++": "Practice C++ fundamentals, functions, classes, and STL basics.",
        "flask": "Build a small Flask application with routes and templates.",
        "fastapi": "Build API endpoints and learn request validation with FastAPI.",
        "pandas": "Practice filtering, grouping, and cleaning data with pandas.",
        "numpy": "Practice arrays, indexing, and numerical operations with NumPy.",
        "power bi": "Learn data modelling, Power Query, and interactive dashboards.",
        "communication": "Practice explaining your projects clearly and giving short presentations.",
        "problem solving": "Solve beginner coding problems and explain your approach.",
        "debugging": "Practice reading error messages and using breakpoints to find bugs.",
    }

    results = []

    for skill in missing_skills:
        suggestion = suggestions.get(
            skill.lower(),
            f"Learn the fundamentals of {skill} and practise with a small project."
        )
        results.append({
            "skill": skill,
            "suggestion": suggestion
        })

    return results


def check_resume_quality(resume_text):
    """
    Check important sections and details in a resume.
    Returns a quality score, found sections, missing sections,
    and improvement suggestions.
    """

    text = resume_text.lower()

    sections = {
        "Contact Information": [
            "email", "phone", "mobile", "contact"
        ],
        "Education": [
            "education", "qualification", "academic"
        ],
        "Technical Skills": [
            "skills", "technical skills", "technologies"
        ],
        "Projects": [
            "projects", "project"
        ],
        "Work Experience": [
            "experience", "employment", "internship"
        ],
        "Certifications": [
            "certification", "certifications", "certificate"
        ],
    }

    found_sections = []
    missing_sections = []

    for section, keywords in sections.items():
        if any(keyword in text for keyword in keywords):
            found_sections.append(section)
        else:
            missing_sections.append(section)

    total_sections = len(sections)
    quality_score = round(
        len(found_sections) / total_sections * 100
    )

    suggestions = []

    for section in missing_sections:
        suggestions.append(
            f"Consider adding a clear {section} section if relevant."
        )

    if len(text.split()) < 100:
        suggestions.append(
            "Your resume text is quite short. Consider adding "
            "relevant details about your skills, education, and projects."
        )

    if not suggestions:
        suggestions.append(
            "Your resume contains the main sections checked. "
            "Review it for accuracy and clear descriptions of your achievements."
        )

    return {
        "quality_score": quality_score,
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "quality_suggestions": suggestions,
    }

import re


def check_ats_resume(resume_text, job_description=""):
    text = resume_text.lower()

    sections = {
        "Skills": ["skills", "technical skills"],
        "Education": ["education", "academic qualification"],
        "Experience": ["experience", "work experience", "employment"],
        "Projects": ["projects", "personal projects"],
    }

    found_sections = []
    missing_sections = []

    for section, keywords in sections.items():
        if any(keyword in text for keyword in keywords):
            found_sections.append(section)
        else:
            missing_sections.append(section)

    email_found = bool(
        re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text)
    )

    phone_found = bool(
        re.search(r"(?:\+?\d[\d\s()-]{8,}\d)", resume_text)
    )

    job_keywords = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
        job_description.lower()
    )

    resume_words = set(re.findall(r"\b\w+\b", text))
    important_keywords = {
        word for word in job_keywords
        if word in {
            "python", "django", "mysql", "javascript",
            "html", "css", "api", "git", "github", "react"
        }
    }

    matched_keywords = sorted(important_keywords & resume_words)
    missing_keywords = sorted(important_keywords - resume_words)

    score = 0
    score += 40 * len(found_sections) / len(sections)
    score += 20 if email_found else 0
    score += 20 if phone_found else 0

    if important_keywords:
        score += 20 * len(matched_keywords) / len(important_keywords)
    else:
        score += 20

    return {
        "ats_score": round(score),
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "email_found": email_found,
        "phone_found": phone_found,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }
