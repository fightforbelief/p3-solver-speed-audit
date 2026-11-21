# Study design

This is a finite-benchmark methods study. The earlier P3 systematic-review snapshot, the five pilot paper codings and the cross-machine OPF timings play no role in estimation. The prior independent Windows checkout at 646e48e9d17d0593ad27ae3690cbd584fb1370d4 remains available to its owner.

## Targets fixed before the first replay

Six purposefully selected ASlib runtime scenarios cover ASP, Bayesian network structure learning, CSP, MIP, QBF and industrial SAT. Input revision and checksums are pinned. Compare a time-limited first solver followed, on failure, by a cold reference solver with the reference alone. The unit is a distinct benchmark instance, repetition 1. Keep the coverage counts for the full evaluation split. The primary panel uses reference-solved instances, so that both procedures return an answer on every retained instance. Charge the full first-stage slice on failures; a supervisor can enforce this fixed-time slot. Assume additive times and no transfer of solver state. This is a replay of archived times.

Assign training instances by the first eight bytes of SHA-256(instance ID), interpreted big-endian, modulo five equal to zero. Rank solvers on training PAR10 (ten times the scenario cutoff for failure, recorded time for success), ties by name. Take the best as fallback and runner-up as first stage. Use 1% of the scenario cutoff as primary slice and 5% and 10% as sensitivities. Exclude instances lacking a pair from the corresponding analysis and disclose counts. Fail closed on duplicates. Record zero reported times as measured. The primary estimand is total schedule cost divided by total baseline cost, with equality at one. Audit width uses these same units.

Hide the linkage between first-stage failure flags and per-instance reference runtimes, retaining the count and total first-stage cost. Evaluate the sharp bounds against the fully paired replay. At budgets 0, 1%, 5%, 10%, 25% and 50% (floor), compare the minimax design with slowest-only and 200 reproducibly seeded uniform subsets. Report worst-case and realized widths and decisions relative to parity. Use both a separately analyzed paired panel per scenario and a joint fixed-total-budget analysis with scenario counts. Repetitions of the audit simulation characterize designs on these fixed panels. They do not generate additional benchmark instances.

## Additional check after the first replay

The primary panel omits instances on which the backup fails. For a separate all-paired-instance sensitivity, record solved counts and charge an unsuccessful backup its entire published cutoff. This measures allocated slot cost even if a failed process stops earlier. Report results independently of the successful-reference panel. The software additionally verifies the unequal-price dynamic program against enumeration and checks replay arithmetic on a fixture containing success, timeout, and success exactly at the slice boundary.
