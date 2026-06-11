from app.controllers.medicine_controller import MedicineController
from app.i18n import t
from app.views.helpers import clear_screen, pause, print_error, print_message, read_yes_no
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
    print(t("remove_medicine.title"))
    print(t("remove_medicine.warning"))
    print(t("medicine_menu.medicine_label").format(name=medicine.name))
    print()

    if not read_yes_no():
        print_error("errors.cancelled")
        pause()
        return "medicine_menu"

    success, error = controller.soft_delete(ctx.medicine_id)
    if success:
        print_message("messages.medicine_removed")
        ctx.medicine_id = None
        pause()
        return "patient_menu"

    print_error(str(error))
    pause()
    return "medicine_menu"
