import shutil
from shared.commands import run_command
from shared.formatting import section_header, section_footer
from shared.constants import CHECKMARK, CROSS


def check_prerequisite_programs():
    section_header("Prerequisite Programs")

    programs = ["git", "python3", "curl"]

    for program in programs:
        if is_installed(program):
            print(f"    {CHECKMARK} Prerequisite {program} is installed!")
        else:
            print(f"    {CROSS} Prerequisite {program} is not installed!")

    section_footer()


def is_installed(program: str) -> bool:
    which = shutil.which(program) is not None
    if which:
        return True

    return False


def expect_to_be_enabled(service: str) -> bool:
    enabled = run_command(f"systemctl is-enabled {service}")

    if not enabled.returncode == 0:
        print(enabled.stderr)
        raise Exception(f"    {CROSS} Failed to check if {service} is enabled")
    else:
        print(f"    {CHECKMARK} {service} is enabled.")


def expect_to_be_running(service: str) -> bool:
    active = run_command(f"systemctl is-active {service}")

    if not active.returncode == 0:
        print(active.stderr)
        raise Exception(f"    {CROSS} Failed to check if {service} is running")
    else:
        print(f"    {CHECKMARK} {service} is running.")
