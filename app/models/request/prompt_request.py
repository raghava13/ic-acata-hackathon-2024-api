from typing import Optional

from app.models.base.camel_model import CamelModel


class PromptRequest(CamelModel):
    template: str
    knowledge: str
    context: Optional[str] = None
    user_content: str
    frequency_penalty: Optional[float] = 0
    max_tokens: Optional[int] = 1000
    presence_penalty: Optional[float] = 0
    stop: Optional[str | list[str]] = None
    temperature: Optional[float] = 0.25
    top_p: Optional[float] = 0.1
