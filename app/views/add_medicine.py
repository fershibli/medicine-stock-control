from app.controllers.medicine_controller import MedicineController
from app.views.helpers import (
    clear_screen,
    pause,
    print_error,
    print_message,
    read_non_empty,
    read_positive_decimal,
)
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    if ctx.patient_id is None:
        print_error("errors.no_patient_selected")
        return "main_menu"

    clear_screen()
    print_message("add_medicine.title")

    controller = MedicineController(ctx.session)
    name = read_non_empty("prompts.enter_name", "errors.empty_name")
    daily_dose = read_positive_decimal("prompts.enter_daily_dose", "errors.invalid_dose")
    if daily_dose is None:
        return "patient_menu"
    unit = read_non_empty("prompts.enter_unit", "errors.empty_unit")

    success, result = controller.create(ctx.patient_id, name, daily_dose, unit)
    if success:
        print_message("messages.medicine_added")
    else:
        print_error(str(result))

    pause()
    return "patient_menu"
