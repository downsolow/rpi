import subprocess

def run(user: str, host: str, destination: str, binary: str):
    subprocess.run(f"ssh {user}@{host} {destination}/{binary}", shell = True)
