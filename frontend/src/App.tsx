import React, { useState, useEffect } from "react";
import { listExtractions } from "./api"; // your API calls
import UploadForm from "./components/UploadForm";
import DocumentViewer from "./components/DocumentViewer";
import FieldsEditor from "./components/FieldsEditor";
import DocumentList from "./components/DocumentList"; // if you have it

interface Extraction {
  id: number;
  document_type: string;
  document_content: Record<string, any>;
}

export default function App() {
  // State for currently selected extraction
  const [selectedExtractionId, setSelectedExtractionId] = useState<number | null>(null);

  // State for all extractions (so we can list them, if needed)
  const [extractions, setExtractions] = useState<Extraction[]>([]);

  // A local blob URL for the *newly picked* file
  const [documentPreviewUrl, setDocumentPreviewUrl] = useState("");

  // --- Load the extraction list (on mount and on demand)
  async function fetchExtractions() {
    try {
      const data = await listExtractions();
      setExtractions(data);
    } catch (err) {
      console.error("Failed to list extractions", err);
    }
  }

  // Load the list on mount
  useEffect(() => {
    fetchExtractions();
  }, []);

  // Called after a successful upload
  function handleUploadComplete(newExtractionId: number) {
    // 1) Mark that extraction as selected
    setSelectedExtractionId(newExtractionId);
    // 2) Refresh the list so the new item shows up
    fetchExtractions();
  }

  // Called when the user picks a file in the upload form
  // We store that as a local preview
  function handlePreviewAvailable(previewUrl: string) {
    setDocumentPreviewUrl(previewUrl);
  }

  // If you have a DocumentList, it might look like:
  <DocumentList
    extractions={extractions}
    onSelect={(id) => {
      setSelectedExtractionId(id);
      setDocumentPreviewUrl(""); // we don't have a preview for older docs
    }}
  />

  return (
    <div style={{ display: "flex", gap: "1rem" }}>
      {/* LEFT COLUMN */}
      <div style={{ width: "25%", borderRight: "1px solid #ccc" }}>
        <h2>Extract New Document</h2>
        <UploadForm
          onUploadComplete={handleUploadComplete}
          onPreviewAvailable={handlePreviewAvailable}
        />

        <hr />
        <h2>Recent Extractions</h2>
        <DocumentList
          extractions={extractions}
          onSelect={(id) => {
            setSelectedExtractionId(id);
            setDocumentPreviewUrl("");
          }}
        />

      </div>

      {/* MIDDLE COLUMN: Document Viewer */}
      <div style={{ width: "35%", borderRight: "1px solid #ccc" }}>
        <h2>Original Document View</h2>
        <DocumentViewer previewUrl={documentPreviewUrl} />
      </div>

      {/* RIGHT COLUMN: Fields Editor */}
      <div style={{ width: "40%" }}>
        <h2>Extracted Fields</h2>
        <FieldsEditor extractionId={selectedExtractionId} />
      </div>
    </div>
  );
}
