from app.controllers.patient_controller import PatientController
from app.controllers.stock_controller import StockController
from app.i18n import t
from app.views.helpers import clear_screen, pause, print_error
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    if ctx.patient_id is None:
        print_error("errors.no_patient_selected")
        return "main_menu"

    patient_controller = PatientController(ctx.session)
    patient = patient_controller.get_by_id(ctx.patient_id)
    if patient is None:
        print_error("errors.patient_not_found")
        ctx.patient_id = None
        return "main_menu"

    clear_screen()
    print(t("list_stock.title"))
    print("-" * len(t("list_stock.title")))
    print(t("patient_menu.patient_label").format(name=patient.name))
    print()

    stock_controller = StockController(ctx.session)
    items = stock_controller.list_current_stock(ctx.patient_id)

    if not items:
        print(t("list_stock.empty"))
    else:
        for item in items:
            print(
                t("list_stock.row").format(
                    name=item["name"],
                    stock=item["current_stock"],
                    unit=item["unit"],
                    dose=item["daily_dose"],
                )
            )

    pause()
    return "patient_menu"
