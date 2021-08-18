import pytest

from pfzy.match import _rank_task, fuzzy_match
from pfzy.score import fzy_scorer, substr_scorer


@pytest.mark.asyncio
async def test_rank_task() -> None:
    assert await _rank_task(substr_scorer, "abc", [{"val": "wzawbc"}], "val") == []
    assert await _rank_task(
        substr_scorer, "abc", [{"val": "wabco"}, {"val": "abcabc"}], "val"
    ) == [
        {
            "haystack": {"val": "abcabc"},
            "indicies": [0, 1, 2],
            "score": -0.6666666666666667,
        },
        {"haystack": {"val": "wabco"}, "indicies": [1, 2, 3], "score": -1.75},
    ]

    assert await _rank_task(
        fzy_scorer,
        "abc",
        [{"val": "acbabc"}, {"val": "abcABC"}, {"val": "bwd abc"}],
        "val",
    ) == [
        {
            "haystack": {"val": "abcABC"},
            "indicies": [0, 1, 2],
            "score": 2.8850000000000002,
        },
        {
            "haystack": {"val": "bwd abc"},
            "indicies": [4, 5, 6],
            "score": 2.7800000000000002,
        },
        {
            "haystack": {"val": "acbabc"},
            "indicies": [3, 4, 5],
            "score": 1.9849999999999999,
        },
    ]

    assert await _rank_task(
        fzy_scorer, "ab", [{"val": "acb"}, {"val": "acbabc"}], "val"
    ) == [
        {"score": 0.98, "indicies": [3, 4], "haystack": {"val": "acbabc"}},
        {"score": 0.89, "indicies": [0, 2], "haystack": {"val": "acb"}},
    ]


@pytest.mark.asyncio
async def test_fuzzy_match() -> None:
    await fuzzy_match("a", ["abca"]) == [{"value": "abca", "indicies": [0]}]
    await fuzzy_match(
        "a",
        [{"val": "abca"}, {"val": "aAbc"}],
        key="val",
        scorer=substr_scorer,
        batch_size=1,
    ) == [{"val": "abca", "indicies": [0]}, {"val": "aAbc", "indices": [0]}]

    with pytest.raises(TypeError):
        await fuzzy_match("a", [{"val": "abc"}])
