from app.controllers.patient_controller import PatientController
from app.i18n import t
from app.views.helpers import clear_screen, pause, print_error, print_message, read_yes_no
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
    print(t("remove_patient.title"))
    print(t("remove_patient.warning"))
    print(t("patient_menu.patient_label").format(name=patient.name))
    print()

    if not read_yes_no():
        print_error("errors.cancelled")
        pause()
        return "patient_menu"

    success, error = controller.delete(ctx.patient_id)
    if success:
        print_message("messages.patient_removed")
        ctx.patient_id = None
        ctx.medicine_id = None
        pause()
        return "main_menu"

    print_error(str(error))
    pause()
    return "patient_menu"
