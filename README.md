# pfzy

[![CI](https://github.com/kazhala/pfzy/workflows/CI/badge.svg)](https://github.com/kazhala/pfzy/actions?query=workflow%3ACI)
[![Docs](https://img.shields.io/readthedocs/pfzy?label=Docs&logo=Read%20the%20Docs)](https://readthedocs.org/projects/pfzy/)
[![Build](https://codebuild.ap-southeast-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiT2pwUFo2MVBzV1ptL0d4VDhmSHo4bSswVHFuaEh6bEU1d2g3bmpsdnZjSzcwWkxac3NHcjBKZDkyT2t1R0VveHJ0WlNFWmZmUjNQUGFpemxwV2loRm9rPSIsIml2UGFyYW1ldGVyU3BlYyI6Imw4dlcwYjlxaU9kYVd0UkoiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)](https://ap-southeast-2.console.aws.amazon.com/codesuite/codebuild/378756445655/projects/pfzy/history?region=ap-southeast-2&builds-meta=eyJmIjp7InRleHQiOiIifSwicyI6e30sIm4iOjIwLCJpIjowfQ)
[![Coverage](https://img.shields.io/coveralls/github/kazhala/pfzy?logo=coveralls)](https://coveralls.io/github/kazhala/pfzy?branch=master)
[![Version](https://img.shields.io/pypi/pyversions/pfzy)](https://pypi.org/project/pfzy/)
[![PyPi](https://img.shields.io/pypi/v/pfzy)](https://pypi.org/project/pfzy/)
[![License](https://img.shields.io/pypi/l/pfzy)](https://github.com/kazhala/pfzy/blob/master/LICENSE)

<!-- start elevator-pitch-intro -->

Python port of the [fzy](https://github.com/jhawthorn/fzy) fuzzy string matching algorithm.

- [Async fuzzy match function](https://pfzy.readthedocs.io/en/latest/pages/usage.html#matcher)
- [Fzy scorer (fuzzy string match)](https://pfzy.readthedocs.io/en/latest/pages/usage.html#fzy-scorer)
- [Substring scorer (exact substring match)](https://pfzy.readthedocs.io/en/latest/pages/usage.html#substr-scorer)

## Requirements

```
python >= 3.7
```

## Installation

```sh
pip install pfzy
```

## Quick Start

**Full documentation: [https://pfzy.readthedocs.io/](https://pfzy.readthedocs.io/)**

```python
import asyncio

from pfzy import fuzzy_match

result = asyncio.run(fuzzy_match("ab", ["acb", "acbabc"]))
```

```
>>> print(result)
[{'value': 'acbabc', 'indices': [3, 4]}, {'value': 'acb', 'indices': [0, 2]}]
```

<!-- end elevator-pitch-intro -->

## Background

[fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) is a famous python package for performing fuzzy matching
between strings powered by [python-Levenshtein](https://github.com/miohtama/python-Levenshtein). While it does its
job well it doesn't calculate/provide the matching indices which is essential in a fuzzy finder applications.

The [fzy](https://github.com/jhawthorn/fzy) fuzzy matching algorithm can calculate the matching score while also
providing the matching indices which fuzzy finder applications can use to provide extra highlights.

The initial implementation of this algorithm can be found at [sweep.py](https://github.com/aslpavel/sweep.py) which
is a python implementation of the terminal fuzzy finder. The code snippet is later used by the project [vim-clap](https://github.com/liuchengxu/vim-clap).

**I found myself needing this logic across multiple projects hence decided to strip out the logic and publish a dedicated
package with detailed documentation and unittest.**

<!-- start elevator-pitch-ending -->

## Credit

- [fzy](https://github.com/jhawthorn/fzy)
- [sweep.py](https://github.com/aslpavel/sweep.py)
- [vim-clap](https://github.com/liuchengxu/vim-clap)

## LICENSE

> All 3 projects mentioned in [Credit](#credit) are all licensed under [MIT](https://opensource.org/licenses/MIT).

This project is licensed under [MIT](https://github.com/kazhala/pfzy). Copyright (c) 2021 Kevin Zhuang

<!-- end elevator-pitch-ending -->
