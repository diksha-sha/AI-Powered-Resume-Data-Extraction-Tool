import os

from resume_parser.parser import extract_text
from resume_parser.ai_extractor import ai_extract_resume

UPLOAD_FOLDER = "uploads"

# Get all PDF files
files = [
    f for f in os.listdir(UPLOAD_FOLDER)
    if f.lower().endswith(".pdf")
]

print("Files Found:\n")

for i, f in enumerate(files):
    print(f"{i+1}. {f}")

if not files:
    print("No PDF files found.")
    exit()

# Read first resume
filepath = os.path.join(UPLOAD_FOLDER, files[0])

print("\nReading:", filepath)

text = extract_text(filepath)

print("\n================ TEXT ================\n")
print(text[:1500])

print("\n================ AI OUTPUT ================\n")

data = ai_extract_resume(text)

print(data)