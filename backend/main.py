"""
main.py
---------
Example FastAPI backend that:
1. Classifies an uploaded image/PDF into doc types (passport, driver_license, ead_card) 
   using a Hugging Face ViT pipeline (naive approach).
2. Runs OCR with pytesseract to extract text from the image.
3. Extracts fields from that text (also naive).
4. Persists the results in a SQLite DB.

Requirements:
  pip install fastapi uvicorn sqlalchemy pydantic python-multipart
  pip install transformers torch torchvision pillow pytesseract

Also, install Tesseract on your system.
"""

import sys
import io
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image  # pillow for image loading
import pytesseract
from transformers import pipeline

from database import engine, get_db
from models import Base
import crud, schemas

# ---------------------
# INITIALIZE FastAPI
# ---------------------
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# COMMAND: INIT-DB
# ---------------------
if len(sys.argv) > 1 and sys.argv[1] == "--init-db":
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Done! You can now run `uvicorn main:app --reload`")
    sys.exit(0)

# ---------------------
# LOAD ViT MODEL for CLASSIFICATION
# ---------------------
# This pipeline is purely for demonstration. In production, you'd use a custom/fine-tuned model.
classifier = pipeline("image-classification", model="google/vit-base-patch16-224", device=-1)
# classifier = pipeline("image-classification", model="microsoft/resnet-50")


def classify_document_type(file_bytes: bytes) -> str:
    """
    Use a Hugging Face ViT pipeline to predict a label from the image.
    Then map that label (or text of top prediction) to one of:
      - 'passport'
      - 'driver_license'
      - 'ead_card'
    This is naive unless you have a specialized or fine-tuned model.
    """

    # 1. Load bytes into a PIL image:
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

    # 2. Run classification pipeline (top 1)
    predictions = classifier(image, top_k=1)
    top_label = predictions[0]["label"].lower()  # e.g. "photocopier", "envelope", "id card", etc.
    
    # 3. Simple matching logic
    #    Real approach would need a specialized dataset or fine-tuning.
    if "passport" in top_label:
        return "passport"
    elif "license" in top_label or "id" in top_label:
        return "driver_license"
    elif "card" in top_label:
        return "ead_card"
    else:
        # fallback if we can't guess
        return "passport"  # default to passport as a fallback


def load_file_as_image(file_bytes: bytes) -> Image.Image:
    """
    1) Attempt to open as an image. If that fails, assume PDF.
    2) If PDF, convert first page to a PIL image using pdf2image.
    """
    try:
        # Try opening as an image
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        return img
    except UnidentifiedImageError:
        # Maybe it's a PDF? Convert from PDF to the first page
        pages = convert_from_bytes(file_bytes, dpi=200, first_page=1, last_page=1)
        # We'll just take the first page
        if not pages:
            raise HTTPException(status_code=400, detail="Could not convert PDF to image.")
        return pages[0].convert("RGB")


def run_ocr(file_bytes: bytes) -> str:
    """
    Run Tesseract OCR to extract text from an image.
    If the upload is a PDF, you'd first convert to an image (via pdf2image or similar).
    This example just assumes images for simplicity.
    """
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    text = pytesseract.image_to_string(image)
    print(text)
    return text

def extract_fields_from_text(doc_type: str, text: str) -> dict:
    """
    Naive approach: parse the text based on doc_type.
    In production, you'd use regex, a custom NER model, or an LLM approach to reliably parse fields.
    """
    print(text)
    if doc_type == "passport":
        # We'll track synonyms for 'Passport No', 'Surname', 'Given Name', etc.
        passport_no = "Unknown"
        full_name = "Unknown"
        first_name = "Unknown"
        last_name = "Unknown"
        date_of_birth = "Unknown"
        country = "Unknown"
        issue_date = "Unknown"
        expiration_date = "Unknown"

        for line in text.split("\n"):
            line_lower = line.lower()

            # Passport number synonyms
            if "passport no" in line_lower or "passport number" in line_lower:
                passport_no = line.split(":", 1)[-1].strip()

            # If the passport says "Surname:" or "Given Name:"
            if "surname" in line_lower or "last name" in line_lower:
                last_name = line.split(":", 1)[-1].strip()
            if "given name" in line_lower or "first name" in line_lower:
                first_name = line.split(":", 1)[-1].strip()

            # Some passports might just say "Name:"
            if "name:" in line_lower:
                full_name = line.split(":", 1)[-1].strip()

            # Date of Birth synonyms
            if "dob:" in line_lower or "date of birth:" in line_lower:
                date_of_birth = line.split(":", 1)[-1].strip()

            # Country
            if "country:" in line_lower:
                country = line.split(":", 1)[-1].strip()

            # Issue date
            if "issue date:" in line_lower:
                issue_date = line.split(":", 1)[-1].strip()

            # Expiry synonyms
            if "expiry date:" in line_lower or "expiration date:" in line_lower:
                expiration_date = line.split(":", 1)[-1].strip()
            
            if full_name=="unknown":
                full_name = first_name+last_name

        return {
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "country": country,
            "issue_date": issue_date,
            "expiration_date": expiration_date,
        }

    elif doc_type == "driver_license":
        license_number = "Unknown"
        first_name = "Unknown"
        last_name = "Unknown"
        date_of_birth = "Unknown"
        issue_date = "Unknown"
        expiration_date = "Unknown"

        for line in text.split("\n"):
            line_lower = line.lower()
            if "license no" in line_lower or "license #" in line_lower:
                license_number = line.split(":", 1)[-1].strip()
            if "first name" in line_lower:
                first_name = line.split(":", 1)[-1].strip()
            if "last name" in line_lower:
                last_name = line.split(":", 1)[-1].strip()
            if "dob:" in line_lower or "date of birth:" in line_lower:
                date_of_birth = line.split(":", 1)[-1].strip()
            if "issue date:" in line_lower:
                issue_date = line.split(":", 1)[-1].strip()
            if "exp date:" in line_lower or "expiration date:" in line_lower:
                expiration_date = line.split(":", 1)[-1].strip()

        return {
            "license_number": license_number,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "issue_date": issue_date,
            "expiration_date": expiration_date,
        }

    else:  # ead_card
        card_number = "Unknown"
        category = "Unknown"
        card_expires_date = "Unknown"
        first_name = "Unknown"
        last_name = "Unknown"

        for line in text.split("\n"):
            line_lower = line.lower()
            if "card number:" in line_lower:
                card_number = line.split(":", 1)[-1].strip()
            if "category:" in line_lower:
                category = line.split(":", 1)[-1].strip()
            if "expires:" in line_lower or "card expires:" in line_lower:
                card_expires_date = line.split(":", 1)[-1].strip()
            if "first name:" in line_lower:
                first_name = line.split(":", 1)[-1].strip()
            if "last name:" in line_lower:
                last_name = line.split(":", 1)[-1].strip()

        return {
            "card_number": card_number,
            "category": category,
            "card_expires_date": card_expires_date,
            "first_name": first_name,
            "last_name": last_name,
        }


# ---------------------
# ENDPOINTS
# ---------------------

@app.post("/extract", response_model=schemas.ExtractionResponse)
async def extract(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Read file bytes
    content = await file.read()
    image = load_file_as_image(content)

    # 2. Classify
    doc_type = classify_document_type(content)

    # 3. OCR
    text = run_ocr(content)

    # 4. Extract fields from text
    fields = extract_fields_from_text(doc_type, text)

    # 5. Save to DB
    extraction = crud.create_extraction(db, doc_type, fields)
    
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
    extraction = crud.update_extraction(db, extraction_id, updated.document_content)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return {
        "id": extraction.id,
        "document_type": extraction.document_type,
        "document_content": extraction.extracted_fields
    }