# backend/crud.py

from sqlalchemy.orm import Session
import models, schemas

def create_extraction(db: Session, doc_type: str, fields: dict):
    db_extraction = models.DocumentExtraction(
        document_type=doc_type,
        extracted_fields=fields
    )
    db.add(db_extraction)
    db.commit()
    db.refresh(db_extraction)
    return db_extraction

def get_extraction(db: Session, extraction_id: int):
    return db.query(models.DocumentExtraction).filter(models.DocumentExtraction.id == extraction_id).first()

def list_extractions(db: Session, limit: int = 20):
    return db.query(models.DocumentExtraction).order_by(models.DocumentExtraction.id.desc()).limit(limit).all()

def update_extraction(db: Session, extraction_id: int, fields: dict):
    db_extraction = get_extraction(db, extraction_id)
    if db_extraction:
        db_extraction.extracted_fields = fields
        db.commit()
        db.refresh(db_extraction)
    return db_extraction
