from datetime import date
from decimal import Decimal, InvalidOperation

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.medicine import Medicine
from app.models.stock_entry import StockEntry
from app.services.stock_service import stock_summary


class StockController:
    def __init__(self, session: Session):
        self.session = session

    def add_entry(
        self,
        medicine_id: int,
        quantity: str,
        entry_date: date | None = None,
    ) -> tuple[bool, StockEntry | str]:
        medicine = self.session.get(Medicine, medicine_id)
        if medicine is None or not medicine.active:
            return False, "errors.medicine_not_found"

        try:
            qty = Decimal(quantity.strip())
            if qty <= 0:
                return False, "errors.invalid_quantity"
        except (InvalidOperation, AttributeError):
            return False, "errors.invalid_quantity"

        if entry_date is None:
            entry_date = date.today()

        entry = StockEntry(
            entry_date=entry_date,
            quantity=qty,
            medicine_id=medicine_id,
        )
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return True, entry

    def list_current_stock(self, patient_id: int) -> list[dict]:
        medicines = list(
            self.session.scalars(
                select(Medicine)
                .where(Medicine.patient_id == patient_id, Medicine.active.is_(True))
                .options(selectinload(Medicine.stock_entries))
                .order_by(Medicine.name)
            ).all()
        )
        return [stock_summary(medicine) for medicine in medicines]
