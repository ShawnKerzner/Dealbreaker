from retrieve import search
from test_set import TEST_SET


def label_of(hit):
    return (hit["url"], hit["section"])


def search_metrics(item, k):
    hits = search(item["question"], k=k)
    relevant = {(r["url"], r["section"]) for r in item["relevant"]}

    correct_hits = [hit for hit in hits if label_of(hit) in relevant]
    precision = len(correct_hits) / k

    found = {label_of(hit) for hit in correct_hits}
    recall = len(found) / len(relevant) if relevant else None

    return precision, recall


if __name__ == "__main__":
    for item in TEST_SET:
        p, r = search_metrics(item, k=5)
        print(f"Q{item['id']}  precision@5={p:.2f}  recall@5={r}")
    scores = [search_metrics(item, k=5) for item in TEST_SET]
    precisions = [p for p, r in scores]
    recalls = [r for p, r in scores if r is not None]
    print(
        f"AVERAGE  precision@5={sum(precisions)/len(precisions):.2f}  recall@5={sum(recalls)/len(recalls):.2f}")
