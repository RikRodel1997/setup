import os
import tempfile
from pathlib import Path
from shared.constants import CHECKMARK, CROSS
from shared.formatting import section_header, section_footer
from shared.commands import apt_install, run_command
from nuc.src.checks import expect_to_be_enabled, expect_to_be_running, is_installed


def setup_samba():
    section_header("Samba")

    if not is_installed("smbd"):
        _install()
    else:
        print(f"    {CHECKMARK} Samba is already installed.")

    print("    Proceeding with configuration...")

    existing_config = run_command("cat /etc/samba/smb.conf").stdout.strip()

    location = _prompt_shared_location()

    username = run_command("whoami").stdout.strip()

    print(f"    Writing new Samba config...")

    config = f"""[global]
    map to guest = Bad User

[media]
    path = {location}
    browseable = yes
    read only = no
    guest ok = yes
    force user = {username}
"""

    if existing_config == config:
        print(f"    {CHECKMARK} Samba configuration is already up to date.")
        section_footer()
        return

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        tf.write(config)
        temp_path = tf.name

    run_command(f"sudo mv {temp_path} /etc/samba/smb.conf")
    run_command("sudo chmod 644 /etc/samba/smb.conf")

    Path(temp_path).unlink(missing_ok=True)

    print(f"    {CHECKMARK} Samba configuration updated successfully.")

    run_command("sudo systemctl restart smbd")

    expect_to_be_enabled("smbd")

    expect_to_be_running("smbd")

    section_footer()


def _prompt_shared_location() -> str:
    print("\n    Enter the folder you want to share via Samba.")
    print("    The folder will be created in ~/ if it doesn't exist.")

    location = input("    If it already exists, it will be used as the shared folder: ")
    if not location:
        return _prompt_shared_location()

    location = os.path.join(os.path.expanduser("~"), location)

    if not os.path.exists(location):
        print(f"    Folder {location} does not exist. Creating it...")
        os.makedirs(location)
        if os.path.exists(location):
            print(f"    {CHECKMARK} Folder {location} created successfully.")
    else:
        print(
            f"    {CHECKMARK} Folder {location} already exists. Using it as the shared folder."
        )

    return location


def _install():
    print("    Samba is not installed. Installing Samba...")

    output = apt_install("samba")

    if output.returncode == 0:
        print(f"    {CHECKMARK} Samba installed successfully!")
    else:
        print(output.stderr)
        print(f"    {CROSS} Failed to install Samba")
