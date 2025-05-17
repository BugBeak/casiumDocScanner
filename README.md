# casiumDocScanner

This repository demonstrates a full-stack application for **document classification**, **field extraction**, **verification**, and **persistence** using:
- **FastAPI** + **SQLAlchemy** (backend)
- **React** + **TypeScript** (frontend)
- **SQLite** (database)

## 1. Requirements

- Python 3.10.6
- Node.js 16+ and npm (or Yarn)
- Tesseract API: Download it from UB Mannheim Tesseract page. Make sure PATH variable is updated.

## 2. Quickstart
### A. Backend
1. Create and activate a Python virtual environment in backend folder:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .\.venv\Scripts\Activate.ps1     # Windows (powershell)
   (might be in bin or Scripts folder, do check)
2. Install Python requirements (in backend folder):
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   pip install -r backend/requirements.txt
3. Initialize the SQLite database (this creates the tables):
   ```bash
   cd backend
   python main.py --init-db
4. Run FastAPI (development server):
   ```bash
   uvicorn main:app --reload
The backend is now running at http://localhost:8000.

### B. Frontend
1. Open a new terminal window (keeping the backend running in the old one).
2. Navigate to frontend folder:
   ```bash
   cd frontend
3. Install dependencies:
   ```bash
   npm install
4. Start the development server:
   ```bash
   npm run dev
The frontend is now running at http://localhost:5173 (Vite default) or http://localhost:3000 if create-react-app.

### C. Usage
1. In your browser, open the frontend URL (e.g., http://localhost:5173).
2. Use the Upload Form to upload an image or PDF. You can see a preview of the uploaded document in the middle window.
3. The left sidebar shows recent extractions pulled from the DB. Click one to view its extracted fields.
4. The right panel allows you to edit the extracted fields and commit changes to the DB.

## 3. Observations
1. A big challenge of this task is reading text when the images are (a) of low resolution, and (b) full of watermarks.
2. The diversity of the files is another challenge.
   - EAD cards are most straightforward to parse and standardise because they are issued by the same country/authority, and hence, the formatting of field names is more or less consistent.
   - Passports, on the other hand, have a great deal of divergence because they are issued by different countries. One can encounter different field names, formatting, placements, and even different languages. For example, I encountered some passport images that didn't have "passport" written on them.
   - Driver's licenses lie somewhere in the middle in terms of difficulty since different US states have different formats (ignoring international licenses).
3. Off-the-shelf models like OpenAI's CLIP model can do “zero‐shot” classification by comparing an image embedding to text embeddings of your label strings. While this approach is convenient particularly when data is limited, it struggles to achieve high accuracy in our scenario because (a) the document types are quite specific (passport vs. driver license vs. EAD), and (b) watermarks and layout inconsistencies degrade performance. I incorporated the OCR reading of the file in the classification task to aid this.
4. The diversity of document designs requires a more specialized or fine‐tuned model. However, this requires gathering a representative dataset of each document type (e.g., passports from multiple countries, licenses from many states). I found the following datasets that can be helpful:
   - Passports: [Synthetic dataset of ID and Travel Document (SIDTD)](https://tc11.cvc.uab.es/datasets/SIDTD_1/), [UniDataPro Synthetic passports](https://huggingface.co/datasets/UniDataPro/synthetic-passports)
   - Driving License: [Synthetic EU Drivers licences](https://www.kaggle.com/datasets/felipebandeiraramos/synthetic-eu-drivers-licences)


## 4. Future Scope
1. Investigating advanced OCR engines (e.g., EasyOCR or commercial APIs) or image preprocessing (binarization, noise removal) to handle heavily watermarked or skewed images.
2. Implementing a pipeline that detects and crops specific fields (using object detection models like YOLO), further improving OCR accuracy by isolating text regions.
3. Incorporate language detection to switch or combine relevant OCR dictionaries.
4. Using regular expressions or, even better, LLM prompts, for more flexible field parsing.
5. A privacy-secure continuous training pipeline can really help improve this system in production.
