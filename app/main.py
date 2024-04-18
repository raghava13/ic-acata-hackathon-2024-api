import json
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware

from app.azure_open_ai import AzureOpenAIService
from app.database import Database
from app.models.database.nlp_document_element import NLPDocumentElement
from app.models.request.nlp_request import NLPRequest
from app.sql_database import SQLSession

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=["*"],
)


@app.get("/")
def get_root():
    return {"message": "IC ACATA HACKATHON 2024 API is running..."}


@app.get("/ocr/{document_id}", response_model=str)
def get_ocr_by_document_id(
    document_id: Annotated[int, Path(title="The Document ID", gt=0)],
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_ocr_by_document_id(session, document_id)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.post("/nlp", response_model=str)
def run_azure_open_ai(
    request: NLPRequest,
    session: Annotated[Session, Depends(SQLSession())],
):
    nlp_id = Database.insert_nlp(session, request)

    if not nlp_id:
        return

    for document_id in request.document_list:
        ocr_text = Database.get_ocr_by_document_id(session, document_id)

        if not ocr_text:
            continue

        response = AzureOpenAIService.run_azure_open_ai(request, ocr_text)

        if not response or response == '["None"]':
            continue

        nlp_document_id = Database.insert_nlp_document(
            session, nlp_id, document_id, response
        )
        if not nlp_document_id:
            continue

        response = json.loads(response)
        nlp_document_element_list = []
        for key, value in response.items():
            nlp_document_element = NLPDocumentElement(
                nlp_document_id=nlp_document_id,
                element_name=key,
                raw_value=value,
            )
            nlp_document_element_list.append(nlp_document_element)

        if len(nlp_document_element_list) > 0:
            Database.insert_nlp_document_element(session, nlp_document_element_list)

    return "Success"
