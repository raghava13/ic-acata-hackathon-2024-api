from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Column, DateTime, Field, ForeignKey, Integer, Relationship, String

from app.models.base.camel_sql_model import CamelSQLModel
from app.models.database.nlp import NLP


class NLPDocument(CamelSQLModel, table=True):
    __tablename__ = "NLPDocument"  # type: ignore
    __table_args__ = {"schema": "HACKATHON"}

    nlp_document_id: Optional[int] = Field(
        default=None,
        sa_column=Column("NLPDocumentId", Integer, primary_key=True),
    )
    nlp_id: int = Field(
        sa_column=Column("NLPId", Integer, ForeignKey("HACKATHON.NLP.NLPId"))
    )
    document_id: int = Field(sa_column=Column("DocumentId", Integer))
    response: str = Field(sa_column=Column("Response", String))
    created_date: Optional[datetime] = Field(
        default=datetime.now(timezone.utc), sa_column=Column("CreatedDate", DateTime)
    )

    nlp: NLP | None = Relationship(back_populates="nlp_documents")

    nlp_document_elements: list["NLPDocumentElement"] = Relationship(  # noqa: F821 # type: ignore
        back_populates="nlp_document"
    )
