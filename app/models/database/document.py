from typing import Optional

from sqlmodel import Column, Field, Integer, Relationship, String

from app.models.base.camel_sql_model import CamelSQLModel


class Document(CamelSQLModel, table=True):
    __tablename__ = "DocumentXREF"  # type: ignore
    __table_args__ = {"schema": "IC_PUBLIC"}

    document_id: Optional[int] = Field(
        sa_column=Column("DocumentId", Integer, primary_key=True)
    )
    # division_code: str = Field(sa_column=Column("DivisionCode", String))
    # ic_site_id: str = Field(sa_column=Column("ICSiteId", String))
    patient_id: str = Field(sa_column=Column("CombinedDivisionMpi", String))
    name: str = Field(sa_column=Column("DocumentName", String))
    type: str = Field(sa_column=Column("DocumentTypeDescription", String))
    # document_extension_code: str = Field(
    #     sa_column=Column("DocumentExtensionCode", String)
    # )
    # document_date: datetime = Field(sa_column=Column("DocumentDate", DateTime))
    # document_create_datetime: datetime = Field(
    #     sa_column=Column("DocumentCreateDatetime", DateTime)
    # )
    # media_type_description: str = Field(
    #     sa_column=Column("MediaTypeDescription", String)
    # )
    # image_id: str = Field(sa_column=Column("ImageId", String))
    # external_image_name: str = Field(sa_column=Column("ExternalImageName", String))
    # bucket_name: str = Field(sa_column=Column("BucketName", String))
    # directory_name: str = Field(sa_column=Column("DirectoryName", String))
    # file_name: str = Field(sa_column=Column("FileName", String))
    # extracted_indicator: Optional[str] = Field(
    #     sa_column=Column("ExtractedIndicator", String)
    # )
    # nlp_status_code: str = Field(sa_column=Column("NLPStatusCode", String))
    # practice_mrn: str = Field(sa_column=Column("PracticeMRN", String))
    # enterprise_mpi: str = Field(sa_column=Column("EnterpriseMPI", String))
    # de_id_file_name: str = Field(sa_column=Column("DeIdFileName", String))
    # de_id_location_name: str = Field(sa_column=Column("DeIdLocationName", String))
    # viewed_status_flag: bool = Field(sa_column=Column("ViewedStatusFlag", Boolean))
    # audit_created_datetime: datetime = Field(
    #     sa_column=Column("AuditCreatedDatetime", DateTime)
    # )
    # audit_created_by_user_id: str = Field(
    #     sa_column=Column("AuditCreatedByUserId", String)
    # )
    # audit_modified_datetime: Optional[datetime] = Field(
    #     default=None, sa_column=Column("AuditModifiedDatetime", DateTime)
    # )
    # audit_modified_by_user_id: Optional[str] = Field(
    #     default=None, sa_column=Column("AuditModifiedByUserId", String)
    # )
    # audit_deleted_flag: bool = Field(sa_column=Column("AuditDeletedFlag", Boolean))

    ocrs: list["Ocr"] = Relationship(back_populates="document")  # type: ignore  # noqa: F821
