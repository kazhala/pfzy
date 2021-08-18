"""Module contains the async interface to match needle against haystack in batch."""
import asyncio
import heapq
from typing import Any, Callable, Dict, List, Union, cast

from pfzy.score import SCORE_INDICIES, fzy_scorer, substr_scorer


async def _rank_task(
    scorer: Callable[[str, str], SCORE_INDICIES],
    needle: str,
    haystacks: List[Union[str, Dict[str, Any]]],
    key: str,
    offset: int,
) -> List[Dict[str, Any]]:
    result = []
    for index, haystack in enumerate(haystacks):
        score, indicies = scorer(needle, cast(Dict, haystack)[key])
        if indicies is None:
            continue
        result.append(
            {
                "score": score,
                "indicies": indicies,
                "haystack": haystack,
                "index": index + offset,
            }
        )
    result.sort(key=lambda x: x["score"], reverse=True)
    return result


async def fuzzy_match(
    needle: str,
    haystacks: List[Union[str, Dict[str, Any]]],
    key: str = "",
    batch_size: int = 4096,
) -> List[Dict[str, Any]]:
    """Fuzzy find needle within list of haystack and get matched results with matching index.

    Args:
        needle: String to search within the `haystacks`.
        haystack: List of haystack/longer strings to be searched.
        key: If `haystacks` is a list of dictionary, provide the key that
            can obtain the haystack value to search.
        batch_size: Number of entry to be processed together.

    Return:
        List of matching `haystacks` with additional key indicies and score.
    """
    if " " in needle:
        scorer = substr_scorer
    else:
        scorer = fzy_scorer

    if not isinstance(haystacks, Dict):
        haystacks = [{"value": haystack} for haystack in haystacks]
        key = "value"

    if not key:
        raise TypeError(
            f"${fuzzy_match.__name__} missing 1 required argument: 'key', 'key' is required when haystacks is an instance of dict"
        )

    batches = await asyncio.gather(
        *(
            _rank_task(
                scorer,
                needle,
                haystacks[offset : offset + batch_size],
                key,
                offset,
            )
            for offset in range(0, len(haystacks), batch_size)
        )
    )
    results = heapq.merge(*batches, key=lambda x: x["score"], reverse=True)
    choices = []
    for candidate in results:
        choices.append({**candidate["haystack"], "indices": candidate["indices"]})
    return choices
