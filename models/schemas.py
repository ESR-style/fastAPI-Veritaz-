from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

class MessageCreate(BaseModel):
    content: str
    sender: str

class ThreadCreate(BaseModel):
    title: str