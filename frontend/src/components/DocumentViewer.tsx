import React from "react";

interface Props {
  extractionId: number | null;
}

export default function DocumentViewer({ extractionId }: Props) {
  if (!extractionId) {
    return <div>Select a document from the list to view.</div>;
  }

  // In a real app, you might fetch the actual file or a link to display here.
  // For now, show a placeholder text or a placeholder image.

  return (
    <div>
      <p>Document ID: {extractionId}</p>
      <div style={{ border: "1px solid #999", padding: "1rem" }}>
        <em>Placeholder for original document preview (PDF/image)</em>
      </div>
    </div>
  );
}
