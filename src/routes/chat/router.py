import os
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends

from src.auth.utils import get_current_user_id
from src.config import get_settings
from src.routes.chat.utils import Assistant
from src.routes.chat.models import ChatSession, ChatMessage
from src.routes.chat.models import chat_sessions, chat_messages


settings = get_settings()
assisstant = Assistant(model_name="ollama:mistral")
router = APIRouter(responses={418: {"description": "Chat Endpoints"}})

# Setting up environment variables
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY


@router.post("/session", response_model=ChatSession)
async def create_session(title: str, user_id: str = Depends(get_current_user_id)):
    try:
        session_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        updated_at = created_at
        session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            title=title,
            created_at=created_at,
            updated_at=updated_at,
        )
        response = await chat_sessions.insert_one(session.model_dump())
        return (
            session if response.acknowledged else {"error": "Failed to create session"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions", response_model=list[ChatSession])
async def get_user_sessions(user_id: str = Depends(get_current_user_id)):
    try:
        sessions = []
        async for session in chat_sessions.find({"user_id": user_id}):
            sessions.append(ChatSession(**session))
        return sessions

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session_history(
    session_id: str, user_id: str = Depends(get_current_user_id)
):
    try:
        session = await chat_sessions.find_one(
            {"session_id": session_id, "user_id": user_id}
        )
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        messages = []
        async for message in chat_messages.find({"session_id": session_id}).sort(
            "created_at", 1
        ):
            messages.append(ChatMessage(**message))

        return {"session": ChatSession(**session), "messages": messages}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def send_chat_message(
    message: str,
    session_id: str,
    model: str = "ollama:qwen:0.5b",
    user_id: str = Depends(get_current_user_id),
):
    try:
        if model != assisstant.get_model_name():
            assisstant.switch_model(model)

        response = await assisstant.ask(message)

        chat_message = ChatMessage(
            session_id=session_id,
            user_id=user_id,
            model=model,
            query=message,
            response=response,
            created_at=datetime.now().isoformat(),
        )

        await chat_messages.insert_one(chat_message.model_dump())

        return {"message": response, "model_used": model}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TODO Edit any message and regenerate all responses
