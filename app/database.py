from sqlmodel import Session, desc, or_, select

from app.models.database.nlp import NLP
from app.models.database.nlp_document import NLPDocument
from app.models.database.nlp_document_element import NLPDocumentElement
from app.models.database.ocr import Ocr
from app.models.request.nlp_request import NLPRequest


class Database:
    @staticmethod
    def get_ocr_by_document_id(session: Session, document_id: int):
        query = (
            select(Ocr.ocr_result_text)
            .where(
                Ocr.document_id == document_id,
                or_(Ocr.audit_deleted_flag == 0, Ocr.audit_deleted_flag == None),  # noqa: E711
            )
            .order_by(desc(Ocr.ocr_result_id))
        )
        response = None
        try:
            response = session.exec(query).first()
        except:
            raise

        return response

    @staticmethod
    def insert_nlp(session: Session, request: NLPRequest):
        nlp = NLP.model_validate(request)

        session.add(nlp)

        try:
            session.commit()
        except:
            raise

        return nlp.nlp_id

    @staticmethod
    def insert_nlp_document(
        session: Session, nlp_id: int, document_id: int, response: str
    ):
        nlp_document = NLPDocument(
            nlp_id=nlp_id, document_id=document_id, response=response
        )

        session.add(nlp_document)

        try:
            session.commit()
        except:
            raise

        return nlp_document.nlp_document_id

    @staticmethod
    def insert_nlp_document_element(
        session: Session, nlp_document_element_list: list[NLPDocumentElement]
    ):
        for nlp_document_element in nlp_document_element_list:
            session.add(nlp_document_element)

        try:
            session.commit()
        except:
            raise
