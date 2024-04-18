from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Column, DateTime, Field, Float, Integer, Relationship, String

from app.models.base.camel_sql_model import CamelSQLModel


class NLP(CamelSQLModel, table=True):
    __tablename__ = "NLP"  # type: ignore
    __table_args__ = {"schema": "HACKATHON"}

    nlp_id: Optional[int] = Field(
        default=None, sa_column=Column("NLPId", Integer, primary_key=True)
    )
    template: str = Field(sa_column=Column("Template", String))
    knowledge: str = Field(sa_column=Column("Knowledge", String))
    user_content: str = Field(sa_column=Column("UserContent", String))
    frequency_penalty: Optional[float] = Field(
        sa_column=Column("FrequencyPenalty", Float)
    )
    presence_penalty: Optional[float] = Field(
        sa_column=Column("PresencePenalty", Float)
    )
    temperature: Optional[float] = Field(sa_column=Column("Temperature", Float))
    top_p: Optional[float] = Field(sa_column=Column("TopP", Float))
    max_tokens: Optional[int] = Field(sa_column=Column("MaxTokens", Integer))
    created_date: Optional[datetime] = Field(
        default=datetime.now(timezone.utc), sa_column=Column("CreatedDate", DateTime)
    )

    nlp_documents: list["NLPDocument"] = Relationship(  # noqa: F821 # type: ignore
        back_populates="nlp"
    )

    nlp_accuracies: list["NLPAccuracy"] = Relationship(  # noqa: F821 # type: ignore
        back_populates="nlp"
    )
