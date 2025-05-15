# backend/models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()

class DocumentExtraction(Base):
    __tablename__ = "document_extractions"

    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String, nullable=False)
    extracted_fields = Column(JSON)  # Store fields in JSON form
