'''full_scraper.py



Sep 2025
'''
import os
import sys
import json
import subprocess

from pathlib import Path
from pypdf import PdfReader
from datetime import datetime
from scrapers import get_arxiv_metadata_batch

def scrape_papers(query, date, sort_by="date", order="descending", max_results=2, verbose=False):
    # for naming conventions
    pdf_save_dir = f"../../mkpuzo-data/AURA_pdfs/papers_{date}"
    os.makedirs(pdf_save_dir, exist_ok=True)
    
    # get metadata
    metadata_dict = get_arxiv_metadata_batch(query=query, sort_by="date", order="descending", max_results=max_results)
    
    # download PDFs
    for paper_id, info in metadata_dict.items():
        pdf_url = info.get("pdf_url")
        if pdf_url:
            # TODO: change this to a basic HTML query
            subprocess.run(["arxiv-downloader", pdf_url, "-d", pdf_save_dir])

    # extract text from each downloaded PDF using PyPDF
    for i, file in enumerate(Path(pdf_save_dir).glob("*.pdf")):
        try:
            reader = PdfReader(file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            metadata_dict[list(metadata_dict.keys())[i]]["full_text"] = text
        except Exception as e:
            metadata_dict[list(metadata_dict.keys())[i]]["full_text"] = f"[Error extracting text: {e}]"
    
    # save results to JSON
    os.makedirs("./metadata", exist_ok=True)
    with open(f"./metadata/metadata_{date}.json", "w") as f:
        json.dump(metadata_dict, f, indent=2)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python full_scraper.py <date>")
        sys.exit(1)
    scrape_papers(query="artificial intelligence", date=sys.argv[1], max_results=2, verbose=True)