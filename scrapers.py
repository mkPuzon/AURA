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
    
    request = f"http://export.arxiv.org/api/query?search_query=cat:{query}&sortBy={sort_method}&sortOrder={order}&max_results={max_results}"
    
    with urllib.request.urlopen(request) as url:
        response = url.read()
        
    feed = feedparser.parse(response) # returns a feedparser.util.FeedParserDict    
    
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
            # PDF link is identified by rel="related" and title="pdf" 
            if link.get('title') == 'pdf' and link.get('rel') == 'related':
                pdf_url = link.get('href')
                break
        
        try:
            authors = ', '.join(author.name for author in entry.authors)
        except AttributeError:
            authors = entry.author
            
        records[paper_num] = {
            "uuid" : str(uuid.uuid4()),
            "title": title,
            "date_submitted": date_submitted[:10],
            "date_scraped": time.time(),
            "tags": tags,
            "authors": authors,
            "abstract": abstract,
            "pdf_url": pdf_url,
            "full_arxiv_url": full_arxiv_url,
            "full_text": None
        }   
        paper_num += 1
        
    return records

