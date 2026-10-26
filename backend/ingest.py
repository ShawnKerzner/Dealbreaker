import requests
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config import EMBEDDING_MODEL, CHROMA_PATH, COLLECTION_NAME

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS, strip_headers=False)

size_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=150)
size_splitter.split_text("some long string")

URLS = [
    "https://posthog.com/docs/privacy.md",
    "https://posthog.com/docs/privacy/gdpr-compliance.md",
    "https://posthog.com/docs/privacy/hipaa-compliance.md",
    "https://posthog.com/docs/privacy/ccpa-compliance.md",
    "https://posthog.com/docs/privacy/soc2.md",
    "https://posthog.com/handbook/company/security.md",
]


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()

    content_type = response.headers["Content-Type"]
    if not content_type.startswith("text/plain"):
        raise ValueError(
            f"Expected markdown but got {content_type} from {url}")

    return {"url": url, "text": response.text}


def fetch_urls(url_list):
    result = []
    for url in url_list:
        page = fetch_page(url)
        result.append(page)
    return result


def clean_text(text):
    lines = text.split("\n")
    kept = []

    for line in lines:
        if "AI agents:" in line:
            continue
        if "Canonical URL:" in line:
            continue
        if "## On this page" in line:
            continue
        if line.startswith("- [") and "](#" in line:
            continue
        kept.append(line)

    return "\n".join(kept)


def split_page(page):
    pieces = splitter.split_text(page["text"])
    chunks = []

    for piece in pieces:
        section = " > ".join(piece.metadata.values())
        texts = size_splitter.split_text(piece.page_content)

        for text in texts:
            chunk = {
                "text": text,
                "url": page["url"],
                "section": section
            }
            chunks.append(chunk)

    return chunks


def chunk_pages(pages):
    all_chunks = []

    for page in pages:
        page["text"] = clean_text(page["text"])
        page_chunks = split_page(page)
        all_chunks.extend(page_chunks)
    return all_chunks


def store_chunks(chunks):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embed_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(
        name=COLLECTION_NAME, embedding_function=embed_fn)

    ids = [str(i) for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"url": chunk["url"], "section": chunk["section"]}
                 for chunk in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return collection.count()


if __name__ == "__main__":
    pages = fetch_urls(URLS)
    chunks = chunk_pages(pages)
    count = store_chunks(chunks)
    print("stored:", count)
