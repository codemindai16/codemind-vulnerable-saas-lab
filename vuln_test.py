import os
import subprocess

# Intentionally vulnerable test file for webhook smoke test
user_input = input("Enter command: ")
os.system(user_input)  # CWE-78: OS Command Injection

password = "admin123"  # CWE-798: Hardcoded credentials
