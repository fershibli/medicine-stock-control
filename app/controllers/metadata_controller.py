from sqlalchemy.orm import Session

from app.models.metadata import Metadata

SUPPORTED_LANGUAGES = ("en", "pt-br")


class MetadataController:
    def __init__(self, session: Session):
        self.session = session

    def get_language(self) -> str:
        metadata = self.session.get(Metadata, 1)
        if metadata is None:
            metadata = Metadata(id=1, language="en")
            self.session.add(metadata)
            self.session.commit()
        return metadata.language

    def set_language(self, language: str) -> tuple[bool, str | None]:
        if language not in SUPPORTED_LANGUAGES:
            return False, "errors.invalid_input"
        metadata = self.session.get(Metadata, 1)
        if metadata is None:
            metadata = Metadata(id=1, language=language)
            self.session.add(metadata)
        else:
            metadata.language = language
        self.session.commit()
        return True, None
