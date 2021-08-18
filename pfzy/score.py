"""Module contains the score calculation algorithems."""
from functools import partial
from typing import Dict, List, Optional, Tuple

SCORE_MIN = float("-inf")
SCORE_MAX = float("inf")
SCORE_GAP_LEADING = -0.005
SCORE_GAP_TRAILING = -0.005
SCORE_GAP_INNER = -0.01
SCORE_MATCH_CONSECUTIVE = 1.0


def _char_range_with(
    char_start: str, char_stop: str, value, hash_table: Dict[str, int]
) -> Dict[str, int]:
    """Generate index mapping for `bonus` calculation.

    Args:
        char_start: Starting char of the range.
        char_stop: Ending char of the range.
        value: Value to give to the range of char.
        hash_table: Base dictionary to add the mapping.

    Returns:
        A dictionary containing the given range with provided index.

    Examples:
        >>> _char_range_with("a", "d", 1, {})
        {'a': 1, 'b': 1, 'c': 1, 'd': 1}
    """
    hash_table = hash_table.copy()
    hash_table.update(
        (chr(uni_char), value)
        for uni_char in range(ord(char_start), ord(char_stop) + 1)
    )
    return hash_table


lower_with = partial(_char_range_with, "a", "z")
upper_with = partial(_char_range_with, "A", "Z")
digit_with = partial(_char_range_with, "0", "9")

SCORE_MATCH_SLASH = 0.9
SCORE_MATCH_WORD = 0.8
SCORE_MATCH_CAPITAL = 0.7
SCORE_MATCH_DOT = 0.6
BONUS_MAP = {
    "/": SCORE_MATCH_SLASH,
    "-": SCORE_MATCH_WORD,
    "_": SCORE_MATCH_WORD,
    " ": SCORE_MATCH_WORD,
    ".": SCORE_MATCH_DOT,
}
BONUS_STATES = [{}, BONUS_MAP, lower_with(SCORE_MATCH_CAPITAL, BONUS_MAP)]
BONUS_INDEX = digit_with(1, lower_with(1, upper_with(2, {})))


SCORE_INDICIES = Tuple[float, Optional[List[int]]]


def _bonus(haystack: str) -> List[float]:
    """Calculate bonus score for the given haystack.

    The bonus are applied to each char based on the previous char.

    When previous char is within the `BONUS_MAP` then additional bonus
    are applied to the current char due to it might be the start of a new
    word.

    When encountered a mix case character, if the current char is capitalised then
    if the previous char is normal case or within `BONUS_MAP`, additional bounus are applied.

    Args:
        haystack: String to calculate bonus.

    Returns:
        A list of float matching the length of the given haystack
        with each index representing the bonus score to apply.

    Examples:
        >>> _bonus("asdf")
        [0.9, 0, 0, 0]
        >>> _bonus("asdf asdf")
        [0.9, 0, 0, 0, 0, 0.8, 0, 0, 0]
        >>> _bonus("asdf aSdf")
        [0.9, 0, 0, 0, 0, 0.8, 0.7, 0, 0]
        >>> _bonus("asdf/aSdf")
        [0.9, 0, 0, 0, 0, 0.9, 0.7, 0, 0]
    """
    prev_char = "/"
    bonus = []
    for char in haystack:
        bonus.append(BONUS_STATES[BONUS_INDEX.get(char, 0)].get(prev_char, 0))
        prev_char = char
    return bonus


def _score(needle: str, haystack: str) -> SCORE_INDICIES:
    """Use fzy logic to calculate score for `needle` within the given `haystack`.

    2 2D array to track the score.
    1. The running score (`running_score`) which represents the best score for the current position.
    2. The result score (`result_score`) which tracks to overall best score that could be for the current positon.

    With every consequtive match, additional bonuse score are given and for every non matching char, a negative
    gap score is applied.

    After the score is calculated, the final matching score will be stored at the last position of the `result_score`.

    Backtrack the result by comparing the 2 2D array to find the corresponding indicies.

    Args:
        needle: Substring to find in haystack.
        haystack: String to be searched and scored.

    Returns:
        A tuple of matching score with a list of matching indicies.

    Examples:
        >>> _score("ab", "acb")
        (0.89, [0, 2])
        >>> _score("ab", "acbabc")
        (0.98, [3, 4])
    """
    needle_len, haystack_len = len(needle), len(haystack)
    bonus_score = _bonus(haystack)

    # smart case
    if needle.islower():
        haystack = haystack.lower()

    # return all values if no query
    if needle_len == 0 or needle_len == haystack_len:
        return SCORE_MAX, list(range(needle_len))

    # best score for the position
    running_score: List[List[float]] = [
        [0 for _ in range(haystack_len)] for _ in range(needle_len)
    ]

    # overall best score at each position
    result_score: List[List[float]] = [
        [0 for _ in range(haystack_len)] for _ in range(needle_len)
    ]

    for i in range(needle_len):
        prev_score = SCORE_MIN

        # gap between matching char
        # more gaps, less score
        gap_score = SCORE_GAP_TRAILING if i == needle_len - 1 else SCORE_GAP_INNER

        for j in range(haystack_len):
            if needle[i] == haystack[j]:
                score = SCORE_MIN
                if i == 0:
                    score = j * SCORE_GAP_LEADING + bonus_score[j]
                elif j != 0:
                    score = max(
                        result_score[i - 1][j - 1] + bonus_score[j],
                        # consecutive match if value is higher
                        running_score[i - 1][j - 1] + SCORE_MATCH_CONSECUTIVE,
                    )
                running_score[i][j] = score
                result_score[i][j] = prev_score = max(score, prev_score + gap_score)
            else:
                running_score[i][j] = SCORE_MIN
                # increment the best score with gap_score since no match
                result_score[i][j] = prev_score = prev_score + gap_score

    # backtrace to find the all indicies of optimal matching
    # starting from the end to pick the first possible match we encounter
    i, j = needle_len - 1, haystack_len - 1
    # use to determine if the current match is consequtive match
    match_required = False
    indicies = [0 for _ in range(needle_len)]

    while i >= 0:
        while j >= 0:
            # if the prev score is determined to be consecutive match
            # then the current position must be a match
            # e.g. haystack, needle = "auibywcabc", "abc"
            # using match_required: [7, 8, 9]
            # without match_required: [0, 8, 9]
            if (
                match_required or running_score[i][j] == result_score[i][j]
            ) and running_score[i][j] != SCORE_MIN:
                match_required = (
                    i > 0
                    and j > 0
                    and result_score[i][j]
                    == running_score[i - 1][j - 1] + SCORE_MATCH_CONSECUTIVE
                )
                indicies[i] = j
                j -= 1
                break
            else:
                j -= 1
        i -= 1

    return result_score[needle_len - 1][haystack_len - 1], indicies


def _subsequence(needle: str, haystack: str) -> bool:
    """Check if needle is subsequence of haystack.

    Args:
        needle: Substring to find in haystack.
        haystack: String to be searched and scored.

    Returns:
        Boolean indicating if `needle` is subsequence of `haystack`.

    Examples:
        >>> _subsequence("as", "bbwi")
        False
        >>> _subsequence("as", "bbaiws")
        True
        >>> _subsequence("sa", "bbaiws")
        False
    """
    needle, haystack = needle.lower(), haystack.lower()
    if not needle:
        return True
    offset = 0
    for char in needle:
        offset = haystack.find(char, offset) + 1
        if offset <= 0:
            return False
    return True


def fzy_scorer(needle: str, haystack: str) -> SCORE_INDICIES:
    """Use fzy matching algorithem to match needle against haystack.

    Args:
        needle: Substring to find in haystack.
        haystack: String to be searched and scored.

    Returns:
        A tuple of matching score with a list of matching indicies.
    """
    if _subsequence(needle, haystack):
        return _score(needle, haystack)
    else:
        return SCORE_MIN, None


def substr_scorer(needle: str, haystack: str) -> SCORE_INDICIES:
    """Match needle against haystack using substrings.

    Args:
        needle: Substring to find in haystack.
        haystack: String to be searched and scored.

    Returns:
        A tuple of matching score with a list of matching indicies.
    """
    indicies = []
    offset = 0
    needle, haystack = needle.lower(), haystack.lower()

    for needle in needle.split(" "):
        if not needle:
            continue
        offset = haystack.find(needle, offset)
        if offset < 0:
            return SCORE_MIN, None
        needle_len = len(needle)
        indicies.extend(range(offset, offset + needle_len))
        offset += needle_len

    if not indicies:
        return 0, indicies

    return (
        -(indicies[-1] + 1 - indicies[0])
        + 2 / (indicies[0] + 1)
        + 1 / (indicies[-1] + 1),
        indicies,
    )
