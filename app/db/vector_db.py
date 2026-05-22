from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantStorage:
    # Changed dim back to 3072 to match gemini-embedding-2
    def __init__(self, url="http://localhost:6333", collection="docs_gemini", dim=3072):
        self.client = QdrantClient(url=url, timeout=30)
        # ... rest of the init code stays the same
        self.collection = collection
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, ids, vectors, payloads):
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=points)

    def search(self, query_vector, top_k: int = 5):
        # 1. Use query_points instead of search
        # 2. Change the argument from 'query_vector=' to 'query='
        response = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k
        )
        
        contexts = []
        sources = set()

        # 3. Iterate over response.points instead of the raw response
        for r in response.points:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                contexts.append(text)
            if source:
                sources.add(source)
                
        return {"contexts": contexts, "sources": list(sources)}
    

    