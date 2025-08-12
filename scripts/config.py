#!/usr/bin/env python3
import os
import subprocess
import socket


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_binary_name():
    cargo_toml = f"{project_root}/Cargo.toml"
    with open(cargo_toml) as file:
        for line in file.readlines():
            if line.startswith("name = "):
                return line.split(" = ")[-1]


def is_host_available(host):
    try:
        socket.gethostbyname(host)
        return True

    except Exception:
        return False


def is_ssh_connectable(user: str, host: str, timeout=5):
    user_host = f"{user}@{host}"
    if is_host_available(host):
        try:
            result = subprocess.run(
                f"ssh -o connectTimeout={timeout} {user_host} exit", 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                timeout=timeout, 
                shell=True
            )
            return result.returncode == 0
        
        except Exception:
            return False

    return False


def get_host(host: str):
    if is_host_available(host):
        return host
    else:
        default_static_ip = "192.168.1.100"
        print(f"host {host} not available, using static ip: {default_static_ip}")
        return default_static_ip


project_root = get_project_root()
binary_name = get_binary_name()
binary_path = os.path.join(project_root, "target", "aarch64-unknown-linux-gnu", "release", binary_name)
rpi_user = "erd"
rpi_dns_host = "raspberrypi.local"
rpi_host = get_host(rpi_dns_host)
destination = "/home/erd/training/hello_world_diode"
