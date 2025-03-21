import { useState } from "react";
import axios from "axios";

export default function ScannerDashboard() {
  const [target, setTarget] = useState("");
  const [scanning, setScanning] = useState(false);
  const [message, setMessage] = useState("");

  const startScan = async () => {
    if (!target) {
      setMessage("Please enter a target URL.");
      return;
    }
    setScanning(true);
    setMessage("Scanning started...");
    try {
      const response = await axios.post("/scan/", { target });
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error starting scan.");
    }
    setScanning(false);
  };

  const downloadReport = async () => {
    try {
      const response = await axios.get("/download-report/", {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "scan_results.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setMessage("Error downloading report.");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-xl font-bold">Vulnerability Scanner</h2>
      <input
        type="text"
        className="border p-2 w-full rounded"
        placeholder="Enter target URL"
        value={target}
        onChange={(e) => setTarget(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded w-full"
        onClick={startScan}
        disabled={scanning}
      >
        {scanning ? "Scanning..." : "Start Scan"}
      </button>
      <button
        className="bg-green-500 text-white px-4 py-2 rounded w-full"
        onClick={downloadReport}
      >
        Download Report
      </button>
      {message && <p className="text-red-500">{message}</p>}
    </div>
  );
}
