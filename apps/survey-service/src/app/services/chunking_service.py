from __future__ import annotations

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except Exception:  # pragma: no cover - optional dependency fallback
    RecursiveCharacterTextSplitter = None


class DocumentChunkingService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            if RecursiveCharacterTextSplitter is not None
            else None
        )

    def chunk_text(self, text: str) -> list[str]:
        if self.splitter is not None:
            return self.splitter.split_text(text)

        chunks: list[str] = []
        start = 0
        text_length = len(text)
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunks.append(text[start:end])
            if end >= text_length:
                break
            start = max(end - self.chunk_overlap, start + 1)
        return chunks
