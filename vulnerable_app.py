"""
Deliberately vulnerable application for pipeline testing.
This file contains multiple security issues for L1/L2/L3 to detect and fix.
"""
import os
import subprocess
import pickle
import sqlite3


def run_user_command(user_input):
    """CWE-78: OS Command Injection via shell=True"""
    subprocess.run(user_input, shell=True)


def execute_system_command(command):
    """CWE-78: OS Command Injection via os.system"""
    os.system(command)


def dangerous_eval(user_input):
    """CWE-94: Code Injection via eval"""
    return eval(user_input)


def dangerous_exec(code):
    """CWE-94: Code Injection via exec"""
    exec(code)


def load_unsafe_data(data):
    """CWE-502: Deserialization via pickle"""
    return pickle.loads(data)


def query_user(user_id):
    """CWE-89: SQL Injection via string formatting"""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchall()
