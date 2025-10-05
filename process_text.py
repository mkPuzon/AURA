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
import json
import time
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
    print(f"     == Model response extracted in {t1-t0:.2f} seconds")
    return model_response

def get_definitions(keywords, paper_txt,model="gemma3:12b"):
    ollama_url = os.getenv("OLLAMA_API")
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
    print(f"    == Model response extracted in {t1-t0:.2f} seconds")
    return model_response

if __name__ == "__main__":
    load_dotenv()
    file_path = "metadata/metadata_2025-10-05.json"
    # for 3 example papers
    with open(file_path, "r") as f:
        metadata_dict = json.load(f)
        for i in range(len(metadata_dict.keys())-7):
            print(f"\n\n{i}: {metadata_dict[str(i)]['full_arxiv_url']}")
            keywords = query_ollama_model(paper_txt=metadata_dict[str(i)]['abstract'])
            # print(f"    {keywords}")
            
            # find list if one exists
            pattern = r'\[(.*?)\]'
            match = re.search(pattern, keywords, re.DOTALL)
            if match:
                list_content = match.group(1)
                keywords = re.findall(r'["\']([^"\']+)["\']', list_content)
                print(f"    {keywords}")
                definitions = get_definitions(keywords=keywords, paper_txt=metadata_dict[str(i)]['full_text'])
                
                dict_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
                dict_match = re.search(dict_pattern, definitions, re.DOTALL)
                if dict_match:
                    try:
                        import ast
                        definitions_dict = ast.literal_eval(dict_match.group())
                        if isinstance(definitions_dict, dict):
                            print(f"\n    {definitions_dict}")
                        else:
                            print(f"\n    Invalid dictionary format: {definitions}")
                    except (ValueError, SyntaxError) as e:
                        print(f"\n    Failed to parse dictionary: {e}")
                        # print(f"\n    Raw output: {definitions}")
                else:
                    # print(f"\n    No dictionary found in: {definitions}")
                    pass
            else:
                print("No list found.")
        
        