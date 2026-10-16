
from .analyzer import SKILL_ALIASES, contains_skill


JOB_ROLES = {
    "Python Developer": {
        "skills": ["python", "django", "sql", "git"],
        "description": "Develop Python applications and backend systems.",
    },
    "Django Developer": {
        "skills": ["python", "django", "mysql", "rest api"],
        "description": "Build web applications using Django and databases.",
    },
    "Backend Developer": {
        "skills": ["python", "sql", "rest api", "git"],
        "description": "Build server-side logic, APIs, and data systems.",
    },
    "Frontend Developer": {
        "skills": ["html", "css", "javascript", "react"],
        "description": "Create interactive and responsive website interfaces.",
    },
    "Full Stack Developer": {
        "skills": ["python", "django", "html", "css", "javascript", "sql"],
        "description": "Work on both frontend and backend development.",
    },
    "Data Analyst": {
        "skills": ["python", "sql", "excel", "data analysis"],
        "description": "Analyze data and prepare useful reports.",
    },
    "Machine Learning Intern": {
        "skills": ["python", "machine learning", "pandas", "numpy"],
        "description": "Explore datasets and build introductory ML models.",
    },
    "Technical Support Engineer": {
        "skills": ["linux", "sql", "communication", "debugging"],
        "description": "Troubleshoot technical issues and support applications.",
    },
}


def recommend_jobs(resume_text, limit=5):
    resume_text = resume_text.lower()
    recommendations = []

    for role, details in JOB_ROLES.items():
        matched = []

        for skill in details["skills"]:
            aliases = SKILL_ALIASES.get(skill, [skill])

            if contains_skill(resume_text, aliases):
                matched.append(skill)

        total_skills = len(details["skills"])
        score = round(len(matched) / total_skills * 100)

        missing = [
            skill for skill in details["skills"]
            if skill not in matched
        ]

        recommendations.append({
            "title": role,
            "description": details["description"],
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
        })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return recommendations[:limit]
