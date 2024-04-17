from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlmodel import Session

from app.database import Database
from app.sql_database import SQLSession

app = FastAPI()


@app.get("/")
def get_root():
    return {"message": "IC ACATA HACKATHON 2024 API is running..."}


@app.get("/ocr/{document_id}")
def get_ocr_by_document_id(
    document_id: Annotated[int, Path(title="The Document ID", gt=0)],
    session: Annotated[Session, Depends(SQLSession())],
):
    response = Database.get_ocr_by_document_id(session, document_id)

    if not response:
        raise HTTPException(status_code=404, detail="Not found")
