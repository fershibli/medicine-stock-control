from app.controllers.patient_controller import PatientController
from app.i18n import t
from app.views.helpers import clear_screen, print_error, read_menu_choice
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    clear_screen()
    print(t("select_patient.title"))
    print("-" * len(t("select_patient.title")))

    controller = PatientController(ctx.session)
    patients = controller.list_all()

    if not patients:
        print(t("select_patient.empty"))
        input(t("prompts.press_enter"))
        return "main_menu"

    for index, patient in enumerate(patients, start=1):
        print(t("select_patient.option_label").format(index=index, name=patient.name))

    back_index = len(patients) + 1
    print(f"{back_index}. {t('patient_menu.options.back')}")
    print()

    choice = read_menu_choice(back_index)
    if choice == back_index:
        return "main_menu"

    ctx.patient_id = patients[choice - 1].id
    ctx.medicine_id = None
    return "patient_menu"
