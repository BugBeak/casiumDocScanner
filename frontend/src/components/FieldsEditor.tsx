import React from "react";
import { getExtraction, updateExtraction } from "../api";

interface Props {
  extractionId: number | null;
}

interface ExtractionData {
  id: number;
  document_type: string;
  document_content: Record<string, any>;
}

export default function FieldsEditor({ extractionId }: Props) {
  const [extraction, setExtraction] = React.useState<ExtractionData | null>(null);
  const [fields, setFields] = React.useState<Record<string, any>>({});

  React.useEffect(() => {
    if (!extractionId) {
      setExtraction(null);
      setFields({});
      return;
    }
    (async () => {
      try {
        const data = await getExtraction(extractionId);
        setExtraction(data);
        setFields(data.document_content);
      } catch (err) {
        console.error("Failed to fetch extraction", err);
      }
    })();
  }, [extractionId]);

  if (!extractionId || !extraction) {
    return <div>No extraction selected.</div>;
  }

  const handleChange = (fieldKey: string, value: string) => {
    setFields((prev) => ({ ...prev, [fieldKey]: value }));
  };

  const handleSave = async () => {
    try {
      const updated = await updateExtraction(extraction.id, fields, extraction.document_type);
      setExtraction(updated);
      alert("Fields saved!");
    } catch (err) {
      console.error("Update error:", err);
      alert("Failed to update fields.");
    }
  };

  return (
    <div>
      <p>Document Type: {extraction.document_type}</p>
      <table>
        <tbody>
          {Object.entries(fields).map(([key, val]) => (
            <tr key={key}>
              <td><strong>{key}</strong></td>
              <td>
                <input
                  value={val}
                  onChange={(e) => handleChange(key, e.target.value)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleSave}>Save Changes</button>
    </div>
  );
}
