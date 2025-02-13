from fastapi import APIRouter, HTTPException
from typing import List, Dict
from models.schemas import Thread, Message, ThreadCreate
from helpers.threads import create_new_thread, generate_mock_response
from helpers.messages import create_user_message, create_assistant_message
from helpers.common.api_helpers import load_mock_responses

router = APIRouter(prefix="/threads", tags=["threads"])

# In-memory storage
chat_threads: Dict[str, Thread] = {}

@router.post("/", response_model=Thread)
async def create_thread(thread_data: ThreadCreate):
    new_thread = create_new_thread(thread_data.title)
    chat_threads[new_thread.id] = new_thread
    return new_thread

@router.get("/", response_model=List[Thread])
async def get_all_threads():
    return list(chat_threads.values())

@router.get("/{thread_id}", response_model=Thread)
async def get_thread(thread_id: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    return chat_threads[thread_id]

@router.delete("/{thread_id}")
async def delete_thread(thread_id: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    del chat_threads[thread_id]
    return {"message": "Thread deleted"}

@router.post("/{thread_id}/messages/", response_model=List[Message])
async def create_message(thread_id: str, content: str, sender: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Create user message
    user_message = create_user_message(thread_id, content)
    
    # Load mock responses
    mock_data = load_mock_responses()
    
    # Generate mock response based on user query
    mock_response = generate_mock_response(content, mock_data)
    
    # Create AI message with mock response
    ai_message = create_assistant_message(thread_id, mock_response)
    
    # Add messages to thread
    chat_threads[thread_id].messages.extend([user_message, ai_message])
    
    return [user_message, ai_message]

    # Commented out actual API call for future use
    """
    # Get response data from external API
    api_url = "http://100.26.118.88:5000/cypherquery"
    payload = {"query": content}
    response_data = get_response_data(api_url, payload)
    """

@router.get("/{thread_id}/messages/", response_model=List[Message])
async def get_thread_messages(thread_id: str):
    if thread_id not in chat_threads:
        raise HTTPException(status_code=404, detail="Thread not found")
    return chat_threads[thread_id].messages