from app.controllers.medicine_controller import MedicineController
from app.i18n import t
from app.views.helpers import clear_screen, print_error, read_menu_choice
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    if ctx.patient_id is None:
        print_error("errors.no_patient_selected")
        return "main_menu"

    clear_screen()
    print(t("select_medicine.title"))
    print("-" * len(t("select_medicine.title")))

    controller = MedicineController(ctx.session)
    medicines = controller.list_active_by_patient(ctx.patient_id)

    if not medicines:
        print(t("select_medicine.empty"))
        input(t("prompts.press_enter"))
        return "patient_menu"

    for index, medicine in enumerate(medicines, start=1):
        print(
            t("select_medicine.option_label").format(
                index=index,
                name=medicine.name,
                dose=medicine.daily_dose,
                unit=medicine.unit,
            )
        )

    back_index = len(medicines) + 1
    print(f"{back_index}. {t('medicine_menu.options.back')}")
    print()

    choice = read_menu_choice(back_index)
    if choice == back_index:
        return "patient_menu"

    ctx.medicine_id = medicines[choice - 1].id
    return "medicine_menu"
