'''process_text.py

Uses Gemma3 to extract keywords and definitions from text.

Note for context window sizes:
32k = 32768
64k = 65536
128k = 131072
256k = 262144
512k = 524288
1M = 1048576

Aug 2025
'''
import os
import re
import sys
import json
import time
import datetime
import requests

from dotenv import load_dotenv

def query_ollama_model(paper_txt, model="gemma3:12b"):
    ollama_url = os.getenv("OLLAMA_API")
    sys_prompt = os.getenv("OLLAMA_PROMPT_KEYWORD_1")
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": model,
        "prompt": sys_prompt + paper_txt,
        "stream": True,
        "options": {
            "num_ctx": 65536
        }
    }
    model_response = ""

    t0 = time.time()
    with requests.post(ollama_url, headers=headers, json=data, stream=True) as response:
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return ""

        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    text = json_data.get("response", "")
                    model_response += text
                except json.JSONDecodeError:
                    pass

    t1 = time.time()
    print(f"    == Keywords extracted in {t1-t0:.2f} seconds")
    return model_response

def get_definitions(keywords, paper_txt,model="gemma3:12b"):
    if not keywords:
        return {}
    
    # ollama_url = os.getenv("OLLAMA_API")
    ollama_url = os.getenv("OLLAMA_DAI_API")
    sys_prompt = f"{keywords}: {os.getenv('OLLAMA_PROMPT_DEFINITION_1')}"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": model,
        "prompt": sys_prompt + paper_txt,
        "stream": True,
        "options": {
            "num_ctx": 65536
        }
    }
    model_response = ""

    t0 = time.time()
    with requests.post(ollama_url, headers=headers, json=data, stream=True) as response:
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return ""

        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    text = json_data.get("response", "")
                    model_response += text
                except json.JSONDecodeError:
                    pass

    t1 = time.time()
    print(f"    == Definitions extracted in {t1-t0:.2f} seconds")
    return model_response

def check_keywords(keywords):
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, keywords, re.DOTALL)
    if match:
        list_content = match.group(1)
        keywords = re.findall(r'["\']([^"\']+)["\']', list_content)
    return keywords

def check_definitions(definitions):
    dict_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
    dict_match = re.search(dict_pattern, definitions, re.DOTALL)
    if dict_match:
        try:
            import ast
            definitions_dict = ast.literal_eval(dict_match.group())
            if isinstance(definitions_dict, dict):
                return definitions_dict
            else:
                print(f"\n    Invalid dictionary format.")
        except (ValueError, SyntaxError) as e:
            print(f"\n    Failed to parse dictionary.")
    else:
        print(f"    No dictionary found in model response.")
        return {}
    
def generate_keywords_and_defs(batch_filepath, model="gemma3:12b", verbose=False):
    load_dotenv()
    try:
        updated_dict = {}
        
        with open(batch_filepath, "r") as f:
            metadata_dict = json.load(f)
            
            for i in range(len(metadata_dict.keys())): # for every paper
                print(f"\n\n{i}: {metadata_dict[str(i)]['full_arxiv_url']}")
                    
                keywords = query_ollama_model(paper_txt=metadata_dict[str(i)]['abstract'], model=model)
                # make sure keywords are a proper python list
                keywords = check_keywords(keywords)
                if keywords:
                    definitions = get_definitions(keywords=keywords, paper_txt=metadata_dict[str(i)]['full_text'], model=model)
                    definitions = check_definitions(definitions)
                    metadata_dict[str(i)]["keywords"] = keywords
                    metadata_dict[str(i)]["definitions"] = definitions
                    if verbose:
                        print(f"    == Keywords: {keywords}")
                        if definitions:
                            for key, value in definitions.items():
                                print(f"    * {key}: {value}")
                else:
                    metadata_dict[str(i)]["keywords"] = []
                    metadata_dict[str(i)]["definitions"] = {}
                    if verbose:
                        print("    == No keywords found.")
                        
                updated_dict[str(i)] = metadata_dict[str(i)]
                        
            with open(batch_filepath, "w") as f:
                json.dump(updated_dict, f, indent=2)
                
                
    except FileNotFoundError:
        print(f"[ERROR] File not found. Double check folder exists at: {batch_filepath}")
        return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_text.py <date>")
        sys.exit(1)
        
    load_dotenv()

    file_path = f"metadata/metadata_{sys.argv[1]}.json"
    generate_keywords_and_defs(file_path, verbose=True, model="llama3.3")
    # generate_keywords_and_defs(file_path, verbose=True, model="gemma3")