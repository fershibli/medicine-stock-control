from app.controllers.patient_controller import PatientController
from app.views.helpers import clear_screen, pause, print_error, print_message, read_non_empty
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    clear_screen()
    print_message("add_patient.title")

    controller = PatientController(ctx.session)
    name = read_non_empty("prompts.enter_name", "errors.empty_name")
    success, result = controller.create(name)

    if success:
        print_message("messages.patient_added")
    else:
        print_error(str(result))

    pause()
    return "main_menu"
