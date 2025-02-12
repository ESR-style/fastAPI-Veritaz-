import requests
from typing import Dict, Any

def get_cypher_query(api_url: str, payload: Dict[str, Any]) -> str:
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('cypher_query')
    else:
        raise Exception("Failed to fetch cypher query from API")

def load_mock_responses():
    import json
    with open('data/mock_responses.json') as f:
        return json.load(f)