import tempfile
from pathlib import Path
from shared.commands import apt_update, run_command, apt_install
from shared.constants import CHECKMARK, CROSS
from shared.formatting import section_footer, section_header
from nuc.src.checks import expect_to_be_enabled, expect_to_be_running, is_installed


def setup_docker():
    section_header("Docker")

    print("    Installing ca-certificates")
    apt_install("ca-certificates")

    _setup_keyring()

    _setup_repository()

    if not is_installed("docker"):
        _install()
    else:
        print(f"    {CHECKMARK} Docker is already installed.")

    expect_to_be_enabled("docker")

    expect_to_be_running("docker")

    section_footer()


def _install():
    print("    Installing Docker components...")

    components = [
        "docker-ce",
        "docker-ce-cli",
        "containerd.io",
        "docker-buildx-plugin",
        "docker-compose-plugin",
    ]

    for component in components:
        print(f"        Installing {component}...")
        apt_install(component)

    print(f"    {CHECKMARK} Docker installed successfully.")


def _setup_keyring():
    run_command("sudo install -m 0755 -d /etc/apt/keyrings")
    run_command(
        "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc"
    )
    run_command("sudo chmod a+r /etc/apt/keyrings/docker.asc")
    print(f"    {CHECKMARK} Docker GPG key installed successfully.")


def _setup_repository():
    os_release = {}
    with open("/etc/os-release") as f:
        for line in f:
            if "=" in line:
                k, v = line.rstrip().split("=", 1)
                os_release[k] = v.strip('"').strip()

    codename = os_release.get("UBUNTU_CODENAME") or os_release.get("VERSION_CODENAME")
    architecture = run_command("dpkg --print-architecture").stdout.strip()

    config = f"""Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: {codename}
Components: stable
Architectures: {architecture}
Signed-By: /etc/apt/keyrings/docker.asc
"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        tf.write(config)
        temp_path = tf.name

    run_command(f"sudo mv {temp_path} /etc/apt/sources.list.d/docker.sources")
    run_command(f"sudo chmod 644 /etc/apt/sources.list.d/docker.sources")

    apt_update()

    print(f"    {CHECKMARK} Docker repository added successfully.")

    Path(temp_path).unlink(missing_ok=True)
