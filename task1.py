"""FAQ knowledge base and keyword search for SupportAI Task 1."""

import re


# The FAQ records are deliberately plain dictionaries so later tasks can reuse them.
faqs = [
    {
        "id": "faq-001",
        "category": "Account",
        "question": "How do I reset my password?",
        "answer": "Click 'Forgot Password' on the login page. Enter your registered email address and check your inbox for a reset link valid for 24 hours.",
        "keywords": ["password", "reset", "forgot", "login", "account"],
    },
    {
        "id": "faq-002",
        "category": "Orders",
        "question": "How do I track my order?",
        "answer": "Log into your account and visit the 'My Orders' section. Click the relevant order to see its real-time tracking details.",
        "keywords": ["order", "track", "tracking", "package", "delivery", "shipment"],
    },
    {
        "id": "faq-003",
        "category": "Billing",
        "question": "What is your refund policy?",
        "answer": "We offer full refunds within 30 days of purchase for unused products in their original packaging. Refunds are processed within 5-7 business days.",
        "keywords": ["refund", "money", "return", "billing", "purchase"],
    },
    {
        "id": "faq-004",
        "category": "Support",
        "question": "How do I contact customer support?",
        "answer": "Contact customer support by emailing support@example.com or by calling the toll-free number listed on our website.",
        "keywords": ["contact", "support", "help", "email", "phone"],
    },
    {
        "id": "faq-005",
        "category": "Subscription",
        "question": "How do I cancel my subscription?",
        "answer": "Go to Account Settings, open Subscriptions, and click 'Cancel Subscription'. You will retain access until the current billing cycle ends.",
        "keywords": ["cancel", "subscription", "membership", "plan", "billing"],
    },
    {
        "id": "faq-006",
        "category": "Shipping",
        "question": "How long does package delivery take?",
        "answer": "Standard package delivery times are shown during checkout and in your order confirmation email. Track the package from the 'My Orders' section for the latest update.",
        "keywords": ["shipping", "package", "delivery", "time", "arrive", "shipment"],
    },
    {
        "id": "faq-007",
        "category": "Account",
        "question": "How do I update my email address?",
        "answer": "Open Account Settings, choose Personal Information, update your email address, and save the change.",
        "keywords": ["email", "update", "change", "account", "credentials"],
    },
]

STOPWORDS = {
    "a", "an", "and", "are", "at", "can", "could", "do", "does", "for",
    "how", "i", "in", "is", "it", "my", "of", "on", "the", "to", "what",
    "when", "where", "why", "will", "you", "your"
}


def _tokenize(text):
    """Return lowercase word tokens from a text value."""
    return re.findall(r"[a-z0-9]+", text.lower())


def search_by_keyword(faqs, query):
    """Return FAQs ranked by the number of query-word matches."""
    query_words = {
        word for word in _tokenize(query) if word not in STOPWORDS
    }
    ranked_matches = []

    for faq in faqs:
        searchable_text = " ".join(
            [
                faq["category"],
                faq["question"],
                " ".join(faq["keywords"]),
            ]
        )
        searchable_words = set(_tokenize(searchable_text))
        hit_count = sum(word in searchable_words for word in query_words)
        if hit_count:
            ranked_matches.append((hit_count, faq))

    ranked_matches.sort(key=lambda match: match[0], reverse=True)
    return [faq for _, faq in ranked_matches]


def get_faq_by_id(faqs, faq_id):
    """Return the FAQ with the requested ID, or None when it does not exist."""
    for faq in faqs:
        if faq["id"] == faq_id:
            return faq
    return None


def get_faqs_by_category(faqs, category):
    """Return all FAQs whose category matches case-insensitively."""
    target_category = category.strip().lower()
    return [
        faq for faq in faqs
        if faq["category"].lower() == target_category
    ]


def display_results(query):
    """Print matching FAQ categories, questions, and official answers."""
    print(f"Query: {query}")
    matches = search_by_keyword(faqs, query)
    if not matches:
        print("  No matching FAQs found.")
        return

    for faq in matches:
        print(f"  [{faq['category']}] {faq['question']}")
        print(f"  -> {faq['answer']}")


def demonstrate_search():
    """Run the required Task 1 search demonstrations."""
    for query in ["forgot my password", "refund", "weather today"]:
        display_results(query)
        print()


if __name__ == "__main__":
    demonstrate_search()
