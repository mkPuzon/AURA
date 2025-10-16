# AURA
AI Understanding, Research, and Analytic glossary for AI education

Project developed on Ubuntu 23.04 and uses Python 3.11.4

# Current Functionality
The `full_scraper.py` file provides a `scrape_papers()` function which scrapes any given number of papers from arXiv based on a given search query. Filtering options include by date or relevance (ascending or decending for either). This scrapes relevant metadata and saves it to a .json file as well as locally saving the .pdf file for text extraction.

# TODOs
- [ ] Dump .json data to PostgreSQL db
    - [ ] Connect tables via paper primary key
    - [ ] Handle incrementing word count
    - [ ] Determine how to merge variants of the same keywords

---
Thank you to arXiv for use of its open access interoperability.
