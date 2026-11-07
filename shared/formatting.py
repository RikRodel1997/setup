TOTAL_HEADER_SIZE = 54
SPACE_PADDING = 2


def section_header(title: str) -> str:
    title_length = len(title) + SPACE_PADDING
    remaining_length = TOTAL_HEADER_SIZE - title_length
    side_length = remaining_length // 2

    if remaining_length % 2 != 0:
        print(f"\n{_dashes(side_length)} {title} {_dashes(side_length + 1)}\n")
    else:
        print(f"\n{_dashes(side_length)} {title} {_dashes(side_length)}\n")


def section_footer() -> str:
    print(f"\n{'-' * TOTAL_HEADER_SIZE}")


def _dashes(length: int) -> str:
    return "-" * length
