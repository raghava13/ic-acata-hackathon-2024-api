from datetime import datetime

from app.models.base.camel_model import CamelModel


class NLPElementResponse(CamelModel):
    nlp_document_element_id: int
    nlp_document_id: int
    element_name: str
    raw_value: str
    created_date: datetime
    ground_truth: str
    document_id: int
