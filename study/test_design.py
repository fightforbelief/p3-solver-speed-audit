from itertools import combinations, product
from functools import lru_cache
from design import Panel, allocate
import pytest


def test_every_transcript_against_all_compatible_completions():
    for costs in [(1, 1, 5, 7, 23), (0,), (), (1, 100, 103, 108, 111, 113)]:
        n = len(costs)
        for m in range(n+1):
            panel = Panel(costs, m)
            flags = [v for v in product(range(2), repeat=n) if sum(v) == m]
            for q in range(n+1):
                candidates = []
                for subset in combinations(range(n), q):
                    groups = {}
                    for v in flags:
                        key = tuple(v[i] for i in subset)
                        groups.setdefault(key, []).append(sum(a*b for a,b in zip(v, costs)))
                    for key, vals in groups.items():
                        assert panel.bounds(dict(zip(subset, key))) == (min(vals), max(vals))
                    actual = max(max(vals)-min(vals) for vals in groups.values())
                    assert panel.worst_width(set(subset)) == actual
                    candidates.append(actual)
                assert panel.window(q)[0] == min(candidates)
                assert panel.worst_width(set(panel.select(q))) == min(candidates)


def test_sequential_minimax_with_group_counts():
    costs = (0, 5, 8, 90, 1, 17, 24)
    panels = [Panel(costs[:4], 2), Panel(costs[4:], 1)]
    flags = [v for v in product(range(2), repeat=7) if sum(v[:4]) == 2 and sum(v[4:]) == 1]

    @lru_cache(None)
    def value(ids, remaining, q):
        if not q:
            sums = [sum(x*y for x,y in zip(costs, flags[j])) for j in ids]
            return max(sums)-min(sums)
        def response(i):
            parts = [tuple(j for j in ids if flags[j][i] == v) for v in (0, 1)]
            return max(value(p, tuple(s for s in remaining if s != i), q-1) for p in parts if p)
        return min(map(response, remaining))

    for q in range(8):
        width, allocation = allocate(panels, q)
        assert sum(allocation) == q
        assert width == value(tuple(range(len(flags))), tuple(range(7)), q)


def test_invalid_transcript():
    with pytest.raises(ValueError):
        Panel([0,1,2],1).bounds({0:1,1:1})
