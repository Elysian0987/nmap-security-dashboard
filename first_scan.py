import subprocess
import json # Import the json library to help us print nicely

target = "scanme.nmap.org"

print(f"--- Starting scan on {target} ---")

# '-F' means "Fast scan" (scans the 100 most common ports)
# capture_output=True tells subprocess to save the result instead of just showing it.
# text=True makes the result a clean string instead of raw bytes.
result = subprocess.run(
    ["nmap", "-F", target], capture_output=True, text=True
)

# The output from the command is now stored in result.stdout
scan_output = result.stdout 

print("--- Scan complete ---")

# Let's prove we have it by printing the variable
# print("\n=== Captured Output Stored in a Variable: ===")
# print(scan_output)

# Analyze the captured output
# print("\n=== Analysis: Finding Open Ports Only ===")

# Split the big string into a list of individual lines
# for line in scan_output.splitlines():
#     # Check if the current line contains the word "open"
#     if "open" in line:
#         # If it does, print just that line!
#         print(line)
        
print("\n=== Analysis: Extracting Structured Data (JSON) ===")

# Create an empty list to store our final, clean data
open_ports = [] 

for line in scan_output.splitlines():
    if "open" in line:
        # This is an open port line, let's break it into pieces
        parts = line.split() # Example: ['21/tcp', 'open', 'ftp']
        
        # Now, structure this data cleanly in a dictionary
        # We also use .strip() to remove any extra whitespace
        port_info = {
            "port": parts[0].strip(),      # The first piece (e.g., '21/tcp')
            "state": parts[1].strip(),     # The second piece (e.g., 'open')
            "service": parts[2].strip()  # The third piece (e.g., 'ftp')
        }
        
        # Add our newly created dictionary to our list of open ports
        open_ports.append(port_info)

# Now, let's print our final list of dictionaries in a clean, readable format
# json.dumps is a great way to "pretty-print" data structures
print(json.dumps(open_ports, indent=2))

# Save the JSON output to a file
output_filename = f"scan_results_{target.replace('.', '_')}.json"
with open(output_filename, 'w') as file:
    json.dump(open_ports, file, indent=2)

print(f"\n--- Results saved to {output_filename} ---")