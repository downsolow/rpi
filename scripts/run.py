import subprocess

def run(user: str, host: str, binary: str):
    subprocess.run(f"ssh {user}@{host} ./{binary}", shell = True)