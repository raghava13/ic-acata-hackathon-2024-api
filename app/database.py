from sqlmodel import Session, desc, or_, select

from app.models.database.nlp import NLP
from app.models.database.nlp_accuracy import NLPAccuracy
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
    def get_nlp_result_by_nlp_id(session: Session, nlp_id: int):
        query = select(NLPDocument).where(NLPDocument.nlp_id == nlp_id)
        response = None
        try:
            response = session.exec(query).all()
        except:
            raise

        return response

    @staticmethod
    def get_nlp_accuracy_by_nlp_id(session: Session, nlp_id: int):
        query = select(NLPAccuracy).where(NLPAccuracy.nlp_id == nlp_id)
        response = None
        try:
            response = session.exec(query).all()
        except:
            raise

        return response

    # @staticmethod
    # def get_ground_truth_by_document_ids(session: Session, document_list: list[int]):
    #     query = select(GroundTruth).where(GroundTruth.document_id.in_([1, 2, 3]))
    #     response = None
    #     try:
    #         response = session.exec(query).first()
    #     except:
    #         raise

    #     return response

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

    @staticmethod
    def insert_nlp_accuracy(session: Session, nlp_accuracy_list: list[NLPAccuracy]):
        for nlp_accuracy in nlp_accuracy_list:
            session.add(nlp_accuracy)

        try:
            session.commit()
        except:
            raise
