from datetime import datetime
from typing import Optional

from sqlmodel import (
    Boolean,
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
from app.models.database.document import Document


class Ocr(CamelSQLModel, table=True):
    __tablename__ = "OCRResult"  # type: ignore
    __table_args__ = {"schema": "CURATION_WB"}

    ocr_result_id: Optional[int] = Field(
        default=None,
        sa_column=Column("OCRResultId", Integer, primary_key=True),
    )
    document_id: int = Field(
        sa_column=Column(
            "DocumentId", Integer, ForeignKey("IC_PUBLIC.DocumentXREF.DocumentId")
        )
    )
    vendor_name: str = Field(sa_column=Column("VendorName", String))
    ocr_result_text: str = Field(sa_column=Column("OCRResultText", String))
    ocr_model_name: str = Field(sa_column=Column("OCRModelName", String))
    time_taken_in_seconds_value: float = Field(
        sa_column=Column("TimeTakenInSecondsValue", Float)
    )
    ocr_result_status_code: str = Field(sa_column=Column("OCRResultStatusCode", String))
    audit_created_datetime: datetime = Field(
        sa_column=Column("AuditCreatedDatetime", DateTime)
    )
    audit_created_by_user_id: str = Field(
        sa_column=Column("AuditCreatedByUserId", String)
    )
    audit_modified_datetime: Optional[datetime] = Field(
        sa_column=Column("AuditModifiedDatetime", DateTime)
    )
    audit_modified_by_user_id: Optional[str] = Field(
        sa_column=Column("AuditModifiedByUserId", String)
    )
    audit_deleted_flag: bool = Field(sa_column=Column("AuditDeletedFlag", Boolean))

    document: Document | None = Relationship(back_populates="ocrs")
