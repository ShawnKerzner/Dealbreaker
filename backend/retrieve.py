import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config import EMBEDDING_MODEL, CHROMA_PATH, COLLECTION_NAME


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embed_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


def search(question, k=5):
    collection = get_collection()
    results = collection.query(query_texts=[question], n_results=k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    hits = []
    for text, meta, dist in zip(documents, metadatas, distances):
        hit = {
            "text": text,
            "url": meta["url"],
            "section": meta["section"],
            "distance": dist,
        }
        hits.append(hit)

    return hits


if __name__ == "__main__":
    hits = search("Are you SOC 2 certified? Can we see the report?", k=10)
    for i, hit in enumerate(hits):
        print(i, hits[i]["section"])
        print(hits[i]["text"])
        print("-" * 60)
