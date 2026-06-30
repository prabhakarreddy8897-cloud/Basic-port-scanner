# ----------------------------------------
# Basic Port Scanner
# Author: E.Prabhakar Reddy
# ----------------------------------------

import socket

# Ask the user for a target
target = input("Enter IP address or website: ")

# Convert website name to IP address
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid Host")
    exit()

print("\nScanning:", target)
print("IP Address:", target_ip)
print("-" * 30)

# Scan ports from 1 to 100
for port in range(1, 101):

    # Create a socket
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set timeout to 1 second
    scanner.settimeout(1)

    # Try connecting to the port
    result = scanner.connect_ex((target_ip, port))

    # If result is 0, the port is open
    if result == 0:
        print(f"Port {port} is OPEN")

    # Close the socket
    scanner.close()

print("\nScan Completed!")
