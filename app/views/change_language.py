from app.controllers.metadata_controller import MetadataController, SUPPORTED_LANGUAGES
from app.i18n import load_locale, t
from app.views.helpers import clear_screen, pause, print_error, read_menu_choice, render_menu
from app.views.router import AppContext


def handle(ctx: AppContext) -> str | None:
    clear_screen()
    options = [(code, f"change_language.options.{code}") for code in SUPPORTED_LANGUAGES]
    render_menu("change_language.title", options)
    choice = read_menu_choice(len(options))

    language = SUPPORTED_LANGUAGES[choice - 1]
    controller = MetadataController(ctx.session)
    success, error = controller.set_language(language)

    if success:
        load_locale(language)
        label = t(f"change_language.options.{language}")
        print(t("change_language.saved").format(language=label))
    else:
        print_error(str(error))

    pause()
    return "main_menu"
