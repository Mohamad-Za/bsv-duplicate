import os
import sys
import pytest

# Add project root to path to import the detector module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.util.detector import detect_duplicates


def test_exact_match_all_fields():
    bib = """
    @article{A,
      title={Deep Learning for Cats},
      year={2021},
      doi={10.1000/abc}
    }
    @article{B,
      title={Deep Learning for Cats},
      year={2021},
      doi={10.1000/abc}
    }
    """
    result = detect_duplicates(bib)
    assert set(result) == {"A", "B"}


def test_normalised_title_and_missing_doi():
    bib = """
    @article{A,
      title={Deep Learning for Cats},
      year={2021},
      doi={10.1000/abc}
    }
    @article{B,
      title={deep   learning   for cats!},
      year={2021}
    }
    """
    result = detect_duplicates(bib)
    assert set(result) == {"A", "B"}


def test_same_doi_overrules_year():
    bib = """
    @article{A,
      title={Deep Learning for Cats},
      year={2020},
      doi={10.1000/abc}
    }
    @article{B,
      title={Deep Learning for Cats},
      year={2021},
      doi={10.1000/abc}
    }
    """
    result = detect_duplicates(bib)
    assert set(result) == {"A", "B"}


def test_doi_match_overrules_title():
    bib = """
    @article{A,
      title={Learning about Dogs},
      year={2021},
      doi={10.1000/abc}
    }
    @article{B,
      title={Training Cats},
      year={2021},
      doi={10.1000/abc}
    }
    """
    result = detect_duplicates(bib)
    assert set(result) == {"A", "B"}


def test_missing_doi_but_title_and_year_match():
    bib = """
    @article{A,
      title={Deep Learning for Cats},
      year={2021}
    }
    @article{B,
      title={Deep Learning for Cats},
      year={2021}
    }
    """
    result = detect_duplicates(bib)
    assert set(result) == {"A", "B"}


def test_typo_title_no_doi_not_duplicate():
    bib = """
    @article{A,
      title={Deep Learning for Cats},
      year={2021}
    }
    @article{B,
      title={Deep Learnng for Cats},
      year={2021}
    }
    """
    result = detect_duplicates(bib)
    assert result == []


def test_different_all_fields_not_duplicate():
    bib = """
    @article{A,
      title={Learning about Dogs},
      year={2021},
      doi={10.2000/def}
    }
    @article{B,
      title={Training Cats},
      year={2021},
      doi={10.3000/ghi}
    }
    """
    result = detect_duplicates(bib)
    assert result == []


def test_empty_input_raises_value_error():
    with pytest.raises(ValueError, match="does not contain enough articles"):
        detect_duplicates("")


def test_malformed_bibtex_raises_value_error():
    # Missing closing brace leads to parse result < 2 entries
    bib = """
    @article{A,
      title={Malformed Entry}
    """
    with pytest.raises(ValueError, match="does not contain enough articles"):
        detect_duplicates(bib)


def test_three_entries_only_two_flagged():
    bib = """
    @article{A,
      title={Duplicate Sample},
      year={2021},
      doi={10.1000/dup}
    }
    @article{B,
      title={Duplicate Sample},
      year={2021},
      doi={10.1000/dup}
    }
    @article{C,
      title={Unique Paper},
      year={2021},
      doi={10.2000/uni}
    }
    """
    result = detect_duplicates(bib)
    assert set(result) == {"A", "B"}


# Test file structure and independence notes
#   Each test is a separate function using its own input string.
#   No shared fixtures or external files detect_duplicates is a pure function.
#   Tests cover cases: exact duplicates, normalized titles, DOI priority,
#   positive duplicates, negative (no duplicates), empty input, malformed input.
#   Ensures independence: each call to detect_duplicates starts fresh.
#   Challenge: matching the exact exception and message for parsing errors.