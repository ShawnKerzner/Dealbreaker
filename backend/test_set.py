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
        "reference_answer": "The documentation doesn't offer a guarantee, but PostHog Cloud EU is hosted on servers in Frankfurt so user data stays in EU jurisdiction, and customers can choose to host their data on PostHog's AWS servers in the EU (Germany) instead of the US.",
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
        "reference_answer": "Yes. PostHog is certified as SOC 2 Type 2 compliant following an external audit. The latest security report is publicly available, and reports, policies, and certifications can be accessed through the Trust Center.",
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
        "reference_answer": "The latest SOC 2 report covers controls as of May 31, 2026, with a reporting period from June 1 to May 31 each year. One archived source gives May 31, 2025, so the sources disagree and the date should be verified before replying.",
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
        "reference_answer": "Yes, PostHog Cloud can be used under HIPAA with a Business Associate Agreement, which is only offered on the Boost, Scale, or Enterprise package. A BAA does not cover every feature, such as PostHog AI, and compliance also depends on how features are configured, so check with a sales engineer.",
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
        "reference_answer": "On PostHog Cloud, PostHog acts as the data processor and the customer is the data controller. If the customer self-hosts PostHog, they are both the processor and the controller.",
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
        "reference_answer": "Yes. PostHog provides data deletion features to handle right to be forgotten requests under GDPR and deletion requests under the CCPA, and a user's data can be deleted programmatically or manually.",
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
        "reference_answer": "PostHog's security policies supporting SOC 2 are available for viewing and on request through the Trust Center. The documentation does not name an incident response plan or encryption policy specifically, so check with a sales engineer.",
    },
    {
        "id": 8,
        "question": "Are you ISO 27001 certified?",
        "expected": "flag",
        "relevant": [],
        "reference_answer": "The documentation does not say whether PostHog is ISO 27001 certified, so check with a sales engineer before replying.", }
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
    for item in TEST_SET:
        words = len(item["reference_answer"].split())
        print(f"Q{item['id']}  reference words={words}")
