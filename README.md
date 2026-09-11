# PRGI Title Verification System

A terminal-based MVP for checking proposed newspaper titles against existing titles and pending applications.

## Problem

The system helps identify potentially conflicting newspaper titles using:

- Fuzzy string similarity
- Phonetic matching
- Prefix and suffix rules
- Restricted-word validation
- Existing-title combination detection
- Periodicity modification detection
- Lightweight multilingual semantic matching
- Pending application checks
- Verification probability and rejection reasons

The design is intended as a foundation for scaling to a large PRGI title dataset.

## Technology Stack

- Python 3
- SQLite
- RapidFuzz
- Double Metaphone
- Pytest

## Project Structure

```text
prgi-title-verifier/
├── src/
│   ├── applications.py
│   ├── combination.py
│   ├── database.py
│   ├── importer.py
│   ├── multilingual.py
│   ├── normalization.py
│   ├── periodicity.py
│   ├── phonetic.py
│   ├── rules.py
│   ├── search.py
│   ├── similarity.py
│   └── verifier.py
├── tests/
│   ├── conftest.py
│   └── test_verification.py
├── data/
│   └── titles.csv
├── database/
├── cli/
├── main.py
├── requirements.txt
└── README.md
```

## Setup

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Initialize the Database

```bash
python3 -m src.database
```

### Import Existing Titles

```bash
python3 -m src.importer
```

The sample dataset contains a small set of titles for demonstration.
The production system can replace this dataset with the full PRGI title database.

### Run the Application

```bash
python3 main.py
```

The terminal interface provides:

```text
1. Verify New Title
2. View Applications
3. Exit
```

## Example Verification

Enter:

```text
India Today
```

The system identifies the existing title and reports a high similarity score.

A restricted-word example:

```text
India Police News
```

The system identifies `police` as a restricted word.

A periodicity example:

```text
Daily India Today
```

The system checks whether the periodicity modification corresponds to an existing title.

A combination example:

```text
Hindu Indian Express
```

The system detects words originating from multiple existing titles.

## Verification Probability

The MVP uses:

```text
Acceptance Probability = 100 - Similarity Score
```

For example:

```text
Similarity Score      = 80%
Acceptance Probability = 20%
```

Hard rejection rules override the probability.

## Testing

Run the complete test suite with:

```bash
pytest -q
```

The tests cover:

- Exact existing-title matches
- Restricted words
- Periodicity modifications
- Existing-title combinations
- New titles
- Acceptance probability

## Current MVP Limitations

The current implementation intentionally uses a lightweight architecture.
Future improvements can include:

- Full PRGI dataset ingestion
- More advanced multilingual semantic models
- Better phonetic indexing
- More sophisticated scoring
- Additional configurable PRGI rules
- Faster candidate retrieval for very large datasets
- Web-based interface
- Detailed application workflow
- Production database deployment

## Demo Workflow

```text
Start application
       ↓
Enter proposed title
       ↓
Normalize title
       ↓
Search existing titles
       ↓
Search pending applications
       ↓
Run fuzzy / phonetic / semantic checks
       ↓
Apply title rules
       ↓
Calculate similarity
       ↓
Calculate acceptance probability
       ↓
Generate verification report
```