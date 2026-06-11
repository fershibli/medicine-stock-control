from app.controllers.medicine_controller import MedicineController
from app.i18n import t
from app.views.helpers import clear_screen, print_error, read_menu_choice, render_menu
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    if ctx.medicine_id is None:
        print_error("errors.no_medicine_selected")
        return "patient_menu"

    controller = MedicineController(ctx.session)
    medicine = controller.get_active_by_id(ctx.medicine_id)
    if medicine is None:
        print_error("errors.medicine_not_found")
        ctx.medicine_id = None
        return "patient_menu"

    clear_screen()
    print(t("medicine_menu.medicine_label").format(name=medicine.name))
    print()

    options = [
        ("add_stock", "medicine_menu.options.add_stock"),
        ("remove_medicine", "medicine_menu.options.remove_medicine"),
        ("back", "medicine_menu.options.back"),
    ]
    render_menu("medicine_menu.title", options)
    choice = read_menu_choice(len(options))

    route_map = {
        1: "add_stock",
        2: "remove_medicine",
        3: "patient_menu",
    }
    route = route_map[choice]
    if route == "patient_menu":
        ctx.medicine_id = None
    return route
