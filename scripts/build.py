import subprocess

def build(project_root: str):
    subprocess.run("cargo build --target aarch64-unknown-linux-gnu --release", cwd = project_root, check = True, shell = True)