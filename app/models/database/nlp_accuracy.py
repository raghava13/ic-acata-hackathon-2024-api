from datetime import datetime, timezone
from typing import Optional

from sqlmodel import (
    Column,
    DateTime,
    Field,
    Float,
    ForeignKey,
    Integer,
    Relationship,
    String,
)

from app.models.base.camel_sql_model import CamelSQLModel
from app.models.database.nlp import NLP


class NLPAccuracy(CamelSQLModel, table=True):
    __tablename__ = "NLPAccuracy"  # type: ignore
    __table_args__ = {"schema": "HACKATHON"}

    nlp_accuracy_id: Optional[int] = Field(
        default=None,
        sa_column=Column("NLPAccuracyId", Integer, primary_key=True),
    )
    nlp_id: int = Field(
        sa_column=Column("NLPId", Integer, ForeignKey("HACKATHON.NLP.NLPId"))
    )
    element_name: str = Field(sa_column=Column("ElementName", String))
    accuracy: float = Field(sa_column=Column("Accuracy", Float))
    document_count: int = Field(sa_column=Column("DocumentCount", String))
    created_date: Optional[datetime] = Field(
        default=datetime.now(timezone.utc), sa_column=Column("CreatedDate", DateTime)
    )

    nlp: NLP | None = Relationship(back_populates="nlp_accuracies")
