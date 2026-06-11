from app.controllers.patient_controller import PatientController
from app.i18n import t
from app.views.helpers import clear_screen, print_error, read_menu_choice, render_menu
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    if ctx.patient_id is None:
        print_error("errors.no_patient_selected")
        return "main_menu"

    controller = PatientController(ctx.session)
    patient = controller.get_by_id(ctx.patient_id)
    if patient is None:
        print_error("errors.patient_not_found")
        ctx.patient_id = None
        return "main_menu"

    clear_screen()
    print(t("patient_menu.patient_label").format(name=patient.name))
    print()

    options = [
        ("list_stock", "patient_menu.options.list_stock"),
        ("add_medicine", "patient_menu.options.add_medicine"),
        ("select_medicine", "patient_menu.options.select_medicine"),
        ("remove_patient", "patient_menu.options.remove_patient"),
        ("back", "patient_menu.options.back"),
    ]
    render_menu("patient_menu.title", options)
    choice = read_menu_choice(len(options))

    route_map = {
        1: "list_stock",
        2: "add_medicine",
        3: "select_medicine",
        4: "remove_patient",
        5: "main_menu",
    }
    route = route_map[choice]
    if route == "main_menu":
        ctx.patient_id = None
        ctx.medicine_id = None
    return route
