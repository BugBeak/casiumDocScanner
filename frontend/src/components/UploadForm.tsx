import React, { useState } from "react";
import { uploadDocument } from "../api";

interface Props {
  onUploadComplete: (id: number) => void;
  onPreviewAvailable: (previewUrl: string) => void;
}

export default function UploadForm({ onUploadComplete, onPreviewAvailable }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  function handleFileSelect(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files || e.target.files.length === 0) return;
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    // Generate a blob URL for local preview
    const previewUrl = URL.createObjectURL(selectedFile);
    // Pass it to the parent so it can show in DocumentViewer
    onPreviewAvailable(previewUrl);
  }

  async function handleUpload() {
    if (!file) return;
    setLoading(true);
    try {
      const response = await uploadDocument(file);
      // The response should contain { id: number, ... }
      onUploadComplete(response.id);
    } catch (err) {
      console.error("Upload error:", err);
      alert("Failed to upload!");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input
        type="file"
        onChange={handleFileSelect}
        accept=".jpg,.jpeg,.png,.pdf" // optional, if you want PDF support
      />
      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}
