import subprocess

from shared.constants import CROSS


def run_command(
    command: str, input: None | str = None
) -> subprocess.CompletedProcess[str]:
    try:
        output = subprocess.run(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=input,
            text=True,
            check=True,
        )

        return output

    except subprocess.CalledProcessError as e:
        print(f"\n--- Command Failed ---")
        print(f"Command: {command}")
        print(f"Exit Code: {e.returncode}")
        if e.stderr:
            print(f"Error Output:\n{e.stderr}")
        if e.stdout:
            print(f"Standard Output:\n{e.stdout}")
        raise


def apt_update():
    return run_command("sudo apt update")


def apt_install(program: str):
    return run_command(f"sudo apt install {program} -y")


def refresh_terminal():
    result = run_command("bash -c 'source ~/.bashrc'")
    if not result.returncode == 0:
        print(result.stderr)
        print(f"{CROSS} Failed to refresh terminal")
