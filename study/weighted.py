"""Exact worst-case width when auditing each flag has a known integer price."""
from design import Panel


def priced_width(panel: Panel, prices, budget):
    if len(prices) != len(panel.order) or any(type(p) is not int or p <= 0 for p in prices):
        raise ValueError("one positive integer price is required per flag")
    if type(budget) is not int or budget < 0:
        raise ValueError("invalid budget")
    n = len(prices)
    if sum(prices) <= budget:
        return 0
    best = panel.window(0)[0]
    max_queries = 0
    spent = 0
    for price in sorted(prices):
        if spent + price > budget:
            break
        spent += price
        max_queries += 1
    for q in range(1, max_queries+1):
        r = n-q
        k = min(panel.count, n-panel.count, r//2)
        states = {(0, 0): 0}
        for i, idx in enumerate(panel.order):
            nxt = {}
            for (j, used), value in states.items():
                if j < r:
                    sign = int(j >= r-k) - int(j < k)
                    key = j+1, used
                    nxt[key] = min(nxt.get(key, float("inf")), value + sign*panel.costs[idx])
                if i-j < q and used + prices[idx] <= budget:
                    key = j, used + prices[idx]
                    nxt[key] = min(nxt.get(key, float("inf")), value)
            states = nxt
        best = min(best, min(v for (j,_),v in states.items() if j == r))
    return best
