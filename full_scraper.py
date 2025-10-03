'''full_scraper.py



Sep 2025
'''
import json
import time
import subprocess
from datetime import datetime

from scrapers import get_arxiv_metadata_batch

def scrape_papers(query, sort_by="date", order="descending", max_results=2, verbose=False):
    # for naming conventions
    date = datetime.today().strftime('%Y-%m-%d')
    
    if verbose:
        print(f"======== Attempting to scrape {max_results} papers from arxiv.org with query: {query}")
    
    t0 = time.time()
    # get article metadata; includes pdf_url but not pdf itself 
    metadata_dict = get_arxiv_metadata_batch(query=query, sort_by=sort_by, order=order, max_results=max_results)
    
    if verbose:
        t1_metadata = time.time()
        print(f"======== Metadata extracted in {t1_metadata-t0:.2f} seconds")
        
        for paper in metadata_dict:
            print(f"[{paper}] {metadata_dict[paper]['title']} ---- {metadata_dict[paper]['date_submitted']}")
    
    t3 = time.time()
    # use a subprocess to run shell command from within python script: https://docs.python.org/3/library/subprocess.html
    for paper in metadata_dict:
        o1 = subprocess.run(["arxiv-downloader", metadata_dict[paper].get("pdf_url"), "-d" f"../../mkpuzo-data/AURA_pdfs/papers_{date}"])

    if verbose:
        t1_papers = time.time()
        print(f"======== Papers downloaded in {t1_papers-t3:.2f} seconds")
    
    print()
    t3 = time.time()
    # dump metadata to json file
    with open(f"./metadata/metadata_{date}.json", "w") as f:
        json.dump(metadata_dict, f, indent=2)
        
    if verbose:
        t1_metadata = time.time()
        print(f"======== Metadata saved in {t1_metadata-t3:.2f} seconds")
        
    print(f"\n ======== {max_results} papers saved | ./metadata/metadata_{date}.json{t1_metadata-t3:.2f} |  /home/mkpuzo/mkpuzo-data/AURA_pdfs/papers_{date} | total time: {time.time()-t0:.2f} seconds")
    
    
if __name__ == "__main__":
    scrape_papers(query="artificial intelligence", max_results=10, verbose=True)