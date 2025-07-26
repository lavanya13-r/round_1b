# 🧠 Approach Explanation: Persona-Driven PDF Document Analyzer

## Overview

This solution was developed for **Adobe Hackathon Round 1B: Persona-Driven Document Intelligence**. The goal is to identify and rank the most relevant content from a collection of PDF files based on a user-defined **persona** and a **job-to-be-done**. The system processes the PDFs, scores each page based on keyword relevance, and returns a structured JSON output.

---

## 🔍 Methodology

### 1. **Text Extraction**

We use `PyPDF2` to extract raw text content from each page of every PDF. The system loops through every document in the input JSON and checks for file existence before parsing to avoid runtime errors.

### 2. **Persona-Aware Keyword Generation**

The core idea is to identify relevance by matching content with the persona’s intent. The system:
- Extracts keywords from both the `persona["role"]` and `job_to_be_done["task"]` fields.
- Tokenizes and lowercases all keywords for uniform comparison.

These keywords are used to compute a **score** for each page.

### 3. **Relevance Scoring and Filtering**

For each page:
- The text is converted to lowercase.
- A score is calculated based on how many of the extracted keywords are present.
- The first line of the page is assumed to be a potential section heading.
- Each match is recorded with document name, heading, text snippet, page number, and score.

### 4. **Ranking and Deduplication**

After collecting potential matches:
- Pages are sorted in descending order of keyword match score.
- To avoid duplicates, we store only the **top 5 unique pages**, using `(filename, page_number)` as a deduplication key.
- Two lists are populated:
  - `extracted_sections` → includes metadata like heading, rank, and page number.
  - `subsection_analysis` → includes the raw text snippet for that page.

### 5. **Structured Output**

The final output JSON includes:
- Metadata (documents, persona, task, timestamp)
- Top 5 extracted sections with importance rank
- Refined text excerpts from those sections

The JSON is saved as `challenge1b_output.json` in the corresponding collection directory.

---

## 🐳 Dockerization

The script runs inside a lightweight Docker container for reproducibility. Usage:
```bash
docker build -t pdf-analyzer .
docker run --rm -v "${PWD}:/app" pdf-analyzer
