import uuid

from app.db.vector_db import QdrantStorage
from app.models.custom_types import (
    RAGChunkAndSrc,
    RAGUpsertResult
)
from app.services.data_loader import load_and_chunk_pdf
from app.services.embedding_service import generate_embeddings

def load_pdf_chunks(
    pdf_path: str,
    source_id: str
) -> RAGChunkAndSrc:

    chunks = load_and_chunk_pdf(pdf_path)

    return RAGChunkAndSrc(
        chunks=chunks,
        source_id=source_id
    )

def upsert_chunks(
    chunks_and_src: RAGChunkAndSrc
) -> RAGUpsertResult:

    chunks = chunks_and_src.chunks
    source_id = chunks_and_src.source_id

    vectors = generate_embeddings(chunks)

    ids = [
        str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{source_id}:{i}"
            )
        )
        for i in range(len(chunks))
    ]

    payloads = [
        {
            "source": source_id,
            "text": chunks[i]
        }
        for i in range(len(chunks))
    ]

    QdrantStorage().upsert(
        ids,
        vectors,
        payloads
    )

    return RAGUpsertResult(
        ingested=len(chunks)
    )