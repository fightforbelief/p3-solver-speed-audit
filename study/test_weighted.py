from itertools import combinations
from design import Panel
from weighted import priced_width


def test_prices_against_all_affordable_subsets():
    costs = (9, 0, 0, 12, 17, 7, 13)
    for prices in ((1, 2, 1, 3, 5, 5, 1), (2,)*7):
        for m in range(len(costs)+1):
            p = Panel(costs, m)
            for b in range(sum(prices)+1):
                expected = min(p.worst_width(set(s))
                               for q in range(8) for s in combinations(range(7),q)
                               if sum(prices[i] for i in s) <= b)
                assert priced_width(p, prices, b) == expected
