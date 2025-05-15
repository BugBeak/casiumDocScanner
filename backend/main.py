# backend/main.py

import sys
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base
import crud, schemas

app = FastAPI()

# Use: `python main.py --init-db` to create tables
if len(sys.argv) > 1 and sys.argv[1] == "--init-db":
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Done! You can now run `uvicorn main:app --reload`")
    sys.exit(0)

# ---------------------
# DUMMY CLASSIFICATION / EXTRACTION
# ---------------------

def classify_document_type(file_bytes: bytes) -> str:
    """
    Placeholder function. 
    In reality, use a vision model or heuristic to classify:
    - passport
    - driver_license
    - ead_card
    """
    # For example, always return 'passport' for demo:
    return "passport"

def extract_fields_from_text(doc_type: str, text: str) -> dict:
    """
    Placeholder function to parse the text according to doc_type.
    Return a dict of extracted fields.
    """
    if doc_type == "passport":
        return {
            "full_name": "John Doe (demo)",
            "date_of_birth": "01/01/1990",
            "country": "United States",
            "issue_date": "01/01/2020",
            "expiration_date": "01/01/2030"
        }
    elif doc_type == "driver_license":
        return {
            "license_number": "D1234567",
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "02/02/1992",
            "issue_date": "02/02/2021",
            "expiration_date": "02/02/2025"
        }
    else:  # ead_card
        return {
            "card_number": "EAD123456",
            "category": "C09",
            "card_expires_date": "03/03/2024",
            "first_name": "Carlos",
            "last_name": "Garcia"
        }

def run_ocr_dummy(file_bytes: bytes) -> str:
    """ 
    Placeholder for OCR. Return dummy text.
    In production, run actual OCR on the file bytes.
    """
    return "Dummy text extracted from the document."

# ---------------------
# ENDPOINTS
# ---------------------

@app.post("/extract", response_model=schemas.ExtractionResponse)
async def extract(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read file bytes
    content = await file.read()
    
    # Step 1: Classify
    doc_type = classify_document_type(content)
    
    # Step 2: OCR (dummy)
    text = run_ocr_dummy(content)
    
    # Step 3: Extract fields
    fields = extract_fields_from_text(doc_type, text)
    
    # Step 4: Save to DB
    extraction = crud.create_extraction(db, doc_type, fields)
    
    # Build response
    return {
        "id": extraction.id,
        "document_type": extraction.document_type,
        "document_content": extraction.extracted_fields
    }

@app.get("/extractions", response_model=list[schemas.ExtractionResponse])
def list_recent_extractions(db: Session = Depends(get_db)):
    data = crud.list_extractions(db)
    return [
        {
            "id": item.id,
            "document_type": item.document_type,
            "document_content": item.extracted_fields
        }
        for item in data
    ]

@app.get("/extractions/{extraction_id}", response_model=schemas.ExtractionResponse)
def get_extraction(extraction_id: int, db: Session = Depends(get_db)):
    extraction = crud.get_extraction(db, extraction_id)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return {
        "id": extraction.id,
        "document_type": extraction.document_type,
        "document_content": extraction.extracted_fields
    }

@app.put("/extractions/{extraction_id}", response_model=schemas.ExtractionResponse)
def update_extraction(
    extraction_id: int, 
    updated: schemas.ExtractionCreate,
    db: Session = Depends(get_db)
):
    # just re-use the fields from updated.document_content
    extraction = crud.update_extraction(db, extraction_id, updated.document_content)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return {
        "id": extraction.id,
        "document_type": extraction.document_type,
        "document_content": extraction.extracted_fields
    }
