from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from retrieve import search
from rerank import rerank, should_flag
from generate import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class AnswerRequest(BaseModel):
    question: str


@app.post("/answer")
def answer_question(request: AnswerRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=400, detail="Question cannot be empty.")
    hits = search(question, k=10)
    ranked = rerank(question, hits)
    flagged = should_flag(ranked)
    answer = generate_answer(question, ranked)
    score = ranked[0]["score"] if ranked else None
    sources = []
    for number, hit in enumerate(ranked[:5], start=1):
        sources.append({
            "number": number,
            "section": hit["section"],
            "url": hit["url"]
        })
    return {
        "answer": answer,
        "flagged": flagged,
        "score": score,
        "sources": sources
    }
