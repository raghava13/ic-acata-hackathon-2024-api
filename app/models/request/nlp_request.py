from app.models.request.prompt_request import PromptRequest


class NLPRequest(PromptRequest):
    name: str
    document_list: list[int]
