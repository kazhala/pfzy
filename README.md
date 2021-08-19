# pfzy

<!-- start elevator-pitch -->

[![CI](https://github.com/kazhala/pfzy/workflows/CI/badge.svg)](https://github.com/kazhala/pfzy/actions?query=workflow%3ACI)
[![Coverage](https://img.shields.io/coveralls/github/kazhala/pfzy?logo=coveralls)](https://coveralls.io/github/kazhala/pfzy?branch=master)

Python port of the [fzy](https://github.com/jhawthorn/fzy) fuzzy string matching algorithm.

## Requirements

```
python >= 3.7
```

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

## Credit

- [fzy](https://github.com/jhawthorn/fzy)
- [sweep.py](https://github.com/aslpavel/sweep.py)
- [vim-clap](https://github.com/liuchengxu/vim-clap)

## LICENSE

> All 3 projects mentioned in [Credit](#credit) are all licensed under [MIT](https://opensource.org/licenses/MIT).

This project is licensed under [MIT](https://github.com/kazhala/pfzy). Copyright (c) 2021 Kevin Zhuang

<!-- end elevator-pitch -->
