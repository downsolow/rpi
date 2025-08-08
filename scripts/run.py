#!/usr/bin/env python3
import subprocess


def run(user: str, host: str, destination: str, binary: str):
    subprocess.run(f"ssh {user}@{host} {destination}/{binary}", shell = True)


if __name__ == "__main__":
    from config import rpi_user, rpi_host, destination, binary_name

    run(rpi_user, rpi_host, destination, binary_name)
