"""Module contains the async interface to match needle against haystack in batch."""
import asyncio
import heapq
from typing import Any, Callable, Dict, List, Union, cast

from pfzy.score import SCORE_INDICIES, fzy_scorer


async def _rank_task(
    scorer: Callable[[str, str], SCORE_INDICIES],
    needle: str,
    haystacks: List[Union[str, Dict[str, Any]]],
    key: str,
) -> List[Dict[str, Any]]:
    """Calculate the score for needle against given list of haystacks and rank them.

    Args:
        scorer: Scorer to be used to do the calculation.
        needle: Substring to search.
        haystacks: List of dictionary containing the haystack to be searched.
        key: The key within the `haystacks` dictionary that contains the actual string value.

    Return:
        Sorted list of haystacks based on the needle score with additional keys for the `score`
        and `indices`.
    """
    result = []
    for haystack in haystacks:
        score, indicies = scorer(needle, cast(Dict, haystack)[key])
        if indicies is None:
            continue
        result.append(
            {
                "score": score,
                "indicies": indicies,
                "haystack": haystack,
            }
        )
    result.sort(key=lambda x: x["score"], reverse=True)
    return result


async def fuzzy_match(
    needle: str,
    haystacks: List[Union[str, Dict[str, Any]]],
    key: str = "",
    batch_size: int = 4096,
    scorer: Callable[[str, str], SCORE_INDICIES] = None,
) -> List[Dict[str, Any]]:
    """Fuzzy find needle within list of haystack and get matched results with matching index.

    Args:
        needle: String to search within the `haystacks`.
        haystack: List of haystack/longer strings to be searched.
        key: If `haystacks` is a list of dictionary, provide the key that
            can obtain the haystack value to search.
        batch_size: Number of entry to be processed together.

    Returns:
        List of matching `haystacks` with additional key indicies and score.

    Examples:
        >>> import asyncio
        >>> asyncio.run(fuzzy_match("ab", ["acb", "acbabc"]))
        [{'value': 'acbabc', 'indicies': [3, 4]}, {'value': 'acb', 'indicies': [0, 2]}]
    """
    if scorer is None:
        scorer = fzy_scorer

    for index, haystack in enumerate(haystacks):
        if not isinstance(haystack, dict):
            if not key:
                key = "value"
            haystacks[index] = {key: haystack}

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
            )
            for offset in range(0, len(haystacks), batch_size)
        )
    )
    results = heapq.merge(*batches, key=lambda x: x["score"], reverse=True)
    choices = []
    for candidate in results:
        choices.append({**candidate["haystack"], "indicies": candidate["indicies"]})
    return choices
