import requests
from typing import Dict, Any, List
import os
from pathlib import Path
from datetime import datetime

def transform_neo4j_response(neo4j_response: List[Dict]) -> List[Dict]:
    transformed_data = []
    for record in neo4j_response:
        # Check if record has _fields array containing the node data
        if '_fields' in record and record['_fields']:
            # Get the first field which contains the node
            node = record['_fields'][0]
            
            # Extract properties if they exist
            if 'properties' in node:
                properties = dict(node['properties'])
                
                # Handle the nested Date object specifically
                if 'Date' in properties:
                    date_obj = properties['Date']
                    # Extract year, month, day from the nested low/high structure
                    year = date_obj['year']['low']
                    month = date_obj['month']['low']
                    day = date_obj['day']['low']
                    # Replace the complex Date object with a formatted string
                    properties['Date'] = f"{year:04d}-{month:02d}-{day:02d}"
                
                transformed_data.append(properties)

    return transformed_data

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