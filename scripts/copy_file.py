import subprocess
import platform


def copy_directory_recursive(directory: str, user: str, host: str, destination):
    trash = "$NULL" if platform.system() == "Windows" else "/dev/null"
    subprocess.run(f"scp -r {directory} {user}@{host}:{destination} > {trash}", check = True, shell = True)


def copy_file(project_root: str, binary: str, user: str, host: str, destination: str):
    trash: str
    if platform.system() == "Windows":
        trash = "$NULL"
    else:
        trash = "/dev/null"
    subprocess.run(f"scp {binary} {user}@{host}:{destination} > {trash}", cwd = project_root, check = True, shell = True)


def create_directory(user: str, host: str, destination: str):
    subprocess.run(f"ssh {user}@{host} mkdir -p {destination}", shell = True)


def allow_execution(user: str, host: str, destination: str, binary: str):
    subprocess.run(f"ssh {user}@{host} chmod +x {destination}/{binary}", shell = True)
