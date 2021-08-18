import pytest

from pfzy.score import SCORE_MAX, _bonus, _char_range_with, _score, _subsequence


def test_char_range_with():
    result = _char_range_with("0", "9", 10, {"a": 1})
    assert result == {
        "0": 10,
        "1": 10,
        "2": 10,
        "3": 10,
        "4": 10,
        "5": 10,
        "6": 10,
        "7": 10,
        "8": 10,
        "9": 10,
        "a": 1,
    }

    result = _char_range_with("A", "D", 2, {})
    assert result == {"A": 2, "B": 2, "C": 2, "D": 2}


def test_bonus():
    assert _bonus("abc") == [0.9, 0, 0]
    assert _bonus("abc abc") == [0.9, 0, 0, 0, 0.8, 0, 0]
    assert _bonus("abc/abc") == [0.9, 0, 0, 0, 0.9, 0, 0]
    assert _bonus("abc/abC") == [0.9, 0, 0, 0, 0.9, 0, 0.7]
    assert _bonus("/abc") == [0, 0.9, 0, 0]


def test_score():
    assert _score("", "abc") == (SCORE_MAX, [])
    assert _score("abc", "abc") == (SCORE_MAX, [0, 1, 2])
    assert _score("abc", "acbabc") == (1.9849999999999999, [3, 4, 5])
    assert _score("abc", "acbABC") == (2.685, [3, 4, 5])
    assert _score("ABC", "acbABC") == (2.685, [3, 4, 5])
    assert _score("b ABC", "acb bABC") == (3.6799999999999997, [2, 3, 5, 6, 7])


def test_subsequence():
    assert _subsequence("awc", "abc") == False
    assert _subsequence("awc", "abcwc") == True
    assert _subsequence("a ui", "waui wou i") == True
    assert _subsequence("", "waui wou i") == True
