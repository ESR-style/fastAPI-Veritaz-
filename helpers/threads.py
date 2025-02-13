from datetime import datetime
import uuid
from models.schemas import Thread
from typing import Dict, List, Optional

def create_new_thread(title: str) -> Thread:
    return Thread(
        id=str(uuid.uuid4()),
        title=title,
        created_at=datetime.now().isoformat(),
        messages=[]
    )

def generate_mock_response(user_message: str, mock_responses: dict) -> Dict:
    query = user_message.lower()
    
    if "rack" in query and "si" in query:
        response = mock_responses["supply_chain_queries"]["racks_by_si"]
        return {
            "text": response['text'],
            "data": response['data'],
            "followup": response['followup'],
            "type": "table"
        }
    
    if "sales" in query and "country" in query:
        response = mock_responses["supply_chain_queries"]["sales_by_country"]
        return {
            "text": response['text'],
            "data": response['data'],
            "followup": response['followup'],
            "type": "table"
        }
    
    return {
        "text": "I can help you analyze your supply chain data. Try asking questions like:\n- Show me sales by country\n- How many racks were built by SI last month?",
        "type": "text"
    }