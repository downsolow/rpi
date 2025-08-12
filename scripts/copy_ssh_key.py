#!/usr/bin/env python3

import subprocess
import os
from config import *
import platform


def copy_ssh_key():
    user = f"{rpi_user}@{rpi_host}"
    check_ssh_already_copied_command = f"ssh -o BatchMode=yes {user} true"
    ssh_check_result = subprocess.run(check_ssh_already_copied_command, shell = True)

    if ssh_check_result.returncode == 0:
        print("ssh already copied")
        return

    user_profile = (subprocess.run(
        ["powershell", "-Command", "echo $env:USERPROFILE"], 
        shell = True, 
        capture_output = True, 
        text = True
    ).stdout.strip()) if platform.system == "Windows" else os.path.expanduser("~")
    ssh_public_key_path = os.path.join(user_profile, ".ssh", "id_ed25519.pub")

    if not os.path.exists(ssh_public_key_path):
        print(f"ssh key path: {ssh_public_key_path} not found")
        print("Generating new ssh key..")
        subprocess.run("ssh-keygen")

    print("Copying ssh key to RPi..")
    ssh_copy_command =  f'ssh {user} "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys" < {ssh_public_key_path}'
    subprocess.run(ssh_copy_command, shell=True)


if __name__ == "__main__":
    copy_ssh_key()
