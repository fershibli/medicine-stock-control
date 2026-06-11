from datetime import date
from decimal import Decimal

from app.models.medicine import Medicine
from app.models.stock_entry import StockEntry


def remaining_for_entry(
    quantity: Decimal,
    daily_dose: Decimal,
    entry_date: date,
    today: date,
) -> Decimal:
    days = (today - entry_date).days
    return max(Decimal("0"), quantity - daily_dose * days)


def current_stock(medicine: Medicine, today: date | None = None) -> Decimal:
    if today is None:
        today = date.today()
    return sum(
        remaining_for_entry(entry.quantity, medicine.daily_dose, entry.entry_date, today)
        for entry in medicine.stock_entries
    )


def stock_summary(medicine: Medicine, today: date | None = None) -> dict:
    if today is None:
        today = date.today()
    return {
        "medicine_id": medicine.id,
        "name": medicine.name,
        "daily_dose": medicine.daily_dose,
        "unit": medicine.unit,
        "current_stock": current_stock(medicine, today),
    }
