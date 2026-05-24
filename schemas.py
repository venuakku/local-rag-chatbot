from pydantic import BaseModel, Field


class RagChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = Field(default_factory=list)


class SessionResetRequest(BaseModel):
    session_id: str


class SessionResetResponse(BaseModel):
    status: str


class IngestResponse(BaseModel):
    status: str
    chunks_added: int
    filename: str
