TEST_SET = [
    {
        "id": 1,
        "question": "We're an EU company. Can you guarantee our data stays in the EU?",
        "expected": "answer",
        "relevant": [
            {"url": "https://posthog.com/docs/privacy/gdpr-compliance.md",
             "section": "PostHog & GDPR compliance > How to set PostHog up for GDPR compliance > Step 1: Choose a hosting provider"},
            {"url": "https://posthog.com/docs/privacy.md",
             "section": "Privacy compliance > Frequently asked questions > Is PostHog GDPR compliant?"},
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > GDPR > PostHog's obligations as a Data Processor"},
        ],
        "reference_answer": "",
    },
    {
        "id": 2,
        "question": "Are you SOC 2 certified? Can we see the report?",
        "expected": "answer",
        "relevant": [
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > SOC 2"},
            {"url": "https://posthog.com/docs/privacy/soc2.md",
             "section": "PostHog & SOC 2 compliance"},
        ],
        "reference_answer": "",
    },
    {
        "id": 3,
        "question": "How current is your SOC 2 report?",
        "expected": "conflict",
        "relevant": [
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > SOC 2"},
            {"url": "https://posthog.com/docs/privacy/soc2.md",
             "section": "PostHog & SOC 2 compliance"},
            {"url": "fixture://stale_soc2_page.md",
             "section": "PostHog & SOC 2 compliance (archived copy)"},
        ],
        "reference_answer": "",
    },
    {
        "id": 4,
        "question": "We handle patient data. Can we use PostHog under HIPAA?",
        "expected": "partial",
        "relevant": [
            {"url": "https://posthog.com/docs/privacy.md",
             "section": "Privacy compliance > Frequently asked questions > Is Google Analytics HIPAA compliant?"},
            {"url": "https://posthog.com/docs/privacy.md",
             "section": "Privacy compliance > Frequently asked questions > Can I use PostHog Cloud under HIPAA?"},
            {"url": "https://posthog.com/docs/privacy/hipaa-compliance.md",
             "section": "PostHog & HIPAA compliance > How to set PostHog up for HIPAA compliance"},
            {"url": "https://posthog.com/docs/privacy/hipaa-compliance.md",
             "section": "PostHog & HIPAA compliance"},
        ],
        "reference_answer": "",
    },
    {
        "id": 5,
        "question": "Under GDPR, are you the controller or the processor?",
        "expected": "answer",
        "relevant": [
            {"url": "https://posthog.com/docs/privacy/gdpr-compliance.md",
             "section": "PostHog & GDPR compliance > How to set PostHog up for GDPR compliance"},
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > GDPR > PostHog's obligations as a Data Processor"},
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > GDPR"},
        ],
        "reference_answer": "",
    },
    {
        "id": 6,
        "question": "If one of our users asks to be deleted, can we remove their data?",
        "expected": "answer",
        "relevant": [
            {"url": "https://posthog.com/docs/privacy/gdpr-compliance.md",
             "section": "PostHog & GDPR compliance > How to set PostHog up for GDPR compliance > Step 6: Complying with 'right to be forgotten' requests"},
            {"url": "https://posthog.com/docs/privacy/ccpa-compliance.md",
             "section": "PostHog & CCPA compliance > How to set PostHog up for CCPA compliance > Step 3: Security configuration"},
            {"url": "https://posthog.com/docs/privacy/ccpa-compliance.md",
             "section": "PostHog & CCPA compliance > What is the CCPA?"},
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > CCPA"},
        ],
        "reference_answer": "",
    },
    {
        "id": 7,
        "question": "Can we see your incident response plan and encryption policy?",
        "expected": "partial",
        "relevant": [
            {"url": "https://posthog.com/handbook/company/security.md",
             "section": "Security & Privacy - Handbook > SOC 2 > Policies"},
            {"url": "https://posthog.com/docs/privacy/soc2.md",
             "section": "PostHog & SOC 2 compliance > Policies"},
        ],
        "reference_answer": "",
    },
    {
        "id": 8,
        "question": "Are you ISO 27001 certified?",
        "expected": "flag",
        "relevant": [],
        "reference_answer": "",
    }
]

if __name__ == "__main__":
    from retrieve import get_collection

    stored = get_collection().get(include=["metadatas"])["metadatas"]
    existing = {(m["url"], m["section"]) for m in stored}

    for item in TEST_SET:
        for label in item["relevant"]:
            if (label["url"], label["section"]) not in existing:
                print(f"Q{item['id']} label not found:", label["section"])
    print("label check done")
