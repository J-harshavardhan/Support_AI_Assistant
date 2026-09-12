"""TF-IDF and hybrid FAQ matching for SupportAI Task 3."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from task1 import faqs, search_by_keyword


class FAQMatcher:
    """Match user questions to FAQs using TF-IDF and cosine similarity."""

    def __init__(self, faqs):
        """Build a TF-IDF index from each FAQ's question and keywords."""
        self.faqs = faqs
        self.vectorizer = TfidfVectorizer(stop_words="english")
        corpus = [
            f"{faq['question']} {' '.join(faq['keywords'])}"
            for faq in faqs
        ]
        self.faq_vectors = self.vectorizer.fit_transform(corpus)

    def match(self, query, top_k=3):
        """Return up to top_k FAQs ranked by cosine similarity to query."""
        if top_k <= 0:
            return []

        query_vector = self.vectorizer.transform([query])
        similarity_scores = cosine_similarity(query_vector, self.faq_vectors)[0]
        ranked_indexes = similarity_scores.argsort()[::-1][:top_k]

        return [
            (self.faqs[index], round(float(similarity_scores[index]), 4))
            for index in ranked_indexes
        ]

    def best_match(self, query, threshold=0.15):
        """Return the best FAQ when its score reaches the supplied threshold."""
        matches = self.match(query, top_k=1)
        if matches and matches[0][1] >= threshold:
            return matches[0]
        return None

    def explain_match(self, query):
        """Return a readable explanation of the top three FAQ matches."""
        lines = [f"Query: {query}", "TF-IDF matches:"]
        for position, (faq, score) in enumerate(self.match(query, top_k=3), 1):
            lines.append(f"  {position}. [{score:.4f}] {faq['question']}")
        return "\n".join(lines)


def hybrid_search(faqs, query, top_k=3):
    """Combine Task 1 keyword hits with TF-IDF scores and rank the results."""
    matcher = FAQMatcher(faqs)
    # Keep one score per FAQ and retain whichever method gives the higher score.
    scores_by_id = {}

    for faq in search_by_keyword(faqs, query):
        scores_by_id[faq["id"]] = (faq, 0.5)

    for faq, score in matcher.match(query, top_k=len(faqs)):
        current = scores_by_id.get(faq["id"])
        if current is None or score > current[1]:
            scores_by_id[faq["id"]] = (faq, score)

    ranked_results = list(scores_by_id.values())
    ranked_results.sort(key=lambda result: result[1], reverse=True)
    return [
        (faq, round(float(score), 4))
        for faq, score in ranked_results[:top_k]
    ]


def _print_ranked_results(results):
    """Print FAQ matches in the format used by the comparison demonstration."""
    if not results:
        print("  (no results)")
        return

    for position, (faq, score) in enumerate(results, 1):
        print(f"  {position}. [{score:.4f}] {faq['question']}")


def demonstrate_comparison():
    """Compare keyword, TF-IDF, and hybrid matching for three queries."""
    matcher = FAQMatcher(faqs)
    queries = [
        "I forgot my login credentials",
        "Can I get my money back?",
        "package delivery time",
    ]

    for query in queries:
        print(f"Query: {query}\n")

        print("[Keyword Search]")
        keyword_matches = search_by_keyword(faqs, query)
        if keyword_matches:
            for faq in keyword_matches[:3]:
                print(f"  {faq['question']}")
        else:
            print("  (no results)")

        print("\n[TF-IDF Matching]")
        tfidf_matches = matcher.match(query)
        _print_ranked_results(tfidf_matches)

        print("\n[Hybrid Search]")
        hybrid_matches = hybrid_search(faqs, query)
        _print_ranked_results(hybrid_matches)

        best = matcher.best_match(query)
        if best:
            print(f"\nBest match: {best[0]['question']} (confidence: {best[1]:.4f})")
        else:
            print("\nBest match: None")
        print("-" * 60)


if __name__ == "__main__":
    demonstrate_comparison()
