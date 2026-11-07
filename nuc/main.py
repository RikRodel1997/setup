import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.commands import apt_update
from nuc.src.home_assistant import setup_home_assistant
from nuc.src.jellyfin import setup_jellyfin
from nuc.src.docker import setup_docker
from nuc.src.checks import check_prerequisite_programs
from nuc.src.samba import setup_samba
from nuc.src.uv import setup_uv
from nuc.src.ssh import setup_local_ssh


def main():
    apt_update()

    check_prerequisite_programs()

    setup_uv()

    setup_samba()

    setup_local_ssh()

    setup_docker()

    setup_jellyfin()

    setup_home_assistant()


main()
