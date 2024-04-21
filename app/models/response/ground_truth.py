from pydantic import BaseModel


class GroundTruthResponse(BaseModel):
    document_id: int
    element_name: str
    ground_truth: str
    raw_value: str
