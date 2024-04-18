from typing import Optional

from sqlmodel import (
    Column,
    Field,
    Integer,
    String,
)

from app.models.base.camel_sql_model import CamelSQLModel


class GroundTruth(CamelSQLModel, table=True):
    __tablename__ = "GroundTruth"  # type: ignore
    __table_args__ = {"schema": "CURATION_WB"}

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("ID", Integer, primary_key=True),
    )
    element_name: str = Field(sa_column=Column("ElementName", String))
    ground_truth: str = Field(sa_column=Column("GTValue", String))
    document_id: int = Field(sa_column=Column("DocumentId", Integer))
