import React from "react";

interface Props {
  previewUrl: string;
}

export default function DocumentViewer({ previewUrl }: Props) {
  // If there's no preview URL, it means either we haven't selected a file,
  // or we're looking at an older extraction that has no stored file.
  if (!previewUrl) {
    return <div>No document selected or no preview available.</div>;
  }

  // Naive PDF vs. image detection by file extension or MIME type
  const isPdf = previewUrl.toLowerCase().includes(".pdf");

  return (
    <div style={{ width: "100%", overflow: "auto" }}>
      {isPdf ? (
        <iframe
          src={previewUrl}
          title="PDF Preview"
          style={{ width: "100%", height: "600px" }}
        />
      ) : (
        <img
          src={previewUrl}
          alt="Document Preview"
          style={{ maxWidth: "100%", height: "auto" }}
        />
      )}
    </div>
  );
}
