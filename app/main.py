import json
from typing import Annotated, Sequence

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Path
from langchain_core.prompts import PromptTemplate
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware

from app.azure_open_ai import AzureOpenAIService
from app.database import Database
from app.models.database.document import Document
from app.models.database.nlp_accuracy import NLPAccuracy
from app.models.database.nlp_document import NLPDocument
from app.models.database.nlp_document_element import NLPDocumentElement
from app.models.request.nlp_request import NLPRequest
from app.models.request.prompt_request import PromptRequest
from app.models.response.nlp_element_response import NLPElementResponse
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


# @app.get("/ocr/{document_id}", response_model=str)
# def get_ocr_by_document_id(
#     document_id: Annotated[int, Path(title="The Document ID", gt=0)],
#     session: Annotated[Session, Depends(SQLSession())],
# ):
#     response = Database.get_ocr_by_document_id(session, document_id)

#     if not response:
#         raise HTTPException(status_code=404, detail="Not found")

#     return response


@app.get("/nlp/result/{nlp_id}", response_model=Sequence[NLPDocument])
def get_nlp_result_by_nlp_id(
    nlp_id: Annotated[int, Path(title="The NLP ID", gt=0)],
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_nlp_result_by_nlp_id(session, nlp_id)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.get("/nlp/element/{nlp_id}", response_model=Sequence[NLPElementResponse])
def get_nlp_element_by_nlp_id(
    nlp_id: Annotated[int, Path(title="The NLP ID", gt=0)],
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_nlp_element_by_nlp_id(session, nlp_id)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.get("/nlp/accuracy/{nlp_id}", response_model=Sequence[NLPAccuracy])
def get_nlp_accuracy_by_nlp_id(
    nlp_id: Annotated[int, Path(title="The NLP ID", gt=0)],
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_nlp_accuracy_by_nlp_id(session, nlp_id)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.get("/nlp/latest/accuracy", response_model=Sequence[NLPAccuracy])
def get_latest_element_accuracy(
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_latest_element_accuracy(session)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.get("/nlp/latest/accuracy/{element_name}", response_model=Sequence[NLPAccuracy])
def get_latest_accuracy_by_element(
    element_name: Annotated[str, Path(title="The Element Name")],
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_latest_accuracy_by_element(session, element_name)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.get("/document", response_model=Sequence[Document])
def get_documents(
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_documents(session)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@app.post("/nlp/process", response_model=int)
def run_azure_open_ai(
    request: NLPRequest,
    session: Annotated[Session, Depends(SQLSession())],
    background_tasks: BackgroundTasks,
):
    nlp_id = Database.insert_nlp(session, request)

    if not nlp_id:
        return

    background_tasks.add_task(nlp_background_process, session, request, nlp_id)

    return nlp_id


@app.post("/nlp/prompt-tuning", response_model=str)
def run_azure_open_ai_prompt(request: PromptRequest):
    prompt_template = PromptTemplate(
        input_variables=["knowledge", "context"],
        template=request.template,
    )

    system_content = prompt_template.format(
        knowledge=request.knowledge, context=request.context
    )

    return AzureOpenAIService.run_azure_open_ai(
        system_content,
        request.user_content,
        request.frequency_penalty,
        request.presence_penalty,
        request.temperature,
        request.top_p,
        request.max_tokens,
        request.stop,
    )


def nlp_background_process(session: Session, request: NLPRequest, nlp_id: int):
    prompt_template = PromptTemplate(
        input_variables=["knowledge", "context"],
        template=request.template,
    )
    for document_id in request.document_list:
        ocr_text = Database.get_ocr_by_document_id(session, document_id)

        if not ocr_text:
            continue

        system_content = prompt_template.format(
            knowledge=request.knowledge, context=ocr_text
        )

        response = AzureOpenAIService.run_azure_open_ai(
            system_content,
            request.user_content,
            request.frequency_penalty,
            request.presence_penalty,
            request.temperature,
            request.top_p,
            request.max_tokens,
            request.stop,
        )

        if not response or response == '["None"]':
            continue

        nlp_document_id = Database.insert_nlp_document(
            session, nlp_id, document_id, response
        )
        if not nlp_document_id:
            continue

        response = json.loads(response)
        nlp_document_element_list: list[NLPDocumentElement] = []
        for key, value in response.items():
            if isinstance(value, list):
                value = value[0]

            nlp_document_element = NLPDocumentElement(
                nlp_document_id=nlp_document_id,
                element_name=key,
                raw_value=value,
            )
            nlp_document_element_list.append(nlp_document_element)

        if len(nlp_document_element_list) > 0:
            Database.insert_nlp_document_element(session, nlp_document_element_list)

    ground_truth_list = Database.get_ground_truth_by_nlp_id(session, nlp_id)
    Database.insert_nlp_accuracy(
        session, nlp_id, len(request.document_list), ground_truth_list
    )


# @app.get("/nlp/accuracy2/{nlp_id}", response_model=Sequence[GroundTruthResponse])
# def get_nlp_accuracy_by_nlp_id2(
#     nlp_id: Annotated[int, Path(title="The NLP ID", gt=0)],
#     session: Annotated[Session, Depends(SQLSession())],
# ):
#     response = Database.get_ground_truth_by_nlp_id(session, nlp_id)

#     if not response:
#         raise HTTPException(status_code=404, detail="Not found")

#     return response
