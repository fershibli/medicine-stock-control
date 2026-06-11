from app.views.helpers import clear_screen, read_menu_choice, render_menu
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    clear_screen()
    options = [
        ("select_patient", "main_menu.options.select_patient"),
        ("add_patient", "main_menu.options.add_patient"),
        ("change_language", "main_menu.options.change_language"),
        ("exit", "main_menu.options.exit"),
    ]
    render_menu("main_menu.title", options)
    choice = read_menu_choice(len(options))

    route_map = {
        1: "select_patient",
        2: "add_patient",
        3: "change_language",
        4: None,
    }
    return route_map[choice]
