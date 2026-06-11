from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient import Patient


class PatientController:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Patient]:
        return list(self.session.scalars(select(Patient).order_by(Patient.name)).all())

    def get_by_id(self, patient_id: int) -> Patient | None:
        return self.session.get(Patient, patient_id)

    def create(self, name: str) -> tuple[bool, Patient | str]:
        name = name.strip()
        if not name:
            return False, "errors.empty_name"
        patient = Patient(name=name)
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)
        return True, patient

    def delete(self, patient_id: int) -> tuple[bool, str | None]:
        patient = self.get_by_id(patient_id)
        if patient is None:
            return False, "errors.patient_not_found"
        self.session.delete(patient)
        self.session.commit()
        return True, None
