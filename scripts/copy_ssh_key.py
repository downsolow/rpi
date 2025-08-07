import subprocess
import os
from config import *

rpi_user = f"{rpi_user}@{rpi_host}"
check_ssh_already_copied_command = f"ssh -o BatchMode=yes {rpi_user} true"
ssh_check_result = subprocess.run(check_ssh_already_copied_command)

if ssh_check_result.returncode == 0:
    print("ssh already copied")
else:
    user_profile = subprocess.run(["powershell", "-Command", "echo $env:USERPROFILE"], capture_output = True, text = True).stdout.strip()
    ssh_public_key_path = os.path.join(user_profile, ".ssh", "id_ed25519.pub")

    if not os.path.exists(ssh_public_key_path):
        print("Generating new ssh key..")
        subprocess.run("ssh-keygen")

    print("Copying ssh key to RPi..")
    ssh_copy_command =  f'type {ssh_public_key_path} | ssh {rpi_user} "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"'
    subprocess.run(["powershell", "-Command", ssh_copy_command])