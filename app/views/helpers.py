from datetime import date, datetime

from app.i18n import t


def clear_screen() -> None:
    print("\n" * 2)


def pause() -> None:
    input(t("prompts.press_enter"))


def print_error(error_key: str) -> None:
    print(t(error_key))


def print_message(message_key: str, **kwargs) -> None:
    print(t(message_key).format(**kwargs) if kwargs else t(message_key))


def read_line(prompt_key: str) -> str:
    return input(t(prompt_key)).strip()


def read_positive_decimal(prompt_key: str, error_key: str) -> str | None:
    while True:
        value = read_line(prompt_key)
        try:
            from decimal import Decimal

            decimal_value = Decimal(value)
            if decimal_value <= 0:
                print_error(error_key)
                continue
            return value
        except Exception:
            print_error(error_key)


def read_non_empty(prompt_key: str, error_key: str) -> str:
    while True:
        value = read_line(prompt_key)
        if value:
            return value
        print_error(error_key)


def read_yes_no() -> bool:
    while True:
        answer = read_line("prompts.confirm_yes_no").lower()
        if answer in ("y", "yes", "s", "sim"):
            return True
        if answer in ("n", "no", "nao", "não"):
            return False
        print_error("errors.invalid_input")


def read_optional_date() -> tuple[date | None, str | None]:
    value = read_line("prompts.enter_date")
    if not value:
        return date.today(), None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date(), None
    except ValueError:
        return None, "errors.invalid_date"


def render_menu(title_key: str, options: list[tuple[str, str]]) -> None:
    print(t(title_key))
    print("-" * len(t(title_key)))
    for index, (_, label_key) in enumerate(options, start=1):
        print(f"{index}. {t(label_key)}")
    print()


def read_menu_choice(option_count: int) -> int | None:
    while True:
        choice = read_line("prompts.select_option")
        if not choice.isdigit():
            print_error("errors.invalid_option")
            continue
        index = int(choice)
        if 1 <= index <= option_count:
            return index
        print_error("errors.invalid_option")
