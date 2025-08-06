import subprocess
import os
from config import *
from kill_binary import kill_binary
from build import build
from copy_file import create_directory, copy_file, allow_execution
from run import run

build(project_root)

kill_binary(binary_name, rpi_user, rpi_host)

create_directory(rpi_user, rpi_host, destination)

copy_file(project_root, binary_path, rpi_user, rpi_host, destination)

allow_execution(rpi_user, rpi_host, destination, binary_name)

run(rpi_user, rpi_host, destination, binary_name)
