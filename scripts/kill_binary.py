import subprocess

def kill_binary(binary: str, user: str, host: str):
    #find processes with the same name
    rpi_binary_process = subprocess.run(f'ssh {user}@{host} "ps -aux | grep {binary}"', capture_output = True, shell = True)

    lines = rpi_binary_process.stdout.decode().splitlines()

    for line in lines:
        #find and kill specific process that ends with: '/{binary}'
        if line.endswith(f"/{binary}"):
            process_id = line.split()[1]
            subprocess.run(f"ssh {user}@{host} kill {process_id}", shell = True)
            print(f"killing: {process_id}")
            break