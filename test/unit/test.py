import pytest
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
    assert ('A', 'B') in result


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
    assert ('A', 'B') in result


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
    assert ('A', 'B') in result


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
    assert ('A', 'B') in result


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
    assert ('A', 'B') in result


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


def test_empty_input_returns_no_duplicates():
    bib = ""
    result = detect_duplicates(bib)
    assert result == []


def test_malformed_bibtex_raises_error():
    # missing closing brace in second entry
    bib = """
    @article{A,
      title={Bad Entry}
    }
    @article{B,
      title={Also Bad"
    """
    with pytest.raises(Exception):
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
    assert result == [('A', 'B')]

# Test Structure:
# Each one the tests follows one scenario from my design table. I chose clear, minimal BibTeX strings to isolate each condition.

# Test Independence:
# All tests build their own bibtex input in the function body, with no shared fixtures or global state.

# Challenges:
# Making malformed BibTeX that triggers parser errors got me errors, 
# also making sure each test only assert one outcome to keeping tests clear.
