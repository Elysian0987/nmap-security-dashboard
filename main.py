from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import subprocess
import json
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# --- Configuration for Safety Nets ---
# 1. Blocklist of sensitive domains
BLOCKLIST = {
    "gov.in", "nic.in", "fbi.gov", "cia.gov", "gov.uk", "mil",
    # Add other sensitive domains or top-level domains (TLDs)
}

# 2. Rate Limiting settings
# Dictionary to track requests: { "ip_address": [timestamp1, timestamp2, ...], }
request_tracker = {}
RATE_LIMIT_COUNT = 5      # Max 5 requests...
RATE_LIMIT_WINDOW = 3600  # ...per hour (3600 seconds)

# --- API Endpoint ---
# This creates a URL at /scan/{some_target_url}
@app.get("/scan/{target_url}")
def scan_target(target_url: str, request: Request):
    """
    Runs an Nmap scan on the target URL, with safety checks, and returns a list of open ports.
    """
    client_ip = request.client.host
    current_time = time.time()

    # --- Safety Net 1: Rate Limiting Logic ---
    if client_ip not in request_tracker:
        request_tracker[client_ip] = []

    # Remove old timestamps that are outside our time window
    request_tracker[client_ip] = [
        ts for ts in request_tracker[client_ip] if current_time - ts < RATE_LIMIT_WINDOW
    ]

    # Check if the user has exceeded the limit
    if len(request_tracker[client_ip]) >= RATE_LIMIT_COUNT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    # Record the new valid request
    request_tracker[client_ip].append(current_time)

    # --- Safety Net 2: Blocklist Logic ---
    for blocked_domain in BLOCKLIST:
        if blocked_domain in target_url:
            raise HTTPException(status_code=403, detail="Scanning this target is forbidden.")

    # --- Original Scanning Logic ---
    print(f"--- ({client_ip}) Received scan request for {target_url} ---")
    
    try:
        result = subprocess.run(
            ["nmap", "-F", target_url], 
            capture_output=True, 
            text=True,
            check=True  # This will raise an error if nmap fails
        )
        scan_output = result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # Handle cases where nmap fails or isn't found
        raise HTTPException(status_code=500, detail=f"Nmap scan failed: {e}")

    print(f"--- ({client_ip}) Scan complete, parsing results for {target_url} ---")
    
    open_ports = []
    for line in scan_output.splitlines():
        if "open" in line and "/" in line:
            parts = line.split()
            port_info = {
                "port": parts[0].strip(),
                "state": parts[1].strip(),
                "service": parts[2].strip()
            }
            open_ports.append(port_info)
            
    # The API endpoint returns the final list. FastAPI automatically converts it to JSON.
    return open_ports

#uvicorn main:app --reload
