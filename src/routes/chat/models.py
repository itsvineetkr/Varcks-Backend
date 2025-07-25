from src.database.mongo import db
from pydantic import BaseModel


chat_sessions = db.chat_sessions
chat_messages = db.chat_messages


class ChatSession(BaseModel):
    session_id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str


class ChatMessage(BaseModel):
    session_id: str
    user_id: str
    model: str
    query: str
    response: str
    created_at: str