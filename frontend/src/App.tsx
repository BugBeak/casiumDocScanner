import React from "react";
import UploadForm from "./components/UploadForm";
import DocumentList from "./components/DocumentList";
import DocumentViewer from "./components/DocumentViewer";
import FieldsEditor from "./components/FieldsEditor";
import "./App.css";

export default function App() {
  const [selectedExtractionId, setSelectedExtractionId] = React.useState<number | null>(null);

  return (
    <div className="App" style={{ display: "flex", gap: "1rem" }}>
      {/* Left side: Upload + List of recent docs */}
      <div style={{ width: "20%", borderRight: "1px solid #ccc" }}>
        <h2>Extract New Document</h2>
        <UploadForm onUploadComplete={setSelectedExtractionId} />
        <hr/>
        <h2>Recent Extractions</h2>
        <DocumentList onSelect={setSelectedExtractionId} />
      </div>

      {/* Middle: Document Viewer */}
      <div style={{ width: "40%", borderRight: "1px solid #ccc" }}>
        <h2>Original Document View</h2>
        <DocumentViewer extractionId={selectedExtractionId} />
      </div>

      {/* Right: Fields Editor */}
      <div style={{ width: "40%" }}>
        <h2>Extracted Fields</h2>
        <FieldsEditor extractionId={selectedExtractionId} />
      </div>
    </div>
  );
}
