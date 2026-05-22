from app.db.vector_db import QdrantStorage
from app.models.custom_types import RAGSearchResult
from app.services.embedding_service import generate_embeddings

def retrieve_contexts(
    question: str,
    top_k: int = 5
) -> RAGSearchResult:

    query_vector = generate_embeddings(
        [question]
    )[0]

    store = QdrantStorage()

    found = store.search(
        query_vector,
        top_k
    )

    return RAGSearchResult(
        contexts=found["contexts"],
        sources=found["sources"]
    )