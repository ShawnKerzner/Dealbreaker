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
]
