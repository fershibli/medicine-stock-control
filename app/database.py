from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATA_DIR = Path(__file__).parent / "data"
DATABASE_URL = f"sqlite:///{DATA_DIR / 'medicine_control.db'}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    from app.models import Metadata, Medicine, Patient, StockEntry  # noqa: F401

    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        if session.get(Metadata, 1) is None:
            session.add(Metadata(id=1, language="en"))
            session.commit()
    finally:
        session.close()
