= Replaying six solver portfolios
We used six ASlib scenarios with archived per-instance runtimes or penalized runtimes and solver status [1]. They cover answer-set programming, Bayesian network structure learning, constraint satisfaction, mixed-integer programming, quantified Boolean formulas, and industrial SAT. We selected them to span domains with recorded completion times. An ASlib status of _ok_ with time between zero and the published cutoff counts as a solved instance. Repetition 1 supplies one observation per solver and instance.

For each scenario, hashing the instance identifier assigned approximately one fifth of instances to training. We ranked solvers on that split by mean PAR10, charging ten times the published cutoff for an unsuccessful or missing run, with ties broken alphabetically. The first-ranked solver became the reference and the second-ranked solver the presolver. The evaluation split contained both solver records for every instance. The schedule gave the presolver 1% of the scenario cutoff, charged the observed time on success and the full slot on failure, then started the reference from scratch when needed. Slot sizes ranged from 6 to 72 seconds. The reference retained its full original timeout. We used successful reference runs as the primary panel so both procedures return a solved status on every compared instance. The all-instance analysis below also accounts for coverage.

We reconstructed the paired schedule cost from the recorded times, then deliberately masked the per-instance routing flags. The released inputs to the audit were the reference runtimes in indexed order, the failure count, and the sum of first-stage charges. Each check restored one original flag. We used exact integer costs rounded to nanoseconds and stable sorting within ties. At each budget we compared the optimal block, checking the slowest instances, and the mean over 200 uniform query sets drawn without replacement. Each design used the same panel, count and budget. The protocol and released inputs are versioned in the replication package.

#figure(block[#set text(size: 9.7pt)
#include "table_primary.typ"], kind: table, caption: [Primary schedule at a 1% slice. ¹Reference-solved instances used in the paired comparison. The last two columns give the uniform-pairing estimate and observed ratio of total times.])

The first-stage failure count alone was misleading about the cost of those failures (Table 1). Every uniform-pairing estimate was below 0.66. The matched schedules saved roughly 4.2% on ASP and consumed 6.6–12.2% more reference time on BNSL, CSP, MIP and QBF. The SAT difference was 0.047% of reference time and is sensitive to small replay overheads. In all six panels, the flags placed more mass on expensive backup runs than uniform pairing would predict. This comparison tests an aggregation assumption on fixed schedules. The schedules were constructed for this study from the six sets of traces.

#figure(image("intervals.svg",width: 98%),caption: [Sharp endpoints after restoring flags. Each colored segment is the range compatible with the observed transcript for its budget. Different budgets may select different records. The dashed line marks equal time.])

== How many checks settle the comparison?
The initial intervals crossed parity in all six panels. At a 10% budget, the fixed minimax design established the direction only on CSP. At 25% it established the direction on five panels. SAT remained unresolved even at 50%. An audit that aims to certify a direction can stop once both endpoints fall on one side of its decision threshold. For an engineering decision with a minimum material improvement, the threshold should encode that improvement.

#figure(block[#set text(size: 9.4pt)
#include "table_design.typ"], kind: table, caption: [Audit width in units of total reference time. Initial, Minimax and Random are worst-transcript widths for the indicated query sets. Random averages this quantity across 200 sets at the same 10% budget. The last column uses the actual labels restored by the minimax design.])

At the six primary 10% budgets the minimizing block always left the cheap end untouched. Checking the slowest instances therefore attained exactly the same width here. Uniform checks left substantially more uncertainty. The largest contraction occurred on CSP, where 138 checks reduced worst-case width from 0.996 to 0.044. The two-tailed rule matters when the cost order has a different shape, as in the example following Theorem 1.

If the six panels are treated as one additive accounting exercise with separate failure counts, checking 10% in each (rounded down) consumes 394 checks. The proportional allocation is $(91,82,138,16,51,16)$ in table order. Corollary 2 assigns $(38,168,88,31,13,56)$ for the same total. Worst-case width falls from 0.216 to 0.121 of combined reference time, a 43.8% reduction. This example values a recorded second equally across scenarios. A deployment with a different workload mix can reweight the groups before optimization.

== Slice length and unsuccessful reference runs
Giving the presolver 5% or 10% of the cutoff retained the paired advantage on ASP and the disadvantage on the other five primary panels (Table 3). At those slices the uniform-pairing estimate put five and three panels, respectively, on the wrong side of parity. As a separate sensitivity after the primary replay, we included all 4,695 evaluation instances and charged the full cutoff to each unsuccessful reference invocation. This last schedule ratio measures the budget consumed under a fixed-slot policy. Solved counts accompany it because the two policies can cover different instances.

#figure(block[#set text(size: 9.4pt)
#include "table_sensitivity.typ"], kind: table, caption: [The first two ratios use the reference-solved panel. The third ratio and both solved counts use the entire evaluation split with a 1% slice.])

#include "closing.typ"
