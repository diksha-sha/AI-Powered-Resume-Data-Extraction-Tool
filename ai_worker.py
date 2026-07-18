from database.db import resume_collection

from resume_parser.parser import extract_text
from resume_parser.extractor import extract_resume_data
from resume_parser.ai_extractor import ai_extract_resume


def process_resume(stored_filename, filepath, selected_domain):

    print(f"Processing {stored_filename}")

    try:

        # ----------------------------------
        # Extract Resume Text
        # ----------------------------------

        text = extract_text(filepath)

        # ----------------------------------
        # Fast Regex Extraction
        # ----------------------------------

        regex_data = extract_resume_data(text)

        # ----------------------------------
        # AI Extraction
        # (AI extracts everything except domain)
        # ----------------------------------

        ai_data = ai_extract_resume(text)

        # ----------------------------------
        # Merge Results
        # AI overwrites regex values
        # ----------------------------------

        regex_data.update(ai_data)

        # ----------------------------------
        # Preserve User Selected Domain
        # ----------------------------------

        regex_data["domain"] = selected_domain

        # ----------------------------------
        # Update MongoDB
        # ----------------------------------

        resume_collection.update_one(

            {
                "stored_filename": stored_filename
            },

            {
                "$set": {

                    **regex_data,

                    "status": "Completed"

                }
            }

        )

        print(f"{stored_filename} completed successfully.")

    except Exception as e:

        print("\n========== AI WORKER ERROR ==========")
        print(e)
        print("=====================================\n")

        resume_collection.update_one(

            {
                "stored_filename": stored_filename
            },

            {
                "$set": {

                    "status": "Failed"

                }
            }

        )