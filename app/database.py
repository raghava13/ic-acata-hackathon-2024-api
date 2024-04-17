from sqlmodel import Session, desc, or_, select

from app.models.ocr import Ocr


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
