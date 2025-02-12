import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import uuid
from fastapi.middleware.cors import CORSMiddleware
import json
from neo4j import GraphDatabase

# Define your Neo4j credentials and URI
neo4j_uri = "neo4j://35.209.84.143:7687"
neo4j_user = "ajayaram"
neo4j_password = "Mysore123!"

# Function to get cypher query from the first API call
def get_cypher_query(api_url, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=payload)
    print(response,'response in get cypher query')
    if response.status_code == 200:
        return response.json().get('cypher_query')
    else:
        raise Exception("Failed to fetch cypher query from API")

# Function to execute cypher query on Neo4j and return the data
def execute_cypher_query(driver, cypher_query):
    with driver.session() as session:
        result = session.run(cypher_query)
        return [record.data() for record in result]

# Main function to get response data
def get_response_data(api_url, payload):
    # Get the cypher query
    cypher_query = get_cypher_query(api_url, payload)
    print(cypher_query,'cypher_query')
    
    # Connect to Neo4j
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    
    # Execute the cypher query and get the data
    response_data = execute_cypher_query(driver, cypher_query)
    print(response_data,'response_data in get response data')
    
    # Close the Neo4j driver connection
    driver.close()
    
    return response_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Message(BaseModel):
    id: str
    thread_id: str
    content: str
    timestamp: str
    sender: str

class Thread(BaseModel):
    id: str
    title: str
    created_at: str
    messages: List[Message] = []

# Mock Database
chat_threads: Dict[str, Thread] = {}
messages: Dict[str, Message] = {}

# Load mock responses
with open('mock_responses.json') as f:
    MOCK_RESPONSES = json.load(f)

def generate_mock_response(user_message: str) -> Dict:
    query = user_message.lower()
    
    if "rack" in query and "si" in query:
        response = MOCK_RESPONSES["supply_chain_queries"]["racks_by_si"]
        return {
            "content": f"{response['text']}\n\n{json.dumps(response['data'])}\n\n{response['followup']}"
        }
    
    if "sales" in query and "country" in query:
        response = MOCK_RESPONSES["supply_chain_queries"]["sales_by_country"]
        return {
            "content": f"{response['text']}\n\n{json.dumps(response['data'])}\n\n{response['followup']}"
        }
    
    return {
        "content": "I can help you analyze your supply chain data. Try asking questions like:\n- Show me sales by country\n- How many racks were built by SI last month?"
    }

# Thread CRUD Operations
@app.post("/threads/", response_model=Thread)
async def create_thread(title: str):
    thread_id = str(uuid.uuid4())
    new_thread = Thread(
        id=thread_id,
        title=title,
        created_at=datetime.now().isoformat(),
        messages=[]
    )
    chat_threads[thread_id] = new_thread
    return new_thread

@app.get("/threads/", response_model=List[Thread])
async def get_all_threads():
    return list(chat_threads.values())

@app.get("/threads/{thread_id}", response_model=Thread)
async def get_thread(thread_id: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    return chat_threads[thread_id]

@app.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    del chat_threads[thread_id]
    return {"message": "Thread deleted"}

# Message CRUD Operations
@app.post("/threads/{thread_id}/messages/", response_model=List[Message])
async def create_message(thread_id: str, content: str, sender: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Create user message
    user_message = Message(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        content=content,
        timestamp=datetime.now().isoformat(),
        sender="user"
    )
    
    # Get response data from external API and execute Cypher query
    api_url = "http://100.26.118.88:5000/cypherquery"
    payload = {"query": content}
    print(payload,'payload')
    response_data = get_response_data(api_url,payload)
    print(response_data,'response data')
    
    # Create AI message
    ai_message = Message(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        content=response_data["content"],
        timestamp=datetime.now().isoformat(),
        sender="assistant"
    )
    
    # Add messages to thread
    chat_threads[thread_id].messages.append(user_message)
    chat_threads[thread_id].messages.append(ai_message)
    
    return [user_message, ai_message]

@app.get("/threads/{thread_id}/messages/", response_model=List[Message])
async def get_thread_messages(thread_id: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    return chat_threads[thread_id].messages

@app.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: str, content: str):
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    messages[message_id].content = content
    return messages[message_id]

@app.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    message = messages[message_id]
    thread = chat_threads[message.thread_id]
    thread.messages = [m for m in thread.messages if m.id != message_id]
    del messages[message_id]
    return {"message": "Message deleted"}