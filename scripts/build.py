import subprocess

TARGET = "aarch64-unknown-linux-gnu"

def target_missing():
    output = subprocess.run("rustup target list --installed", capture_output=True, shell=True).stdout
    return output.decode("utf-8").find(TARGET) == -1

def install_target():
    subprocess.run(f"rustup target add {TARGET}", shell=True)

def build(project_root: str):
    if target_missing():
        install_target()
    subprocess.run(f"cargo build --target {TARGET} --release", cwd = project_root, check = True, shell=True)
