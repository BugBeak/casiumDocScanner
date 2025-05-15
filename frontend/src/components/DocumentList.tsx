import React from "react";
import { listExtractions } from "../api";

interface Extraction {
  id: number;
  document_type: string;
  document_content: Record<string, any>;
}

interface Props {
  onSelect: (id: number) => void;
}

export default function DocumentList({ onSelect }: Props) {
  const [extractions, setExtractions] = React.useState<Extraction[]>([]);

  React.useEffect(() => {
    (async () => {
      try {
        const data = await listExtractions();
        setExtractions(data);
      } catch (err) {
        console.error("Failed to list extractions", err);
      }
    })();
  }, []);

  return (
    <div style={{ maxHeight: "400px", overflowY: "auto" }}>
      {extractions.map((ext) => (
        <div key={ext.id}>
          <button onClick={() => onSelect(ext.id)}>
            #{ext.id} - {ext.document_type}
          </button>
        </div>
      ))}
    </div>
  );
}
