from src.database import initialize_database
from src.verifier import verify_title


def setup_module():
    initialize_database()


def test_exact_existing_title():
    result = verify_title("India Today")

    assert result["decision"] == "REJECTED"
    assert result["similarity_score"] >= 80
    assert result["acceptance_probability"] <= 20


def test_restricted_word():
    result = verify_title("India Police News")

    assert result["decision"] == "REJECTED"
    assert "police" in result["restricted_words"]


def test_periodicity_modification():
    result = verify_title("Daily India Today")

    assert result["decision"] == "REJECTED"
    assert result["periodicity_detected"] is True


def test_title_combination():
    result = verify_title("Hindu Indian Express")

    assert result["decision"] == "REJECTED"
    assert result["combination_detected"] is True


def test_new_title():
    result = verify_title(
        "Western Maharashtra Chronicle"
    )

    assert result["decision"] == "LIKELY ACCEPTED"


def test_acceptance_probability():
    result = verify_title("India Today")

    expected_probability = max(
        0.0,
        100.0 - result["similarity_score"],
    )

    assert (
        result["acceptance_probability"]
        == expected_probability
    )
