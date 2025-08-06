import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
binary_name = "app"
binary_path = os.path.join(project_root, "target", "aarch64-unknown-linux-gnu", "release", binary_name)
rpi_user = "erd"
rpi_host = "raspberrypi1.local"
destination = "/home/erd/training/hello_world_diode"
