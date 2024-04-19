from datetime import datetime, timezone
from typing import Optional

from sqlmodel import (
    Column,
    DateTime,
    Field,
    ForeignKey,
    Integer,
    Relationship,
    String,
)

from app.models.base.camel_sql_model import CamelSQLModel
from app.models.database.nlp_document import NLPDocument


class NLPDocumentElement(CamelSQLModel, table=True):
    __tablename__ = "NLPDocumentElement"  # type: ignore
    __table_args__ = {"schema": "HACKATHON"}

    nlp_document_element_id: Optional[int] = Field(
        default=None,
        sa_column=Column("NLPDocumentElementId", Integer, primary_key=True),
    )
    nlp_document_id: int = Field(
        sa_column=Column(
            "NLPDocumentId", Integer, ForeignKey("HACKATHON.NLPDocument.NLPDocumentId")
        )
    )
    element_name: str = Field(sa_column=Column("ElementName", String))
    raw_value: str = Field(sa_column=Column("RawValue", String))
    created_date: Optional[datetime] = Field(
        default=datetime.now(timezone.utc), sa_column=Column("CreatedDate", DateTime)
    )

    nlp_document: NLPDocument | None = Relationship(
        back_populates="nlp_document_elements"
    )
