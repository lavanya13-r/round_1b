import os
import json
from datetime import datetime
from PyPDF2 import PdfReader
from collections import defaultdict

def extract_relevant_sections(documents, persona, job, pdf_folder):
    keywords = set()
    keywords.update(persona["role"].lower().split())
    keywords.update(job["task"].lower().split())

    matches = []

    for doc in documents:
        pdf_path = os.path.join(pdf_folder, doc["filename"])
        if not os.path.exists(pdf_path):
            continue

        try:
            reader = PdfReader(pdf_path)
        except:
            continue

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue

            text_lower = text.lower()
            keyword_hits = sum(k in text_lower for k in keywords)

            if keyword_hits > 0:
                matches.append({
                    "document": doc["filename"],
                    "section_title": text.strip().split("\n")[0][:100],  # top line
                    "refined_text": text.replace("\n", " ")[:1000],      # cleaned
                    "page_number": i + 1,
                    "score": keyword_hits
                })

    # Sort matches by score descending
    matches.sort(key=lambda x: -x["score"])

    # Take top 5 unique (based on document+page_number)
    seen = set()
    extracted_sections = []
    subsection_analysis = []

    for idx, match in enumerate(matches):
        key = (match["document"], match["page_number"])
        if key in seen:
            continue
        seen.add(key)

        if len(extracted_sections) < 5:
            extracted_sections.append({
                "document": match["document"],
                "section_title": match["section_title"],
                "importance_rank": len(extracted_sections) + 1,
                "page_number": match["page_number"]
            })

        if len(subsection_analysis) < 5:
            subsection_analysis.append({
                "document": match["document"],
                "refined_text": match["refined_text"],
                "page_number": match["page_number"]
            })

        if len(extracted_sections) >= 5 and len(subsection_analysis) >= 5:
            break

    return extracted_sections, subsection_analysis

def main():
    for collection in os.listdir():
        if not collection.startswith("Collection") or not os.path.isdir(collection):
            continue

        input_path = os.path.join(collection, "challenge1b_input.json")
        output_path = os.path.join(collection, "challenge1b_output.json")
        pdf_folder = os.path.join(collection, "PDFs")

        if not os.path.exists(input_path) or not os.path.exists(pdf_folder):
            print(f"⚠️ Skipping {collection}: missing input or PDF folder")
            continue

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        extracted_sections, subsection_analysis = extract_relevant_sections(
            data["documents"], data["persona"], data["job_to_be_done"], pdf_folder
        )

        output = {
            "metadata": {
                "input_documents": [doc["filename"] for doc in data["documents"]],
                "persona": data["persona"]["role"],
                "job_to_be_done": data["job_to_be_done"]["task"],
                "processing_timestamp": datetime.utcnow().isoformat()
            },
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

        print(f"✅ {collection} processed ({len(extracted_sections)} sections)")

if __name__ == "__main__":
    main()
