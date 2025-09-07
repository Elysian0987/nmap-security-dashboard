# Nmap Security Dashboard 

## ⚠️ Disclaimer
**This tool is intended for educational purposes and authorized security testing only. Use at your own risk.**

By using this software, you agree that the author and any contributors are not liable for any misuse or damage caused. You are solely responsible for your actions and for complying with all applicable laws. The software is provided "as is," without warranty of any kind.

---

A web-based dashboard built with Python and FastAPI to run live Nmap port scans and visualize the results in real-time.

---

## Key Features
* **Live Port Scanning:** Leverages the power of Nmap, executed via a Python backend, to scan targets for open ports.
* **REST API Backend:** A robust backend built with **FastAPI** serves scan results as clean, structured JSON data.
* **Automated Data Parsing:** Intelligently parses the raw output from Nmap into a machine-readable format for easy consumption.
* **Dynamic Frontend:** A responsive user interface built with vanilla JavaScript that consumes the API and displays results in a clean table without a page reload.

---

## Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **Security Tool:** Nmap
* **Frontend:** HTML, CSS, JavaScript

---

## Getting Started
Follow these instructions to get a local copy up and running.

### Prerequisites
You must have the following installed on your system:
* [Python 3.8+](https://www.python.org/downloads/)
* [Nmap](https://nmap.org/download.html) (Ensure it is added to your system's PATH)

### Installation & Running
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Elysian0987/nmap-security-dashboard.git
    cd nmap-security-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install fastapi uvicorn
    ```

4.  **Start the backend API server:**
    ```bash
    uvicorn main:app --reload
    ```
    The server will be running at `http://127.0.0.1:8000`.

5.  **Open the application:**
    Open the `index.html` file in your web browser to use the app.

---

## API Endpoint
The API has one main endpoint for initiating scans.

### `GET /scan/{target_url}`
- **Action:** Runs a fast Nmap scan (`-F`) on the specified target
- **Returns:** JSON array of open ports  
- **Example:** `/scan/scanme.nmap.org`

---

## License
This project is licensed under the MIT License.
