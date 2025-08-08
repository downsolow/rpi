#!/usr/bin/env python3

import zipfile
import os
import sys
import tarfile
import platform
from pathlib import Path
import subprocess

def download_file(url, destination):
    print(f"Downloading {url} to {destination}")
    try:
        subprocess.run(f"curl -L -o {destination} {url}", check=True, shell=True)
        print("Download completed successfully!")
    except Exception as e:
        print("Error downloading file: {e}")
        sys.exit(1)

def extract_tarxz(archive_path, extract_path):
    print(f"Extracting {archive_path} to {extract_path}")
    try:
        with tarfile.open(archive_path, "r:xz") as tar:
            tar.extractall(path=extract_path, filter='data')
        print("Extraction completed successfully!")
    except Exception as e:
        print(f"Error extracting archive: {e}")
        sys.exit(1)

def extract_zip(archive_path, extract_path):
    print(f"Extracting {archive_path} to {extract_path}")
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip:
            zip.extractall(path=extract_path)
    except Exception as e:
        print(f"Error extracting archive: {e}")
        sys.exit(1)

def remove_archive(download_path):
    print(f"Removing {download_path} archive")
    try:
        Path.unlink(download_path)
    except FileNotFoundError as e:
        print(f"Error removing archive: {e}")

def get_toolchain_url():
    if platform.system() == "Windows":
        return "https://developer.arm.com/-/media/Files/downloads/gnu/14.3.rel1/binrel/arm-gnu-toolchain-14.3.rel1-mingw-w64-x86_64-aarch64-none-linux-gnu.zip"
    else:
        return "https://developer.arm.com/-/media/Files/downloads/gnu/14.3.rel1/binrel/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-linux-gnu.tar.xz"

def create_build_dir():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    build_dir = os.path.join(project_root, "build")
    os.makedirs(build_dir, exist_ok=True)
    return build_dir

def verify_installation(bin_dir):
    if not os.path.exists(bin_dir):
        print(f"Error: Expected bin directory not found at {bin_dir}")
        sys.exit(1)

    try:
        compiler_path = os.path.join(bin_dir, "aarch64-none-linux-gnu-gcc")
        if platform.system() == 'Windows':
            compiler_path += ".exe"
        if os.path.exists(compiler_path):
            result = subprocess.run([compiler_path, "--version"], capture_output=True, text=True)
            print("\nVerification successful. Toolchain information:")
            print(result.stdout.split("\n")[0])
        else:
            print("\nWarning: Compiler executable not found at expected location")
    except Exception as e:
            print(f"\nWarning: Could not verify installation: {e}")

def extract_toolchain(download_path, build_dir):
    (_, ext) = os.path.splitext(download_path)
    if ext == ".zip":
        build_dir = os.path.join(build_dir, "arm-gnu-toolchain-aarch64-none-linux-gnu")
        os.mkdir(build_dir)
        extract_zip(download_path, build_dir)
    else:
        extract_tarxz(download_path, build_dir)
        os.rename(download_path.replace(".tar.xz", ""), get_toolchain_path(build_dir))

def download_toolchain(url, download_path, toolchain_path):
    if not os.path.exists(toolchain_path):
        download_file(url, download_path)
    else:
        print(f"Directory {download_path} already exists, skipping download")
        bin_dir = os.path.join(toolchain_path, "bin")
        verify_installation(bin_dir)
        sys.exit(0)

def get_toolchain_path(build_dir):
    return os.path.join(build_dir, "arm-gnu-toolchain-aarch64-none-linux-gnu")

def main():
    url = get_toolchain_url()
    filename = url.split("/")[-1]
    build_dir = create_build_dir()
    toolchain_path = get_toolchain_path(build_dir)
    download_path = os.path.join(build_dir, filename)
    
    download_toolchain(url, download_path, toolchain_path)
    extract_toolchain(download_path, build_dir)
    remove_archive(download_path)
    
    bin_dir = os.path.join(toolchain_path, "bin")   
    verify_installation(bin_dir)

if __name__ == "__main__":
    main()
