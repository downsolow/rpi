import os
import subprocess

def  check_ssh_connection(host, timeout=5):
    try:
        result = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes", host, "exit"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False



project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
binary_name = "app"
binary_path = os.path.join(project_root, "target", "aarch64-unknown-linux-gnu", "release", binary_name)
rpi_user = "erd"
rpi_dns_host = "raspberrypi1.local"
rpi_host = rpi_dns_host if check_ssh_connection(rpi_dns_host) else "192.168.1.100"
destination = "/home/erd/training/hello_world_diode"
