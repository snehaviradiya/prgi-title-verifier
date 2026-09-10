from src.combination import detect_combination
from src.multilingual import semantic_similarity
from src.periodicity import detect_periodicity_modification
from src.phonetic import phonetic_similarity
from src.rules import (
    check_prefix_suffix,
    validate_restricted_words,
)
from src.search import search_candidates
from src.similarity import calculate_similarity


SIMILARITY_THRESHOLD = 80.0


def verify_title(title: str) -> dict:
    """
    Run all title verification checks and generate
    a unified verification result.
    """

    restricted = validate_restricted_words(title)
    combination = detect_combination(title)
    periodicity = detect_periodicity_modification(title)
    prefix_suffix = check_prefix_suffix(title)

    candidates = search_candidates(title)

    highest_fuzzy = 0.0
    highest_phonetic = 0.0
    highest_semantic = 0.0
    best_match = None

    for candidate in candidates:
        existing_title = candidate["title"]

        fuzzy_score = calculate_similarity(
            title,
            existing_title,
        )

        phonetic_score = phonetic_similarity(
            title,
            existing_title,
        )

        semantic_score = semantic_similarity(
            title,
            existing_title,
        )

        highest_fuzzy = max(highest_fuzzy, fuzzy_score)
        highest_phonetic = max(highest_phonetic, phonetic_score)
        highest_semantic = max(highest_semantic, semantic_score)

        combined_score = max(
            fuzzy_score,
            phonetic_score,
            semantic_score,
        )

        if best_match is None or combined_score > best_match["score"]:
            best_match = {
                "title": existing_title,
                "score": combined_score,
            }

    similarity_score = max(
        highest_fuzzy,
        highest_phonetic,
        highest_semantic,
    )

    acceptance_probability = round(
        max(0.0, 100.0 - similarity_score),
        2,
    )

    rejection_reasons = []

    if restricted["restricted_words"]:
        for word in restricted["restricted_words"]:
            rejection_reasons.append(
                f"Restricted word detected: {word}"
            )

    if combination["detected"]:
        rejection_reasons.append(
            "Title appears to combine existing titles"
        )

    if periodicity["detected"]:
        for existing_title in periodicity["matching_titles"]:
            rejection_reasons.append(
                f"Periodicity modification of existing title: "
                f"{existing_title}"
            )

    if similarity_score >= SIMILARITY_THRESHOLD:
        if best_match:
            rejection_reasons.append(
                f"High similarity with existing title: "
                f"{best_match['title']}"
            )

    if rejection_reasons:
        decision = "REJECTED"
    else:
        decision = "LIKELY ACCEPTED"

    return {
        "title": title,
        "decision": decision,
        "similarity_score": similarity_score,
        "acceptance_probability": acceptance_probability,
        "fuzzy_score": round(highest_fuzzy, 2),
        "phonetic_score": round(highest_phonetic, 2),
        "semantic_score": round(highest_semantic, 2),
        "best_match": best_match,
        "rejection_reasons": rejection_reasons,
        "restricted_words": restricted["restricted_words"],
        "combination_detected": combination["detected"],
        "combination_matches": combination["matching_titles"],
        "periodicity_detected": periodicity["detected"],
        "periodicity_matches": periodicity["matching_titles"],
        "prefix": prefix_suffix["prefix"],
        "suffix": prefix_suffix["suffix"],
    }


if __name__ == "__main__":
    examples = [
        "India Today",
        "India Police News",
        "Daily India Today",
        "Completely New Newspaper",
    ]

    for example in examples:
        result = verify_title(example)

        print()
        print("=" * 55)
        print(f"Title: {result['title']}")
        print(f"Decision: {result['decision']}")
        print(f"Similarity: {result['similarity_score']}%")
        print(
            f"Acceptance probability: "
            f"{result['acceptance_probability']}%"
        )

        if result["best_match"]:
            print(
                f"Best match: "
                f"{result['best_match']['title']} "
                f"({result['best_match']['score']}%)"
            )

        if result["rejection_reasons"]:
            print("Reasons:")

            for reason in result["rejection_reasons"]:
                print(f"- {reason}")