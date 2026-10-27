from sentence_transformers import CrossEncoder
from config import RERANK_MODEL, FLAG_THRESHOLD
from retrieve import search
from test_set import TEST_SET


model = CrossEncoder(RERANK_MODEL)


def rerank(question, list_of_hits):
    pairs = [(question, hit["text"]) for hit in list_of_hits]
    scores = model.predict(pairs)
    for hit, score in zip(list_of_hits, scores):
        hit["score"] = float(score)
    return sorted(list_of_hits, key=lambda hit: hit["score"], reverse=True)


def should_flag(ranked_hits):
    if not ranked_hits:
        return True
    return ranked_hits[0]["score"] < FLAG_THRESHOLD


if __name__ == "__main__":
    for item in TEST_SET:
        hits = search(item["question"], k=10)
        ranked = rerank(item["question"], hits)
        top = ranked[0]
        print(
            f"Q{item['id']}  expected={item['expected']:<8}  top_score={top['score']:.4f}  flagged={should_flag(ranked)}")
