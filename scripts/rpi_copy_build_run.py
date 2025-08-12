#!/usr/bin/env python3
from build import run_remote
from kill_binary import kill_binary
from copy_file import create_directory, copy_directory_recursive, copy_file
import subprocess


def copy_build_run(user: str, host: str, destination: str):
    from config import get_project_root, get_binary_name

    if not is_ssh_connectable(user, host):
        print("unable to establish ssh keyless connection")
        return
    
    create_directory(user, host, destination)
    project_root = get_project_root()

    source = f"{project_root}/src"
    copy_directory_recursive(source, user, host, destination)

    cargo = f"{project_root}/.cargo"
    copy_directory_recursive(source, user, host, destination)

    binary_name = get_binary_name()
    kill_binary(binary_name, user, host)

    cargo_toml = f"{project_root}/Cargo.toml"
    copy_file(project_root, cargo_toml, user, host, destination)

    run_remote(destination, user, host)


if __name__ == "__main__":
    from config import *
    copy_build_run(rpi_user, rpi_host, destination)