import subprocess

def copy_file(project_root: str, binary: str, user: str, host: str, destination: str):
    subprocess.run(f"scp {binary} {user}@{host}:{destination} > NUL", cwd = project_root, check = True, shell = True)


def allow_execution(user: str, host: str, binary: str):
    subprocess.run(f"ssh {user}@{host} chmod +x {binary}", shell = True)