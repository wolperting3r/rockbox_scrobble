import os
# Method 1: Using os.uname() (works on Unix-like systems)
hostname = os.uname().nodename
print(f"Hostname: {hostname}")
