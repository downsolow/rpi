import subprocess
from config import rpi_user, rpi_host


TARGET = "aarch64-unknown-linux-gnu"


def target_missing():
    output = subprocess.run("rustup target list --installed", capture_output=True, text=True, shell=True).stdout
    return output.find(TARGET) == -1


def install_target():
    subprocess.run(f"rustup target add {TARGET}", shell=True)


def build(project_root: str):
    if target_missing():
        install_target()
    subprocess.run(f"cargo build --target {TARGET} --release", cwd = project_root, check = True, shell=True)


def build_remote(destination: str, user: str, host: str):
    cargo_path = f'/home/{user}/.cargo/bin/cargo'
    subprocess.run(f'ssh {user}@{host} {cargo_path} build --release --manifest-path {destination}/Cargo.toml', check=True, text=True, shell=True)


def run_remote(destination: str, user: str, host: str):
    cargo_path = f'/home/{user}/.cargo/bin/cargo'
    subprocess.run(f'ssh {user}@{host} {cargo_path} run --release --manifest-path {destination}/Cargo.toml', check=True, text=True, shell=True)
    