SKILLS = [

    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",


    "Flask",
    "Django",
    "React",
    "Angular",
    "Node.js",

  
    "MySQL",
    "MongoDB",
    "Oracle",
    "SQLite",


    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "NLP",


    "Pandas",
    "NumPy",
    "Matplotlib",
    "Power BI",
    "Tableau",
    "Excel",


    "Git",
    "GitHub",
    "VS Code",
    "Linux",

  
    "AWS",
    "Azure",
    "Google Cloud"

]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def detect_domain(skills):

    skills = [skill.lower() for skill in skills]

    if "python" in skills:
        return "Python Developer"

    elif "react" in skills or "javascript" in skills or "html" in skills or "css" in skills:
        return "Frontend Developer"

    elif "flask" in skills or "django" in skills:
        return "Backend Developer"

    elif "machine learning" in skills or "deep learning" in skills or "tensorflow" in skills:
        return "Machine Learning Engineer"

    elif "mongodb" in skills or "mysql" in skills or "sql" in skills:
        return "Database Developer"

    elif "aws" in skills or "azure" in skills or "google cloud" in skills:
        return "Cloud Engineer"

    return "General"