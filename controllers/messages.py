from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import Message, MessageCreate
from helpers.messages import create_user_message, create_assistant_message, get_response_data

router = APIRouter(prefix="/messages", tags=["messages"])

# In-memory storage
messages = {}

@router.put("/{message_id}", response_model=Message)
async def update_message(message_id: str, content: str):
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    messages[message_id].content = content
    return messages[message_id]

@router.delete("/{message_id}")
async def delete_message(message_id: str):
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    message = messages[message_id]
    del messages[message_id]
    return {"message": "Message deleted"}