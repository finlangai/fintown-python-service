def text_to_italic(text):
    return "\033[3m" + text + "\033[0m"


def print_italic(message):
    print(text_to_italic(message))


def print_green_bold(message):
    # ANSI escape codes for green and bold text
    GREEN = "\033[92m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"{GREEN}{BOLD}{message}{RESET}")


def print_pink_bold(message):
    # ANSI escape codes for pink and bold text
    PINK = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    # Print the message in pink and bold
    print(f"{PINK}{BOLD}{message}{RESET}")


def text_to_red(text):
    return "\033[91m" + text + "\033[0m"


def text_to_blue(text):
    return "\033[94m" + text + "\033[0m"
