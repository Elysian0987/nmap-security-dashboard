import subprocess
import json 

target = "scanme.nmap.org"

print(f"--- Starting scan on {target} ---")

# '-F' means "Fast scan" (scans the 100 most common ports)
# capture_output=True tells subprocess to save the result instead of just showing it.
# text=True makes the result a clean string instead of raw bytes.
result = subprocess.run(
    ["nmap", "-F", target], capture_output=True, text=True
)

scan_output = result.stdout 

print("--- Scan complete ---")

# print("\n=== Captured Output Stored in a Variable: ===")
# print(scan_output)

# print("\n=== Analysis: Finding Open Ports Only ===")

# Split the big string into a list of individual lines
# for line in scan_output.splitlines():
#     # Check if the current line contains the word "open"
#     if "open" in line:
#         print(line)
        
print("\n=== Analysis: Extracting Structured Data (JSON) ===")

# Create an empty list to store our final, clean data
open_ports = [] 

for line in scan_output.splitlines():
    if "open" in line:
        parts = line.split() # Example: ['21/tcp', 'open', 'ftp']
        
        # We also use .strip() to remove any extra whitespace
        port_info = {
            "port": parts[0].strip(),      # The first piece (e.g., '21/tcp')
            "state": parts[1].strip(),     # The second piece (e.g., 'open')
            "service": parts[2].strip()  # The third piece (e.g., 'ftp')
        }
        
        open_ports.append(port_info)

print(json.dumps(open_ports, indent=2))

output_filename = f"scan_results_{target.replace('.', '_')}.json"
with open(output_filename, 'w') as file:
    json.dump(open_ports, file, indent=2)

print(f"\n--- Results saved to {output_filename} ---")