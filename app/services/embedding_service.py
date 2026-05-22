from app.services.data_loader import embed_texts

def generate_embeddings(texts: list[str]):
    return embed_texts(texts)