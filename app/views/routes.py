from app.views import (
    add_medicine,
    add_patient,
    add_stock,
    change_language,
    list_stock,
    main_menu,
    medicine_menu,
    patient_menu,
    remove_medicine,
    remove_patient,
    select_medicine,
    select_patient,
)
from app.views.router import RouteHandler

ROUTES: dict[str, RouteHandler] = {
    "main_menu": main_menu.handle,
    "select_patient": select_patient.handle,
    "add_patient": add_patient.handle,
    "change_language": change_language.handle,
    "patient_menu": patient_menu.handle,
    "list_stock": list_stock.handle,
    "add_medicine": add_medicine.handle,
    "select_medicine": select_medicine.handle,
    "remove_patient": remove_patient.handle,
    "medicine_menu": medicine_menu.handle,
    "add_stock": add_stock.handle,
    "remove_medicine": remove_medicine.handle,
}
