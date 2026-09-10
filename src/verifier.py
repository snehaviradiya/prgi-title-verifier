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


def verify_title(title: str) -> dict:
    """
    Run all current title verification checks.
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

        if fuzzy_score > highest_fuzzy:
            highest_fuzzy = fuzzy_score

        if phonetic_score > highest_phonetic:
            highest_phonetic = phonetic_score

        if semantic_score > highest_semantic:
            highest_semantic = semantic_score

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

    # Start with the strongest similarity signal.
    similarity_score = max(
        highest_fuzzy,
        highest_phonetic,
        highest_semantic,
    )

    # Hard rules override similarity.
    rejected_by_rule = (
        not restricted["valid"]
        or combination["detected"]
        or periodicity["detected"]
    )

    # MVP threshold.
    if rejected_by_rule:
        decision = "REJECTED"
    elif similarity_score >= 80:
        decision = "REJECTED"
    else:
        decision = "LIKELY ACCEPTED"

    return {
        "title": title,
        "decision": decision,
        "similarity_score": round(similarity_score, 2),
        "fuzzy_score": round(highest_fuzzy, 2),
        "phonetic_score": round(highest_phonetic, 2),
        "semantic_score": round(highest_semantic, 2),
        "best_match": best_match,
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
        print("=" * 50)
        print(f"Title: {result['title']}")
        print(f"Decision: {result['decision']}")
        print(f"Similarity: {result['similarity_score']}%")
        print(f"Best match: {result['best_match']}")
        print(f"Restricted words: {result['restricted_words']}")
        print(f"Combination: {result['combination_detected']}")
        print(f"Periodicity: {result['periodicity_detected']}")