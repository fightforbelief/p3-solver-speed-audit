from replay import capped_panel, summarize


def test_schedule_charges_and_common_quality_population():
    # At a 5-tick slice the first stage solves the first, third and fourth instances.
    rows = [(2, 20), (8, 10), (5, 6), (4, None), (None, None)]
    s, ds, p = summarize("toy", rows, 100, 5)
    assert s["n"] == 3 and p.count == 1 and s["solved_beyond_primary"] == 1
    assert s["paired_ratio"] == (2+5+5+10)/36
    cap = capped_panel("toy",rows,100,5)
    assert cap["schedule_solved"] == 4 and cap["reference_solved"] == 3
    assert cap["actual"] == (2+5+5+4+5+10+100)/236
