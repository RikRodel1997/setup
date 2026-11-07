from shared.constants import CHECKMARK, CROSS
from shared.commands import run_command, refresh_terminal
from nuc.src.checks import is_installed
from shared.formatting import section_header, section_footer


def setup_uv():
    _install()


def _install():
    section_header("uv")

    if not is_installed("uv"):
        print("    uv is not installed. Installing uv...")

        run_command("curl -LsSf https://astral.sh/uv/install.sh -o install_uv.sh")

        install_uv = run_command("sh install_uv.sh")

        if install_uv.returncode == 0:
            print(f"    {CHECKMARK} uv installed successfully!")
        else:
            print(install_uv.stderr)
            print(f"    {CROSS} Failed to install uv")

        refresh_terminal()

    else:
        print(f"    {CHECKMARK} uv is already installed.")

    section_footer()
