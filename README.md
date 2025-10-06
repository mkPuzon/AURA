# AURA
AI Understanding, Research, and Analytic glossary for AI education

Project developed on Ubuntu 23.04 and uses Python 3.11.4

# Current Functionality
The `full_scraper.py` file provides a `scrape_papers()` function which scrapes any given number of papers from arXiv based on a given search query. Filtering options include by date or relevance (ascending or decending for either). This scrapes relevant metadata and saves it to a .json file as well as locally saving the .pdf file for text extraction.

# TODOs
- [ ] Prompt engineer to reliably extract keywords/important terms
- [ ] Prompt engineer to reliably extract relevant definitions
- [ ] Deal with garbage model responses
- [ ] Hook up pipeline for Python script to PostgreSQL db from .json

---
Thank you to arXiv for use of its open access interoperability.
