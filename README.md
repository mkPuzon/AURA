# AURA
AI Understanding, Research, and Analytic glossary for AI education

Project developed on Ubuntu 23.04 and uses Python 3.11.4

# TODOs
- [ ] Extract keywords
    - [ ] Determine standard if keywords are not present
    - [ ] Determine standard if keywords are similar to one another (merge? collection?)
- [ ] Get definitions from papers 
    - [ ] Set up Ollama querying
    - [ ] Extract key concepts
        - [ ] Compare with keywords
    - [ ] Test queries for quality definitions

- [ ] Design PostgreSQL table system
    - [ ] Hook up pipeline for Python script to PostgreSQL db from .json

# Notes
Currently queries Gemini 2.5 Flash Lite through the Google API for keyword extraction. I am limited by the free teir rates:

- Requests per minute (RPM) = 15
- Tokens per minute (TPM)   = 250,000
- Requests per day (RPD)    = 1,000

More information on the rate limits available [here](https://ai.google.dev/gemini-api/docs/rate-limits?authuser=3) and information on Google LLM models [here](https://ai.google.dev/gemini-api/docs/models).

---
Thank you to arXiv for use of its open access interoperability.