import subprocess


def run_command(cmd: str) -> (str, int):
    command_handle = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    command_handle.wait()
    command_handle.stdout.flush()
    return command_handle.stdout.read().decode(), command_handle.poll()
