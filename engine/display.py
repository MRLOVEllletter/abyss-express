import time
import sys

SLOW_TYPING = True
SLOW_SPEED = 0.015


def set_slow(enable):
    global SLOW_TYPING
    SLOW_TYPING = enable


def slow_print(text, end="\n"):
    if SLOW_TYPING:
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(SLOW_SPEED)
        sys.stdout.write(end)
        sys.stdout.flush()
    else:
        print(text, end=end)


def print_line(char="━", length=50):
    print(char * length)


def print_header(title, subtitle=""):
    print("╔" + "═" * 48 + "╗")
    title_line = f"║{title:^48}║"
    print(title_line)
    if subtitle:
        sub_line = f"║{subtitle:^48}║"
        print(sub_line)
    print("╚" + "═" * 48 + "╝")


def print_menu(title, options):
    print()
    print(f"  【{title}】")
    print()
    for key, desc in options:
        print(f"    {key}. {desc}")
    print()


def print_event_menu(options):
    for i, (text, _) in enumerate(options, 1):
        print(f"    {i}. {text}")
    print()


def get_event_choice(options):
    valid = [str(i) for i in range(1, len(options) + 1)]
    while True:
        choice = input("  请选择：").strip()
        if choice in valid:
            idx = int(choice) - 1
            return options[idx][1]
        print(f"  无效输入，请输入 1-{len(options)}")


def get_choice(prompt="请选择：", valid=None):
    while True:
        choice = input(prompt).strip()
        if valid is None or choice in valid:
            return choice
        print(f"无效输入，请输入 {', '.join(valid)}")


def wait_enter():
    input("\n 按 Enter 继续...")


def typewriter(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()