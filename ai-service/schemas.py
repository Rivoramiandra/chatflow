from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):

    role: Literal["client", "agent"]

    content: str = Field(
        min_length=1,
        max_length=5000
    )


class ConversationRequest(BaseModel):

    conversation: list[Message]

    language: str = "French"

    tone: str = "auto"


class ResponseSuggestion(BaseModel):

    id: int

    style: str

    text: str = Field(
        min_length=150,
        max_length=500
    )


class GenerateResponse(BaseModel):

    language: str

    topic: str

    client_intent: str

    tone: str

    responses: list[ResponseSuggestion]