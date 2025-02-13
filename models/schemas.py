from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class Message(BaseModel):
    id: str
    thread_id: str
    content: Union[str, Dict[str, Any]]  # Allow either string or structured content
    timestamp: str
    sender: str

class Thread(BaseModel):
    id: str
    title: str
    created_at: str
    messages: List[Message] = []

class MessageCreate(BaseModel):
    content: Union[str, Dict[str, Any]]
    sender: str

class ThreadCreate(BaseModel):
    title: str