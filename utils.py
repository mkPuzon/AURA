'''utils.py

Contains general helpful functions for codebase.

Sep 2025
'''
import os
import json
import time
import subprocess
from pathlib import Path

import feedparser # parse/extract from RSS and Atom feeds
import urllib.request # opening URLs

def inspect_dictionary(d, indent=0):
    """ [Written by CLAUDE Sonnet 4]
    Neatly and clearly inspects a dictionary object, printing all key/value pairs
    at all levels and specifying the types of each element.

    Args:
        d (dict): The dictionary object to inspect.
        indent (int): The current indentation level for nested dictionaries (internal use).
    """
    if not isinstance(d, dict):
        print(f"{'  ' * indent}[ERROR] Expected dictionary, received {type(d).__name__}")
        return

    for key, value in d.items():
        key_type = type(key).__name__
        value_type = type(value).__name__
        
        # Print key with clear visual hierarchy
        print(f"{'  ' * indent}├─ {key} ({key_type})")

        # Handle nested dictionaries
        if isinstance(value, dict):
            print(f"{'  ' * indent}│  └─ {value_type} with {len(value)} key(s)")
            inspect_dictionary(value, indent + 1)
            if indent == 0:  # Add spacing after top-level nested dicts
                print()
        
        # Handle lists and tuples
        elif isinstance(value, (list, tuple)):
            print(f"{'  ' * indent}│  └─ {value} ({value_type}, length: {len(value)})")
            for i, item in enumerate(value):
                item_type = type(item).__name__
                print(f"{'  ' * (indent + 1)}   [{i}] {item} ({item_type})")
                # Recursively inspect dictionary items in lists
                if isinstance(item, dict):
                    inspect_dictionary(item, indent + 2)
        
        # Handle simple values
        else:
            print(f"{'  ' * indent}│  └─ {value} ({value_type})")
    
    # Add clean separation after top-level inspection
    if indent == 0:
        print("─" * 50)
        

def clear_pdfs(date: str, clear_metadata: bool = False):
    """Safely delete PDF files under ./papers/papers_{date}"""
    
    BASE_PAPERS_DIR = Path("./papers").resolve()
    BASE_METADATA_DIR = Path("./metadata").resolve()

    # build target paths
    papers_dir = (Path("./papers") / f"papers_{date}").resolve()
    if not str(papers_dir).startswith(str(BASE_PAPERS_DIR) + os.sep):
        raise ValueError("Invalid 'date' path: target not under ./papers")

    if papers_dir.exists() and papers_dir.is_dir():
        deleted_any = False
        for p in papers_dir.iterdir():
            if p.is_file() and p.suffix.lower() == ".pdf":
                try:
                    p.unlink()
                    deleted_any = True
                except Exception as e:
                    raise RuntimeError(f"Failed to delete {p}: {e}") from e
        try:
            if not any(papers_dir.iterdir()):
                papers_dir.rmdir()
        except Exception:
            print(f"Failed to delete {papers_dir} (not empty)")
    else:
        # no such papers directory
        print(f"[WARNING] No such directory: {papers_dir}")

    if clear_metadata:
        meta_file = (Path("./metadata") / f"metadata_{date}.json").resolve()
        if not str(meta_file).startswith(str(BASE_METADATA_DIR) + os.sep):
            raise ValueError("Invalid 'date' path: metadata target not under ./metadata")

        if meta_file.exists() and meta_file.is_file():
            try:
                meta_file.unlink()
            except Exception as e:
                raise RuntimeError(f"Failed to delete metadata file {meta_file}: {e}") from e


def save_specific_paper(arxiv_id):
    '''For grabbing specific papers off of arXiv. PDFs are saved to ./papers/papers_core
    PARAMETER MUST BE A STRING not a number!
    '''
    # scrape metadata from specific papers
    metadata_dict = get_arxiv_metadata_single(arxiv_id)
    
    with open(f"./metadata/metadata_{metadata_dict[0]['title'].replace(' ', '')}.json", "a") as f:
        json.dump(metadata_dict, f, indent=2)

        
    # download pdf
    subprocess.run(["arxiv-downloader", arxiv_id, "-d" "./papers/papers_core"])
    
    
if __name__ == "__main__":
    save_specific_paper("2404.18416v2")