from app.controllers.stock_controller import StockController
from app.views.helpers import (
    clear_screen,
    pause,
    print_error,
    print_message,
    read_optional_date,
    read_positive_decimal,
)
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    if ctx.medicine_id is None:
        print_error("errors.no_medicine_selected")
        return "patient_menu"

    clear_screen()
    print_message("add_stock.title")

    quantity = read_positive_decimal("prompts.enter_quantity", "errors.invalid_quantity")
    if quantity is None:
        return "medicine_menu"

    entry_date, date_error = read_optional_date()
    if date_error:
        print_error(date_error)
        pause()
        return "medicine_menu"

    controller = StockController(ctx.session)
    success, result = controller.add_entry(ctx.medicine_id, quantity, entry_date)
    if success:
        print_message("messages.stock_added")
    else:
        print_error(str(result))

    pause()
    return "medicine_menu"
