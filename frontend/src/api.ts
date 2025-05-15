// frontend/src/api.ts

export const BASE_URL = "http://localhost:8000"; // Adjust if needed

// Upload a file for extraction
export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/extract`, {
    method: "POST",
    body: formData
  });
  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }
  return response.json();
}

// Get the list of recent extractions
export async function listExtractions() {
  const response = await fetch(`${BASE_URL}/extractions`);
  if (!response.ok) {
    throw new Error("Could not fetch extractions");
  }
  return response.json();
}

// Get a single extraction by ID
export async function getExtraction(id: number) {
  const response = await fetch(`${BASE_URL}/extractions/${id}`);
  if (!response.ok) {
    throw new Error("Could not fetch extraction");
  }
  return response.json();
}

// Update extraction fields
export async function updateExtraction(id: number, newFields: any, docType: string) {
  const body = {
    document_type: docType,
    document_content: newFields
  };
  const response = await fetch(`${BASE_URL}/extractions/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!response.ok) {
    throw new Error("Failed to update extraction");
  }
  return response.json();
}
