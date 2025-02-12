from datetime import datetime
import uuid
from models.schemas import Message
from database.neo4j_client import neo4j_client
from helpers.common.api_helpers import get_cypher_query

def create_user_message(thread_id: str, content: str) -> Message:
    return Message(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        content=content,
        timestamp=datetime.now().isoformat(),
        sender="user"
    )

def create_assistant_message(thread_id: str, content: str) -> Message:
    return Message(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        content=content,
        timestamp=datetime.now().isoformat(),
        sender="assistant"
    )

def get_response_data(api_url: str, payload: dict) -> dict:
    cypher_query = get_cypher_query(api_url, payload)
    return neo4j_client.execute_query(cypher_query)