"""Sharp finite-panel bounds with an exact fallback count. Costs may be integer ticks."""
from itertools import accumulate
from math import isfinite


class Panel:
    def __init__(self, costs, count):
        self.costs = tuple(costs)
        n = len(self.costs)
        if not isinstance(count, int) or not 0 <= count <= n:
            raise ValueError("count must be an integer between zero and panel size")
        if any(not isfinite(x) or x < 0 for x in self.costs):
            raise ValueError("costs must be finite and nonnegative")
        self.count = count
        self.order = sorted(range(n), key=self.costs.__getitem__)
        self.prefix = list(accumulate((self.costs[i] for i in self.order), initial=0))

    def window(self, budget):
        n = len(self.order)
        if not isinstance(budget, int) or not 0 <= budget <= n:
            raise ValueError("invalid query budget")
        r = n - budget
        k = min(self.count, n - self.count, r // 2)
        p = self.prefix

        def width(start):
            end = start + r
            return p[end] - p[end-k] - p[start+k] + p[start]

        start = min(range(budget + 1), key=width)
        return width(start), start

    def select(self, budget):
        _, start = self.window(budget)
        end = start + len(self.order) - budget
        return self.order[:start] + self.order[end:]

    def worst_width(self, queries):
        remaining = [self.costs[i] for i in self.order if i not in queries]
        k = min(self.count, len(self.order)-self.count, len(remaining)//2)
        return sum(remaining[len(remaining)-k:]) - sum(remaining[:k])

    def bounds(self, observed):
        if any(not isinstance(i, int) or not 0 <= i < len(self.order)
               or v not in (0, 1) for i, v in observed.items()):
            raise ValueError("invalid observed index or flag")
        fixed = sum(self.costs[i] * v for i, v in observed.items())
        h = self.count - sum(observed.values())
        unknown = [self.costs[i] for i in self.order if i not in observed]
        if not 0 <= h <= len(unknown):
            raise ValueError("reported total conflicts with the observed flags")
        return fixed + sum(unknown[:h]), fixed + sum(unknown[len(unknown)-h:])


def allocate(panels, budget):
    """Exact budget allocation across panels in common cost units."""
    if not isinstance(budget, int) or not 0 <= budget <= sum(len(p.order) for p in panels):
        raise ValueError("invalid total budget")
    best = [0]
    choices = []
    for panel in panels:
        limit = min(budget, len(panel.order))
        widths = [panel.window(q)[0] for q in range(limit + 1)]
        stage, picks = [], []
        for b in range(min(budget, len(best)-1 + limit) + 1):
            value, pick = min((best[b-q] + widths[q], q)
                              for q in range(max(0, b-len(best)+1), min(limit, b)+1))
            stage.append(value)
            picks.append(pick)
        choices.append(picks)
        best = stage
    allocation = []
    left = budget
    for picks in reversed(choices):
        allocation.append(picks[left])
        left -= picks[left]
    return best[budget], list(reversed(allocation))
