import re

from resume_parser.skills import SKILLS
from resume_parser.education import DEGREES
from resume_parser.softskills import SOFT_SKILLS
from resume_parser.languages import LANGUAGES


# -----------------------------
# NAME
# -----------------------------

def extract_name(text):

    lines = text.split("\n")

    for line in lines[:8]:

        line = line.strip()

        if not line:
            continue

        if "@" in line:
            continue

        if any(ch.isdigit() for ch in line):
            continue

        if "linkedin" in line.lower():
            continue

        if "github" in line.lower():
            continue

        words = re.sub(r"[^A-Za-z ]", "", line).split()

        if 2 <= len(words) <= 4:
            return " ".join(words)

    return "NA"


# -----------------------------
# EMAIL
# -----------------------------

def extract_email(text):

    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)

    return match.group(0) if match else "NA"


# -----------------------------
# PHONE
# -----------------------------

def extract_phone(text):

    match = re.search(r'(\+91[\-\s]?)?[6-9]\d{9}', text)

    return match.group(0) if match else "NA"


# -----------------------------
# LINKEDIN
# -----------------------------

def extract_linkedin(text):

    match = re.search(r'https?://(?:www\.)?linkedin\.com/[^\s]+', text)

    return match.group(0) if match else "NA"


# -----------------------------
# GITHUB
# -----------------------------

def extract_github(text):

    match = re.search(r'https?://(?:www\.)?github\.com/[^\s]+', text)

    return match.group(0) if match else "NA"


# -----------------------------
# PORTFOLIO
# -----------------------------

def extract_portfolio(text):

    urls = re.findall(r'https?://[^\s]+', text)

    for url in urls:

        if "linkedin" not in url.lower() and "github" not in url.lower():

            return url

    return "NA"


# -----------------------------
# EDUCATION
# -----------------------------

def extract_education(text):

    lower = text.lower()

    for degree in DEGREES:

        if degree.lower() in lower:

            return degree

    return "NA"


# -----------------------------
# COLLEGE
# -----------------------------

def extract_college(text):

    for line in text.split("\n"):

        if any(word in line.lower() for word in ["college", "institute", "school"]):

            return line.strip()

    return "NA"


# -----------------------------
# UNIVERSITY
# -----------------------------

def extract_university(text):

    for line in text.split("\n"):

        if "university" in line.lower():

            return line.strip()

    return "NA"


# -----------------------------
# CGPA
# -----------------------------

def extract_cgpa(text):

    patterns = [

        r'CGPA[:\s]*([0-9]\.[0-9]{1,2})',

        r'([0-9]\.[0-9]{1,2})\s*/\s*10'

    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            return match.group(1)

    return "NA"


# -----------------------------
# EXPERIENCE
# -----------------------------

def extract_experience(text):

    match = re.search(r'(\d+)\+?\s+years?', text, re.IGNORECASE)

    if match:

        return match.group(1) + " Years"

    return "NA"


# -----------------------------
# TECHNICAL SKILLS
# -----------------------------

def extract_skills(text):

    lower = text.lower()

    found = []

    for skill in SKILLS:

        if skill.lower() in lower:

            found.append(skill)

    return sorted(set(found))


# -----------------------------
# SOFT SKILLS
# -----------------------------

def extract_soft_skills(text):

    lower = text.lower()

    found = []

    for skill in SOFT_SKILLS:

        if skill.lower() in lower:

            found.append(skill)

    return sorted(set(found))


# -----------------------------
# LANGUAGES
# -----------------------------

def extract_languages(text):

    lower = text.lower()

    found = []

    for language in LANGUAGES:

        if language.lower() in lower:

            found.append(language)

    return sorted(set(found))


# -----------------------------
# DOMAIN
# -----------------------------

def detect_domain(skills):

    skills = [s.lower() for s in skills]

    if "python" in skills:

        return "Python Developer"

    if "java" in skills:

        return "Java Developer"

    if "react" in skills:

        return "Frontend Developer"

    if "node.js" in skills:

        return "Backend Developer"

    if "power bi" in skills:

        return "Data Analyst"

    if "machine learning" in skills:

        return "Machine Learning Engineer"

    if "sql" in skills and "python" in skills:

        return "Data Scientist"

    return "General"


# -----------------------------
# MAIN
# -----------------------------

def extract_resume_data(text):

    skills = extract_skills(text)

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": extract_education(text),

        "college": extract_college(text),

        "university": extract_university(text),

        "cgpa": extract_cgpa(text),

        "experience": extract_experience(text),

        "technical_skills": skills,

        "soft_skills": extract_soft_skills(text),

        "languages": extract_languages(text),

        "linkedin": extract_linkedin(text),

        "github": extract_github(text),

        "portfolio": extract_portfolio(text),

        "domain": detect_domain(skills)

    }