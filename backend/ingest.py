import requests

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


if __name__ == "__main__":
    pages = fetch_urls(URLS)
    cleaned = clean_text(pages[0]["text"])
    print(cleaned[:800])
