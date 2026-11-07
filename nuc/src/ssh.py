from shared.commands import apt_install, run_command
from shared.constants import CHECKMARK, CROSS
from shared.formatting import section_footer, section_header
from nuc.src.checks import expect_to_be_enabled, expect_to_be_running


def setup_local_ssh():
    section_header("ssh")

    result = run_command(f"dpkg-query -W -f='${{db:Status-Status}}' openssh-server")
    print(f"    {result.stdout.strip()}")
    if result.stdout.strip() != "'installed'":
        print("    Installing openssh-server...")
        apt_install("openssh-server")

    enable_ssh = run_command("sudo systemctl enable --now ssh")
    if not enable_ssh.returncode == 0:
        print(enable_ssh.stderr)
        raise Exception(f"    {CROSS} Failed to enable ssh service")

    allow_ufw = run_command("sudo ufw allow ssh")
    if not allow_ufw.returncode == 0:
        print(allow_ufw.stderr)
        raise Exception(f"    {CROSS} Failed to allow ssh through ufw")
    else:
        print("    ssh is allowed through ufw")

    expect_to_be_enabled("ssh")

    expect_to_be_running("ssh")

    username = run_command("whoami").stdout.strip()
    ip = run_command("hostname -I").stdout.strip().split()[0]

    print(
        f"    ssh is set up. You can connect to this machine using `ssh {username}@{ip}`"
    )

    section_footer()
