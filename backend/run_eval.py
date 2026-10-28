from retrieve import search
from rerank import rerank, should_flag
from test_set import TEST_SET
from generate import generate_answer
import json
import re
import evaluate
from transformers import AutoTokenizer, AutoModelForCausalLM
import math
import torch


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
            "answer": generate_answer(question, ranked),
            "flagged": should_flag(ranked),
        }
        records.append(record)
        print(f"Q{item['id']} done")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def clean_answer(answer_text):
    text = re.sub(r"\[\d+\]", "", answer_text)
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"^- ", "", text, flags=re.MULTILINE)
    return text


def compute_perplexity(texts):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()

    perplexities = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            loss = model(**inputs, labels=inputs["input_ids"]).loss
        perplexities.append(math.exp(loss.item()))

    return (sum(perplexities)/len(perplexities))


def score_answers(path="answers.json"):
    with open(path, encoding="utf-8") as f:
        records = json.load(f)

    reference_by_id = {item["id"]: item["reference_answer"]
                       for item in TEST_SET}

    predictions = [clean_answer(record["answer"]) for record in records]
    references = [reference_by_id[record["id"]] for record in records]

    rouge = evaluate.load("rouge").compute(
        predictions=predictions, references=references)
    bleu = evaluate.load("bleu").compute(
        predictions=predictions, references=references)
    perplexity = compute_perplexity(predictions)

    return rouge, bleu, perplexity


if __name__ == "__main__":
    report(k=5, use_rerank=False)
    report(k=5, use_rerank=True)
    rouge, bleu, perplexity = score_answers()
    print(f"ANSWERS  ROUGE-1={rouge['rouge1']:.2f}  ROUGE-2={rouge['rouge2']:.2f}  "
          f"ROUGE-L={rouge['rougeL']:.2f}  BLEU={bleu['bleu']:.2f}  Perplexity={perplexity:.1f}")
