from dataclasses import dataclass


@dataclass
class DocumentPage:
    page_number: int
    text: str


@dataclass
class ParsedDocument:
    document_id: str
    filename: str
    pages: list[DocumentPage]