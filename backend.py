from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
import subprocess
import csv
import os
import requests
import time

app = FastAPI()

SCAN_RESULTS = "scan_results.csv"
ZAP_URL = "http://localhost:8080"  # Update if ZAP is running on a different port
API_KEY = ""  # Set OWASP ZAP API key if required

def run_basic_scan(target: str):
    results = []
    
    # Basic security checks (example placeholders)
    results.append({"target": target, "vuln": "Open Ports Scan", "severity": "Medium", "description": "Port scan results here"})
    results.append({"target": target, "vuln": "Security Headers", "severity": "Low", "description": "Missing security headers detected"})
    
    save_results_to_csv(results)
    run_zap_scan(target)

def save_results_to_csv(results):
    file_exists = os.path.isfile(SCAN_RESULTS)
    with open(SCAN_RESULTS, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["target", "vuln", "severity", "description"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)

def run_zap_scan(target: str):
    try:
        start_scan_url = f"{ZAP_URL}/JSON/ascan/action/scan/?url={target}&apikey={API_KEY}"
        response = requests.get(start_scan_url)
        if response.status_code == 200:
            scan_id = response.json().get("scan")
            if scan_id:
                print(f"ZAP scan started for {target} with Scan ID: {scan_id}")
                monitor_zap_scan(scan_id)
        else:
            print(f"Failed to start ZAP scan: {response.text}")
    except Exception as e:
        print(f"Error running ZAP scan: {str(e)}")

def monitor_zap_scan(scan_id: str):
    while True:
        status_url = f"{ZAP_URL}/JSON/ascan/view/status/?scanId={scan_id}&apikey={API_KEY}"
        response = requests.get(status_url)
        if response.status_code == 200:
            status = response.json().get("status")
            print(f"ZAP Scan Status: {status}%")
            if status == "100":
                print("ZAP scan completed.")
                fetch_zap_results(scan_id)
                break
        time.sleep(10)  # Check every 10 seconds

def fetch_zap_results(scan_id: str):
    results_url = f"{ZAP_URL}/JSON/core/view/alerts/?baseurl=&apikey={API_KEY}"
    response = requests.get(results_url)
    if response.status_code == 200:
        alerts = response.json().get("alerts", [])
        results = []
        for alert in alerts:
            results.append({
                "target": alert.get("url", "Unknown"),
                "vuln": alert.get("alert", "Unknown"),
                "severity": alert.get("risk", "Unknown"),
                "description": alert.get("description", "No description available")
            })
        save_results_to_csv(results)
    else:
        print("Failed to fetch ZAP scan results.")

@app.post("/scan/")
def scan_target(target: str, background_tasks: BackgroundTasks):
    if not target:
        raise HTTPException(status_code=400, detail="Target URL is required")
    background_tasks.add_task(run_basic_scan, target)
    return {"message": "Scan started", "target": target}

@app.get("/download-report/")
def download_report():
    if not os.path.exists(SCAN_RESULTS):
        raise HTTPException(status_code=404, detail="No report found")
    with open(SCAN_RESULTS, "rb") as file:
        return Response(content=file.read(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=scan_results.csv"})
