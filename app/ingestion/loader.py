from pathlib import Path

from app.ingestion.models import ParsedDocument


class DocumentLoader:

    def load(self, file_path: Path) -> ParsedDocument:
        raise NotImplementedError