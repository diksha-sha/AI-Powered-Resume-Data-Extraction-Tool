from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory
)

import os
from datetime import datetime
from resume_parser.parser import extract_text
#from resume_parser.extractor import extract_resume_data
from database.db import resume_collection
from resume_parser.extractor import extract_resume_data
import threading
from ai_worker import process_resume

app = Flask(__name__)

# ==========================
# Configuration
# ==========================

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================
# Dashboard
# ==========================

@app.route("/")
def dashboard():

    resumes = list(resume_collection.find())

    total_resumes = len(resumes)

    uploaded_today = 0

    today = datetime.now().date()

    domains = set()

    skills = set()

    recent_activity = []

    for doc in resumes:

        # --------------------------
        # Uploaded Today
        # --------------------------

        upload_date = doc.get("upload_date")

        if upload_date and upload_date.date() == today:
            uploaded_today += 1

        # --------------------------
        # Domain Count
        # --------------------------

        domain = doc.get("domain")

        if domain and domain != "NA":
            domains.add(domain)

        # --------------------------
        # Technical Skills
        # --------------------------

        technical = doc.get("technical_skills", [])

        if isinstance(technical, list):

            for skill in technical:

                skill = str(skill).strip()

                if skill and skill != "NA":
                    skills.add(skill)

        else:

            for skill in str(technical).split(","):

                skill = skill.strip()

                if skill and skill != "NA":
                    skills.add(skill)

        # --------------------------
        # Soft Skills
        # --------------------------

        soft = doc.get("soft_skills", [])

        if isinstance(soft, list):

            for skill in soft:

                skill = str(skill).strip()

                if skill and skill != "NA":
                    skills.add(skill)

        else:

            for skill in str(soft).split(","):

                skill = skill.strip()

                if skill and skill != "NA":
                    skills.add(skill)

        # --------------------------
        # Recent Activity
        # --------------------------

        recent_activity.append({

            "filename": doc.get(
                "original_filename",
                doc.get("stored_filename", "Unknown Resume")
            ),

            "date": upload_date if upload_date else datetime.now()

        })

    recent_activity.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return render_template(

        "dashboard.html",

        total_resumes=total_resumes,

        total_domains=len(domains),

        total_skills=len(skills),

        uploaded_today=uploaded_today,

        recent_activity=recent_activity[:5]

    )

# ==========================
# Upload Resume
# ==========================

#@app.route("/upload", methods=["GET", "POST"])
#def upload():

 #   if request.method == "POST":

  #      if "resume" not in request.files:
   #         return redirect(url_for("upload"))

    #    files = request.files.getlist("resume")

     #   if len(files) == 0:
       #     return redirect(url_for("upload"))

        #uploaded_count = 0

       # for file in files:

        #    if file.filename == "":
         #       continue

            # Create unique filename
          #  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

           # stored_filename = f"{timestamp}_{file.filename}"

            #save_path = os.path.join(
             #   app.config["UPLOAD_FOLDER"],
              #  stored_filename
            #)

            # Save file
         #   file.save(save_path)

            # Extract text
            #text = extract_text(save_path)

            # Extract resume data
            #data = extract_resume_data(text)

            # Save into MongoDB
           # resume_collection.insert_one({

          #      "original_filename": file.filename,

         #       "stored_filename": stored_filename,

          #      "upload_date": datetime.now(),

         #       **data

        #    })

       #     uploaded_count += 1

     #   print(f"{uploaded_count} Resume(s) Uploaded Successfully")
#
     #   return redirect(url_for("upload"))

# ==========================
# Upload Resume
# ==========================

# ==========================
# Upload Resume
# ==========================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if "resume" not in request.files:
            return redirect(url_for("upload"))

        files = request.files.getlist("resume")

        # Domain selected from dropdown
        selected_domain = request.form.get("domain", "General")

        for file in files:

            if file.filename == "":
                continue

            # -------------------------
            # Create Unique Filename
            # -------------------------

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

            stored_filename = f"{timestamp}_{file.filename}"

            save_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                stored_filename
            )

            # -------------------------
            # Save Resume
            # -------------------------

            file.save(save_path)

            # -------------------------
            # Save Initial Record
            # -------------------------

            resume_collection.insert_one({

                "original_filename": file.filename,

                "stored_filename": stored_filename,

                "upload_date": datetime.now(),

                "selected_domain": selected_domain,

                "status": "Processing"

            })

            # -------------------------
            # Start AI Worker
            # -------------------------

            thread = threading.Thread(

                target=process_resume,

                args=(stored_filename, save_path, selected_domain)

            )

            thread.daemon = True

            thread.start()

            print(
                f"{file.filename} uploaded with domain '{selected_domain}'. AI processing started."
            )

        return redirect(url_for("upload"))

    # ==========================
    # Display Uploaded Resumes
    # ==========================

    resumes = []

    for doc in resume_collection.find().sort("upload_date", -1):

        resumes.append({

            "filename": doc.get(
                "original_filename",
                "Unknown Resume"
            ),

            "stored_filename": doc.get(
                "stored_filename",
                ""
            ),

            "selected_domain": doc.get(
                "selected_domain",
                "General"
            ),

            "date": doc.get(
                "upload_date",
                datetime.now()
            ).strftime("%d-%m-%Y %I:%M %p"),

            "status": doc.get(
                "status",
                "Completed"
            )

        })

    return render_template(
        "upload.html",
        resumes=resumes
    )

def format_list(value):

    if value == "NA" or value is None:
        return "NA"

    if isinstance(value, str):
        return value

    if isinstance(value, list):

        formatted = []

        for item in value:

            if isinstance(item, dict):

                if "title" in item:
                    formatted.append(item["title"])

                elif "name" in item:
                    formatted.append(item["name"])

                else:
                    formatted.append(str(item))

            else:
                formatted.append(str(item))

        return ", ".join(formatted)

    return str(value)

# ==========================
# Extracted Data
# ==========================

# ==========================
# Extracted Data
# ==========================

def format_list(value):

    if value is None or value == "NA":
        return "NA"

    if isinstance(value, str):
        return value

    if isinstance(value, list):

        result = []

        for item in value:

            if isinstance(item, dict):

                if "title" in item:
                    result.append(item["title"])

                elif "name" in item:
                    result.append(item["name"])

                elif "description" in item:
                    result.append(item["description"])

                else:
                    result.append(str(item))

            else:
                result.append(str(item))

        return ", ".join(result) if result else "NA"

    return str(value)


@app.route("/extracted-data")
def extracted_data():

    resumes = []

    docs = resume_collection.find().sort("upload_date", -1)

    for doc in docs:

        resumes.append({

            "filename": doc.get("original_filename", "NA"),

            "name": doc.get("name", "NA"),

            "email": doc.get("email", "NA"),

            "phone": doc.get("phone", "NA"),

            "skills": format_list(doc.get("skills")),

            "domain": doc.get("domain", "NA"),

            "education": doc.get("education", "NA"),

            "college": doc.get("college", "NA"),

            "university": doc.get("university", "NA"),

            "cgpa": doc.get("cgpa", "NA"),

            "experience": doc.get("experience", "NA"),

            "internships": doc.get("internships", "NA"),

            "projects": format_list(doc.get("projects")),

            "certifications": format_list(doc.get("certifications")),

            "technical_skills": format_list(doc.get("technical_skills")),

            "soft_skills": format_list(doc.get("soft_skills")),

            "languages": format_list(doc.get("languages")),

            "linkedin": doc.get("linkedin", "NA"),

            "github": doc.get("github", "NA"),

            "portfolio": doc.get("portfolio", "NA")

        })

    return render_template(
        "extracted_data.html",
        resumes=resumes
    )
# ==========================
# Resume Repository
# ==========================

@app.route("/repository")
def repository():

    resumes = []

    for doc in resume_collection.find().sort("upload_date", -1):

        resumes.append({

            "filename": doc.get(
                "original_filename",
                doc.get("stored_filename", "Unknown Resume")
            ),

            "stored_filename": doc.get(
                "stored_filename",
                doc.get("original_filename", "")
            ),

            "date": doc.get(
                "upload_date",
                datetime.now()
            ).strftime("%d-%m-%Y %I:%M %p")

        })

    return render_template(
        "resume_repository.html",
        resumes=resumes
    )

# ==========================
# Download Resume
# ==========================

@app.route("/download/<stored_filename>")
def download_resume(stored_filename):

    doc = resume_collection.find_one({
        "stored_filename": stored_filename
    })

    download_name = stored_filename

    if doc:
        download_name = doc.get(
            "original_filename",
            stored_filename
        )

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        stored_filename,

        as_attachment=True,

        download_name=download_name

    )


# ==========================
# Delete Resume
# ==========================

@app.route("/delete/<stored_filename>")
def delete_resume(stored_filename):

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        stored_filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    resume_collection.delete_one({
        "stored_filename": stored_filename
    })

    return redirect(url_for("repository"))

@app.route("/remove_unknown")
def remove_unknown():

    result = resume_collection.delete_many({
        "original_filename": {"$exists": False}
    })

    return f"Deleted {result.deleted_count} Unknown Resume record(s)."

# ==========================
# Run
# ==========================

if __name__ == "__main__":
    app.run(debug=True)