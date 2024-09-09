from pydantic import BaseModel, constr
from typing import List, Literal


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: constr(min_length=1) # type: ignore


class ChatHistory(BaseModel):
    history: List[Message]
