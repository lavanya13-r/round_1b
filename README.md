

```markdown
# 📘 Persona-Driven PDF Document Analyzer

A solution for **Adobe Hackathon Round 1B: Persona-Driven Document Intelligence**.  
This tool analyzes PDF collections and extracts relevant sections based on a **persona** and **job-to-be-done**.

---

## 🚀 Features

- 📂 Multi-collection support  
- 🧠 Persona-aware keyword matching  
- 🏷️ Importance-ranked section extraction  
- 📦 Dockerized workflow  
- 📊 Structured JSON output  


---

## 🧱 Project Structure

Challenge_1b/
├── Collection1/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection2/
├── Collection3/
├── main.py
├── Dockerfile
├── requirements.txt
└── README.md

---

## 🧠 Input JSON

```json
{
  "documents": [{ "filename": "doc.pdf", "title": "Doc Title" }],
  "persona": { "role": "HR professional" },
  "job_to_be_done": { "task": "Create and manage fillable forms" }
}
```

## 📤 Output JSON

```json
{
  "metadata": {
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    { "document": "...", "section_title": "...", "importance_rank": 1, "page_number": 1 }
  ],
  "subsection_analysis": [
    { "document": "...", "refined_text": "...", "page_number": 1 }
  ]
}
```

## 🐳 Run with Docker

```bash
docker build -t pdf-analyzer .
docker run --rm -v "${PWD}:/app" pdf-analyzer
```

## On Windows PowerShell:

```bash
docker run --rm -v ${PWD}:/app pdf-analyzer
```

## 👤 Personas & Tasks

| Collection  | Persona         | Task                                     |
| ----------- | --------------- | ---------------------------------------- |
| Collection1 | Travel Planner  | Plan a 4-day trip                        |
| Collection2 | HR Professional | Create/manage onboarding forms           |
| Collection3 | Food Contractor | Prepare buffet menu for corporate dinner |

## 🛠️ Tech Stack

- Python 3.10
- PyPDF2
- Docker
```
