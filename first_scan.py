import subprocess

# A safe website made by Nmap for people to practice scanning
target = "scanme.nmap.org"

print(f"--- Starting scan on {target} ---")

# '-F' means "Fast scan" (scans the 100 most common ports)
subprocess.run(["nmap", "-F", target])

print("--- Scan complete ---")
