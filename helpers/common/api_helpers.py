import requests
from typing import Dict, Any
import os
from pathlib import Path

def get_cypher_query(api_url: str, payload: Dict[str, Any]) -> str:
    # Commenting out actual API call for future use
    """
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('cypher_query')
    else:
        raise Exception("Failed to fetch cypher query from API")
    """
    return "MOCK_QUERY"

def load_mock_responses():
    import json
    # Get the FastAPI root directory path
    current_dir = Path(__file__).parent.parent.parent
    mock_file_path = current_dir / 'data' / 'mock_responses.json'
    
    with open(mock_file_path) as f:
        return json.load(f)