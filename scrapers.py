'''scrapers.py

Contains functions to get relevant research papers from the web. Currently can query:
- arXiv

Sep 2025
'''
import os
import time
import uuid
import feedparser # parse/extract from RSS and Atom feeds
import urllib.request # opening URLs

from google import genai # query Gemini
from dotenv import load_dotenv # load in sensitive .env variables

def get_arxiv_metadata_batch(query, sort_by="date", order="descending", max_results=2):
    if " " in query:
        query = query.replace(" ", "+")
    
    if sort_by == "date":
        sort_method = "submittedDate"
    elif sort_by == "relevance":
        sort_method = "relevance"
    else:
        raise ValueError(f"Unknown sorting request by: {sort_by}. Valid options: date, relevance.")
    
    if order not in ["descending", "ascending"]:
        raise ValueError(f"Unknown sorting order: {order}. Valid options: ascending, descending.")
    
    request = f"http://export.arxiv.org/api/query?search_query=all:{query}&sortBy={sort_method}&sortOrder={order}&max_results={max_results}"
    
    with urllib.request.urlopen(request) as url:
        response = url.read()
        
    feed = feedparser.parse(response) # feedparser.util.FeedParserDict    
    # inspect_dictionary(feed)
    
    records = {}
    paper_num = 0
    for entry in feed.entries:
        # get relevant info from feedparser and add to records list Python dict
        title = entry.title.strip()
        date_submitted = entry.published
        tags = ', '.join(t['term'] for t in entry.tags) if entry.tags else None
        abstract = entry.summary.strip()
        
        full_arxiv_url = entry.link
        pdf_url = None
        for link in entry.links:
            # The PDF link is identified by rel="related" and title="pdf" 
            if link.get('title') == 'pdf' and link.get('rel') == 'related':
                pdf_url = link.get('href')
                break
        
        try:
            authors = ', '.join(author.name for author in entry.authors)
        except AttributeError:
            authors = entry.author
        try:
            affiliation = entry.arxiv_affiliation
        except AttributeError:
            affiliation = None
            
        records[paper_num] = {
            "uuid" : str(uuid.uuid4()),
            "title": title,
            "date_submitted": date_submitted[:10],
            "date_scraped": time.time(),
            "tags": tags,
            "authors": authors,
            "abstract": abstract,
            "affiliation": affiliation,
            "pdf_url": pdf_url,
            "full_arxiv_url": full_arxiv_url
        }   
        paper_num += 1
        
    return records

def get_keywords(abstract, keywords=5):
    '''Using a Google LLM to extract keywords from a paper abstract.'''
    model = "gemini-2.5-flash-lite"
    prompt = f"For the following paper abstract, extract {keywords} keywords to describe the topic and content of the paper. Return they keywords in a Python list. Return only the Python list, no extra words. For example: ['computer science', 'RAG', 'higher education', ...]. Here is the abstrac to analyze: {abstract}"
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model=model, contents=prompt
    )
    return response.text