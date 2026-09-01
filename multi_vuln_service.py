"""
Multi-vulnerability test service.
Contains 4 distinct CWE classes in a single file for multi-finding pipeline testing.
"""
import os
import subprocess
import sqlite3
import pickle


def run_user_command(user_input: str) -> str:
    """CWE-78: OS Command Injection via os.system"""
    output = os.system(f"echo {user_input}")
    return f"exit code: {output}"


def dynamic_code(code: str):
    """CWE-94: Code Injection via eval"""
    return eval(code)


def execute_code(code: str):
    """CWE-94: Code Injection via exec"""
    exec(code)


def fetch_user_data(user_id: str, db_path: str = "app.db") -> dict:
    """CWE-89: SQL Injection via string formatting"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return {"user": result} if result else {}


def load_untrusted_data(data: bytes):
    """CWE-502: Deserialization via pickle.loads"""
    return pickle.loads(data)


def run_subprocess_unsafe(command: str) -> str:
    """CWE-78: Command Injection via subprocess shell=True"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def get_user_profile(raw_profile: str):
    """CWE-94: eval on user input (duplicate pattern for stress testing)"""
    return eval(raw_profile)
