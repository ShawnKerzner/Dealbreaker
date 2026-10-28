from retrieve import search
from rerank import rerank, should_flag
from test_set import TEST_SET
from generate import generate_answer
import json


def label_of(hit):
    return (hit["url"], hit["section"])


def search_metrics(item, k, use_rerank=False):
    if use_rerank:
        hits = search(item["question"], k=10)
        hits = rerank(item["question"], hits)
        hits = hits[:k]
    else:
        hits = search(item["question"], k=k)

    relevant = {(r["url"], r["section"]) for r in item["relevant"]}

    correct_hits = [hit for hit in hits if label_of(hit) in relevant]
    precision = len(correct_hits) / k

    found = {label_of(hit) for hit in correct_hits}
    recall = len(found) / len(relevant) if relevant else None

    return precision, recall


def report(k, use_rerank):
    label = "RERANKED" if use_rerank else "BASELINE"
    scores = [search_metrics(item, k, use_rerank) for item in TEST_SET]

    for item, (p, r) in zip(TEST_SET, scores):
        print(f"{label}  Q{item['id']}  precision@{k}={p:.2f}  recall@{k}={r}")

    precisions = [p for p, r in scores]
    recalls = [r for p, r in scores if r is not None]
    print(f"{label}  AVERAGE  precision@{k}={sum(precisions)/len(precisions):.2f}  "
          f"recall@{k}={sum(recalls)/len(recalls):.2f}")
    print()


def save_answers(path="answers.json"):
    records = []

    for item in TEST_SET:
        question = item["question"]
        ranked = rerank(question, search(question, k=10))
        record = {
            "id": item["id"],
            "answer": item["reference_answer"],
            "flagged": item["expected"],
        }
        records.append(record)
        # progress, since each Claude call takes a few seconds
        print(f"Q{item['id']} done")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


if __name__ == "__main__":
    report(k=5, use_rerank=False)
    report(k=5, use_rerank=True)
