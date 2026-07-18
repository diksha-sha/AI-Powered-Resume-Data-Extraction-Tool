import json
import re
import ollama

DEFAULT_DATA = {
    "name": "NA",
    "email": "NA",
    "phone": "NA",
    "location": "NA",
    "education": "NA",
    "college": "NA",
    "university": "NA",
    "cgpa": "NA",
    "experience": "NA",
    "internships": "NA",
    "projects": [],
    "certifications": [],
    "technical_skills": [],
    "soft_skills": [],
    "languages": [],
    "linkedin": "NA",
    "github": "NA",
    "portfolio": "NA"
}


def clean_json(response_text):

    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")
    response_text = response_text.strip()

    match = re.search(r"\{.*\}", response_text, re.DOTALL)

    if not match:
        raise Exception("No JSON object returned.")

    return match.group(0)


def normalize_list(value):

    if value in [None, "", "NA"]:
        return []

    if isinstance(value, list):

        cleaned = []

        for item in value:

            item = str(item).strip()

            if item and item not in cleaned:
                cleaned.append(item)

        return cleaned

    return [str(value)]


def normalize_string(value):

    if value is None:
        return "NA"

    value = str(value).strip()

    if value == "":
        return "NA"

    return value


def ai_extract_resume(text):

    # Enough for 2–3 page resumes
    text = text[:7000]

    prompt = f"""
You are an expert ATS Resume Parser.

Read the resume carefully.

Extract ONLY the information explicitly mentioned.

Rules:

- Return ONLY ONE JSON object.
- Do NOT explain.
- Do NOT think.
- Do NOT include markdown.
- Do NOT include a domain field.
- Never guess information.
- Missing values must be "NA".
- Arrays must always remain arrays.

Extract:

Personal Information
- name
- email
- phone
- location

Education
- education
- college
- university
- cgpa

Experience
- experience (Example: "3 Years")
- internships

Projects

Certifications

Technical Skills

Soft Skills

Languages

LinkedIn

GitHub

Portfolio

Return exactly

{{
"name":"",
"email":"",
"phone":"",
"location":"",
"education":"",
"college":"",
"university":"",
"cgpa":"",
"experience":"",
"internships":"",
"projects":[],
"certifications":[],
"technical_skills":[],
"soft_skills":[],
"languages":[],
"linkedin":"",
"github":"",
"portfolio":""
}}

Resume

{text}
"""

    for attempt in range(2):

        try:

            response = ollama.chat(

                model="llama3:latest",

                messages=[
                    {
                        "role": "system",
                        "content": "You are a JSON API. Respond ONLY with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature": 0,
                    "top_p": 0.9,
                    "num_predict": 260,
                    "num_ctx": 4096
                }

            )

            answer = response["message"]["content"]

            print("\n========== RAW AI RESPONSE ==========\n")
            print(answer)
            print("\n=====================================\n")

            answer = clean_json(answer)

            data = json.loads(answer)

            # Remove accidental domain
            data.pop("domain", None)

            # Ensure every field exists
            for key in DEFAULT_DATA:

                if key not in data:
                    data[key] = DEFAULT_DATA[key]

            # Normalize string fields
            string_fields = [
                "name",
                "email",
                "phone",
                "location",
                "education",
                "college",
                "university",
                "cgpa",
                "experience",
                "internships",
                "linkedin",
                "github",
                "portfolio"
            ]

            for field in string_fields:
                data[field] = normalize_string(data[field])

            # Normalize list fields
            list_fields = [
                "projects",
                "certifications",
                "technical_skills",
                "soft_skills",
                "languages"
            ]

            for field in list_fields:
                data[field] = normalize_list(data[field])

            # Experience formatting
            if data["experience"] != "NA":

                m = re.search(r"\d+", data["experience"])

                if m:
                    data["experience"] = f"{m.group()} Years"

            return data

        except Exception as e:

            print(f"\nAttempt {attempt + 1} failed")
            print(e)

    print("\nAI Extraction Failed\n")

    return DEFAULT_DATA.copy()