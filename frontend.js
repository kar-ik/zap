import { useState } from "react";
import axios from "axios";
import { Button, Input } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function ScannerUI() {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const startScan = async () => {
    if (!target) {
      setMessage("Please enter a target URL.");
      return;
    }
    setLoading(true);
    setMessage("");
    try {
      const response = await axios.post("http://localhost:8000/scan/", { target });
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error starting scan.");
    }
    setLoading(false);
  };

  const downloadReport = () => {
    window.location.href = "http://localhost:8000/download-report/";
  };

  return (
    <div className="flex flex-col items-center gap-6 p-6">
      <Card className="w-full max-w-md">
        <CardContent className="p-6 flex flex-col gap-4">
          <h1 className="text-xl font-bold">Vulnerability Scanner</h1>
          <Input
            type="text"
            placeholder="Enter target URL"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          />
          <Button onClick={startScan} disabled={loading}>
            {loading ? "Scanning..." : "Start Scan"}
          </Button>
          <Button onClick={downloadReport} variant="outline">
            Download Report
          </Button>
          {message && <p className="text-sm text-red-500">{message}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
