from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import subprocess
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define an API endpoint
# This creates a URL at /scan/{some_target_url}
@app.get("/scan/{target_url}")
def scan_target(target_url: str):
    """
    Runs an Nmap scan on the target URL and returns a list of open ports.
    """
    print(f"--- Received scan request for {target_url} ---")
    
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
        return {"error": f"Nmap scan failed: {e}"}

    print("--- Scan complete, parsing results ---")
    
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