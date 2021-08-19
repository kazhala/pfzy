# Usage

## Matcher

The [pfzy](https://github.com/jhawthorn/fzy) package provides an async entry point [fuzzy_match](https://pfzy.readthedocs.io/en/latest/pages/api.html#pfzy.match.fuzzy_match) to perform
fuzzy matching using a given string against a given list of strings and will perform ranking automatically.

```{code-block} python
---
caption: main.py
---
import asyncio

from pfzy import fuzzy_match

async def main():
  return await fuzzy_match("ab", ["acb", "acbabc"])

if __name__ == "__main__":
  print(asyncio.run(main()))
```

```{code-block} python
>>> python main.py
[{"value": "acbabc", "indices": [3, 4]}, {"value": "acb", "indices": [0, 2]}]
```

### Matching against dictionaries

The second argument can also be a list of dictionary but you'll have to also specify the argument `key` so that
the function knows which key in the dictionary contains the value to match.

```{code-block} python
import asyncio

from pfzy import fuzzy_match

result = asyncio.run(fuzzy_match("ab", [{"val": "acb"}, {"val": "acbabc"}], key="val"))
```

```{code-block} python
>>> print(result)
[{"val": "acbabc", "indices": [3, 4]}, {"val": "acb", "indices": [0, 2]}]
```

### Using different scorer

By default, it uses the [fzy_scorer](#fzy_scorer) to perform string matching if not specified. You can
explicitly set a different scorer using the argument `scorer`. Reference [#Scorer](#scorer) for a list of
available scorers.

```{code-block} python
import asyncio

from pfzy import fuzzy_match, substr_scorer

result = asyncio.run(fuzzy_match("ab", ["acb", "acbabc"], scorer=substr_scorer))
```

```{code-block} python
>>> print(result)
[{'value': 'acbabc', 'indices': [3, 4]}]
```

## Scorer

### [fzy_scorer](https://pfzy.readthedocs.io/en/latest/pages/api.html#pfzy.score.fzy_scorer)

```{Tip}
The higher the score, the higher the string similarity.
```

The `fzy_scorer` uses [fzy](https://github.com/jhawthorn/fzy) matching logic to perform string fuzzy
matching.

The returned value is a tuple with the matching score and the matching indices.

```{code-block} python
from pfzy import fzy_scorer

score, indices = fzy_scorer("ab", "acbabc")
```

```{code-block} python
>>> print(score)
0.98
>>> print(indices)
[3, 4]
```

### [substr_scorer](https://pfzy.readthedocs.io/en/latest/pages/api.html#pfzy.score.substr_scorer)

```{Note}
The score returned by `substr_scorer` might be negative value, but it doesn't mean its not a match.
As a rule of thumb, the higher the score, the higher the string similarity.
```

Use this scorer when exact substring matching is preferred. Different than the [fzy_scorer](#fzy_scorer),
`substr_scorer` only performs exact matching and the score calculation works differently.

The returned value is a tuple with the matching score and the matching indices.

```{code-block} python
from pfzy import substr_scorer

score, indices = substr_scorer("ab", "awsab")
```

```{code-block} python
>>> print(score)
-1.3
>>> print(indices)
[3, 4]
```

```{code-block} python
from pfzy import substr_scorer

score, indices = substr_scorer("ab", "asdafswabc")
```

```{code-block} python
>>> print(score)
-1.6388888888888888
>>> print(indices)
[7, 8]
```
