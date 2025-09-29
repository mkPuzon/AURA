# AURA
AI Understanding, Research, and Analytic glossary for AI education

Project developed on Windows 11 and uses Python 3.12.10

# TODOs
- [ ] Format data as .json per batch
- [ ] Look into how to get more data about the papers themselves/query defintions from paper content
- [ ] Extract keywords
- [ ] Send definition queries to Gemma3 on Gandalf

- [ ] Design PostgreSQL table system

# Notes
Currently queries Gemini 2.5 Flash Lite through the Google API for keyword extraction. I am limited by the free teir rates:

- Requests per minute (RPM) = 15
- Tokens per minute (TPM)   = 250,000
- Requests per day (RPD)    = 1,000

More information on the rate limits available [here](https://ai.google.dev/gemini-api/docs/rate-limits?authuser=3) and information on Google LLM models [here](https://ai.google.dev/gemini-api/docs/models).

---
Thank you to arXiv for use of its open access interoperability.