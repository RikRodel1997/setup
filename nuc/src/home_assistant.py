from shared.commands import apt_install, run_command
from shared.constants import CHECKMARK, CROSS
from shared.formatting import section_footer, section_header
from nuc.src.checks import expect_to_be_enabled, expect_to_be_running


def setup_home_assistant():
    section_header("Home Assistant")

    section_footer()
