from app.controllers.metadata_controller import MetadataController
from app.database import SessionLocal, init_db
from app.i18n import load_locale, t
from app.views.router import AppContext, Router
from app.views.routes import ROUTES


def main() -> None:
    init_db()

    session = SessionLocal()
    try:
        metadata_controller = MetadataController(session)
        language = metadata_controller.get_language()
        load_locale(language)

        ctx = AppContext(session=session)
        Router(ROUTES).run("main_menu", ctx)
        print(t("messages.goodbye"))
    finally:
        session.close()


if __name__ == "__main__":
    main()
