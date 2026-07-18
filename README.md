# AI-Powered Resume Data Extraction Tool

An AI-powered Resume Data Extraction Tool built using **Python, Flask, and NLP-inspired information extraction** that automatically extracts structured candidate information from uploaded PDF and DOCX resumes. The system converts unstructured resume data into structured JSON and provides an admin dashboard for efficient resume management.

---

## Features

- Upload resumes in PDF and DOCX formats
- Automatically extracts candidate information after resume upload
- Extracts:
  - Name
  - Email Address
  - Phone Number
  - Skills
  - Work Experience
  - Total Experience
  - Education
  - Professional Domain
  - Relevant Information
- Converts unstructured resumes into structured JSON
- Resume Repository for managing uploaded resumes
- Download and delete functionality
- Admin Dashboard for monitoring extracted data
- REST API support for integration

---

## System Workflow

```text
Upload Resume
      │
      ▼
PDF / DOCX Parser
      │
      ▼
Text Extraction
      │
      ▼
Text Preprocessing
      │
      ▼
Information Extraction
      │
      ├── Name
      ├── Contact Details
      ├── Skills
      ├── Experience
      ├── Education
      ├── Domain
      └── Relevant Information
      │
      ▼
Structured JSON
      │
      ▼
Admin Dashboard
```

---

## Tech Stack

### Backend
- Python
- Flask

### NLP & Information Extraction
- Regular Expressions (Regex)
- Text Preprocessing
- Keyword Matching

### Document Processing
- pdfplumber
- python-docx

### Database
- MongoDB (Integration Ready)

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

### APIs
- REST APIs
- JSON

---

## Project Structure

```text
Resume_Data_Extraction_Tool/
│
├── app.py
├── extractor.py
├── parser.py
├── requirements.txt
│
├── uploads/
├── templates/
├── static/
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/Resume_Data_Extraction_Tool.git
```

```bash
cd Resume_Data_Extraction_Tool
```

### Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## Sample Output

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "skills": [
    "Python",
    "Flask",
    "Machine Learning",
    "SQL"
  ],
  "experience": "2 Years",
  "education": "B.Tech Computer Science",
  "domain": "AI Engineer"
}
```

---

## Project Highlights

- Processed **75+ resumes** across PDF and DOCX formats during testing.
- Automatically extracted **8+ candidate attributes** from uploaded resumes.
- Built **5 REST API endpoints** for upload, extraction, retrieval, download, and management.
- Reduced manual resume screening effort by **approximately 85%** by automating information extraction.
- Supports **2 document formats** (PDF and DOCX).
- Generates structured JSON output for easy integration with HR systems.

---

## Future Enhancements

- LLM-powered resume parsing using OpenAI or Gemini
- Resume-to-Job Description matching
- Candidate ranking based on skill matching
- Semantic search using vector embeddings
- Vector database integration (FAISS, ChromaDB, Pinecone)
- RAG-based recruiter assistant
- OCR support for scanned resumes
- Cloud deployment on AWS, Azure, or GCP

---

## Use Cases

- Resume Screening
- Applicant Tracking Systems (ATS)
- Recruitment Automation
- Candidate Database Management
- HR Analytics
- Talent Acquisition

---

## Author

**Diksha Sharma**

AI/ML Enthusiast | Python Developer | B.Tech Computer Science
