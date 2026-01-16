from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import (
    ConversationCreate, ConversationResponse, 
    SendMessageRequest, SendMessageResponse,
    MessageResponse
)
from app.services.chat_service import ConversationService, MessageService
from app.utils.dependencies import get_current_user, get_conversation_service, get_message_service

router = APIRouter(prefix="/conversations", tags=["Chat"])

@router.post("", response_model=ConversationResponse)
async def create_conversation(
    project_id: str,
    current_user: str = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    conversation = await service.create_conversation(project_id)
    return ConversationResponse(
        id=conversation.id,
        project_id=conversation.project_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: str = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse(
        id=conversation.id,
        project_id=conversation.project_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )

@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    current_user: str = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    messages = await service.list_messages(conversation_id)
    return [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in messages
    ]

@router.post("/{conversation_id}/messages", response_model=SendMessageResponse)
async def send_message(
    conversation_id: str,
    req: SendMessageRequest,
    current_user: str = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    try:
        response = await service.send_message_and_get_response(conversation_id, req.content)
        return SendMessageResponse(
            message_id=conversation_id,
            response=response,
            created_at=__import__('datetime').datetime.utcnow()
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error communicating with LLM service")

@router.get("/project/{project_id}", response_model=list[ConversationResponse])
async def list_project_conversations(
    project_id: str,
    current_user: str = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    conversations = await service.list_conversations(project_id)
    return [
        ConversationResponse(
            id=c.id,
            project_id=c.project_id,
            created_at=c.created_at,
            updated_at=c.updated_at
        )
        for c in conversations
    ]

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: str = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    success = await service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}
