from decimal import Decimal, InvalidOperation

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.medicine import Medicine
from app.models.patient import Patient


class MedicineController:
    def __init__(self, session: Session):
        self.session = session

    def list_active_by_patient(self, patient_id: int) -> list[Medicine]:
        return list(
            self.session.scalars(
                select(Medicine)
                .where(Medicine.patient_id == patient_id, Medicine.active.is_(True))
                .order_by(Medicine.name)
            ).all()
        )

    def list_active_with_stock_by_patient(self, patient_id: int) -> list[Medicine]:
        return list(
            self.session.scalars(
                select(Medicine)
                .where(Medicine.patient_id == patient_id, Medicine.active.is_(True))
                .options(selectinload(Medicine.stock_entries))
                .order_by(Medicine.name)
            ).all()
        )

    def get_by_id(self, medicine_id: int) -> Medicine | None:
        return self.session.get(Medicine, medicine_id)

    def get_active_by_id(self, medicine_id: int) -> Medicine | None:
        medicine = self.get_by_id(medicine_id)
        if medicine is None or not medicine.active:
            return None
        return medicine

    def create(
        self,
        patient_id: int,
        name: str,
        daily_dose: str,
        unit: str,
    ) -> tuple[bool, Medicine | str]:
        patient = self.session.get(Patient, patient_id)
        if patient is None:
            return False, "errors.patient_not_found"

        name = name.strip()
        unit = unit.strip()
        if not name:
            return False, "errors.empty_name"
        if not unit:
            return False, "errors.empty_unit"

        try:
            dose = Decimal(daily_dose.strip())
            if dose <= 0:
                return False, "errors.invalid_dose"
        except (InvalidOperation, AttributeError):
            return False, "errors.invalid_dose"

        medicine = Medicine(
            name=name,
            daily_dose=dose,
            unit=unit,
            patient_id=patient_id,
            active=True,
        )
        self.session.add(medicine)
        self.session.commit()
        self.session.refresh(medicine)
        return True, medicine

    def soft_delete(self, medicine_id: int) -> tuple[bool, str | None]:
        medicine = self.get_by_id(medicine_id)
        if medicine is None:
            return False, "errors.medicine_not_found"
        if not medicine.active:
            return False, "errors.medicine_not_found"
        medicine.active = False
        self.session.commit()
        return True, None
