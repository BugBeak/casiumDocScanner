# casiumDocScanner

This repository demonstrates a full-stack application for **document classification**, **field extraction**, **verification**, and **persistence** using:
- **FastAPI** + **SQLAlchemy** (backend)
- **React** + **TypeScript** (frontend)
- **SQLite** (database)

## 1. Requirements

- Python 3.9+ (any recent version should work)
- Node.js 16+ and npm (or Yarn)

## 2. Quickstart

### A. Backend

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate     # Windows



2. Install Python requirements:
```bash
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

4.Start the development server:
```bash
   npm run dev

The frontend is now running at http://localhost:5173 (Vite default) or http://localhost:3000 if create-react-app.

### C. Usage
1. In your browser, open the frontend URL (e.g., http://localhost:5173).

2. Use the Upload Form to upload an image or PDF.

3. The app calls the FastAPI /extract endpoint, which:
- Classifies the document as Passport, Driver License, or EAD (stub logic in this example).
- Extracts dummy fields (or uses OCR + LLM if you integrate real logic).
- Saves extraction results in the SQLite DB.

4. The left sidebar shows recent extractions pulled from the DB. Click one to view/edit.

5. The right panel allows you to edit the extracted fields and commit changes to the DB.
