from datetime import datetime

from sqlmodel import Session, col, desc, or_, select, text

from app.models.database.document import Document
from app.models.database.ground_truth import GroundTruth
from app.models.database.nlp import NLP
from app.models.database.nlp_accuracy import NLPAccuracy
from app.models.database.nlp_document import NLPDocument
from app.models.database.nlp_document_element import NLPDocumentElement
from app.models.database.ocr import Ocr
from app.models.request.nlp_request import NLPRequest
from app.models.response.ground_truth import GroundTruthResponse


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
    def get_nlp_element_by_nlp_id(session: Session, nlp_id: int):
        query = (
            select(
                NLPDocumentElement.nlp_document_element_id,
                NLPDocumentElement.nlp_document_id,
                NLPDocumentElement.element_name,
                NLPDocumentElement.raw_value,
                NLPDocumentElement.created_date,
                GroundTruth.ground_truth,
                GroundTruth.document_id,
            )
            .join(
                NLPDocument,
                NLPDocumentElement.nlp_document_id == NLPDocument.nlp_document_id,
            )
            .join(GroundTruth, NLPDocument.document_id == GroundTruth.document_id)
            .where(
                NLPDocumentElement.element_name == GroundTruth.element_name,
                NLPDocument.nlp_id == nlp_id,
            )
        )
        response = None
        try:
            response = [each._asdict() for each in session.exec(query).all()]
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

    @staticmethod
    def get_latest_element_accuracy(session: Session):
        query = (
            select(NLPAccuracy)
            .where(
                col(NLPAccuracy.nlp_accuracy_id).in_(
                    text(
                        "SELECT MAX(NLPAccuracyId) FROM HACKATHON.NLPAccuracy GROUP BY ElementName"
                    )
                )
            )
            .limit(25)
        )

        response = None
        try:
            response = session.exec(query).all()
        except:
            raise

        return response

    @staticmethod
    def get_latest_accuracy_by_element(session: Session, element_name: str):
        query = (
            select(NLPAccuracy)
            .where(NLPAccuracy.element_name == element_name)
            .limit(25)
            .order_by(desc(NLPAccuracy.nlp_accuracy_id))
        )
        response = None
        try:
            response = session.exec(query).all()
        except:
            raise

        return response

    @staticmethod
    def get_documents(session: Session):
        query = select(Document).where(
            col(Document.document_id).in_(
                text("SELECT DISTINCT DocumentId FROM CURATION_WB.GroundTruth")
            )
        )
        response = None
        try:
            response = session.exec(query).all()
        except:
            raise

        return response

    @staticmethod
    def get_ground_truth_by_nlp_id(session: Session, nlp_id: int):
        query = (
            select(
                NLPDocument.document_id,
                NLPDocumentElement.element_name,
                NLPDocumentElement.raw_value,
                GroundTruth.ground_truth,
            )
            .join(
                NLPDocument,
                NLPDocument.nlp_document_id == NLPDocumentElement.nlp_document_id,
            )
            .join(GroundTruth, GroundTruth.document_id == NLPDocument.document_id)
            .where(
                NLPDocumentElement.element_name == GroundTruth.element_name,
                NLPDocument.nlp_id == nlp_id,
            )
        )
        response = None
        try:
            response = [each._asdict() for each in session.exec(query).all()]
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

    @staticmethod
    def insert_nlp_accuracy(
        session: Session,
        nlp_id: int,
        document_count: int,
        ground_truth_list: list[GroundTruthResponse],
    ):
        accuracy_list = {}

        for gt in ground_truth_list:
            element_name: str = gt["element_name"]
            ground_truth = gt["ground_truth"]
            raw_value = gt["raw_value"]

            if element_name.endswith("date"):
                try:
                    ground_truth = str(
                        datetime.strptime(ground_truth, "%m/%d/%Y").date()
                    )
                    raw_value = str(datetime.strptime(raw_value, "%m/%d/%Y").date())
                except:
                    pass

            if ground_truth.lower() == raw_value.lower():
                if element_name in accuracy_list:
                    accuracy_list[element_name] += 1
                else:
                    accuracy_list[element_name] = 1
            else:
                if element_name not in accuracy_list:
                    accuracy_list[element_name] = 0

        for key, value in accuracy_list.items():
            nlp_accuracy = NLPAccuracy(
                nlp_id=nlp_id,
                element_name=key,
                accuracy=100 * value / document_count,
                document_count=document_count,
            )
            session.add(nlp_accuracy)

        try:
            session.commit()
        except:
            raise
