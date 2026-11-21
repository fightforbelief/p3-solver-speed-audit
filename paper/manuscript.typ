#set document(title: "Which fallback flags should a solver benchmark recover?", author: ("Yunjie Guo", "Hanqing Yang"))
#set page(paper: "a4", margin: (x: 23mm, y: 19.5mm), numbering: "1")
#set text(font: "Libertinus Serif", size: 10.8pt, lang: "en")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.25em, below: 0.55em)
#let term(x) = text(weight: "bold", x)
#let note(title, body) = block(above: 0.65em, below: 0.6em)[#term(title) #body]
#align(center)[
#set par(justify: false)
#text(size: 20pt, weight: "bold")[Which fallback flags should a solver benchmark recover?]
#v(0.35em)
#text(size: 13pt)[Minimax audits of runtime with a known failure count]
#v(0.7em)
Yunjie Guo and Hanqing Yang\
Independent Researcher, Suzhou, China\
Correspondence: #link("mailto:hanqing.yang189@gmail.com")[Hanqing Yang]
]
#v(0.5em)
#include "abstract.typ"
= A speed comparison with a missing join
Consider an archive of a solver benchmark. A front end attempted every instance, recorded its total time and reported how often it needed a backup solver. A second log gives the time taken by the backup on each instance. Joining the two logs would reveal whether the expensive instances were also the ones routed to the backup. If run identifiers survive, an ordinary join settles the question. If a join requires checking a trace or rerunning a deterministic first-stage decision, which records should the auditor recover first?

Schedules with a time-limited presolver and a backup are established components of solver portfolios [1, 2]. A related setting is a learned optimization proxy with an acceptance test and an exact backup. Either architecture incurs backup cost selectively. A nominal solver time multiplied by the reported failure rate silently assumes zero empirical covariance between cost and failure. The archive may have enough information to bound this covariance even when it cannot determine its sign.

We give an exact decision rule for allocating a fixed number of checks. It identifies a consecutive block in cost order whose flags may remain hidden. We prove a matching lower bound for every deterministic sequential audit and extend it to budgets shared by groups. When individual checks have different prices, computing the best width becomes NP-hard. We examine the practical size of the bounds by masking and restoring known flags from public solver traces. The object of inference throughout is the recorded panel.

= What the released information identifies
Write $c_i >= 0$ for the cost of running the backup from a cold start on instance $i$, and $z_i in {0,1}$ for the decision to invoke it. The known quantities are the list of $n$ indexed costs, the count $m=sum_i z_i$, and the total front-end time $A$ including checks. The target is the aggregate runtime ratio
$ R = (A + sum_i c_i z_i) / B, quad B = sum_i c_i > 0. $
A ratio below one favors the two-stage procedure. A comparison at matched quality requires the accepted outputs and the backup outputs to satisfy the target specification. For a fixed panel, $R$ aggregates time before division. Its reciprocal gives throughput speedup under serial additive timing. We optimize width in cost units or, equivalently, in $R$. Taking reciprocals changes the design objective.

The fallback must incur the recorded $c_i$ under either procedure. A warm start that depends on the front-end state, parallel execution, setup costs that depend on the subset, and order-dependent caches require a different accounting model. We assume that each recovered flag agrees with the original routing decision. We condition on published totals; measurement error and run-to-run hardware variation require additional data.

Let $Q$ denote the checked indices, $K=sum_(i in Q)c_i z_i$, and $h=m-sum_(i in Q)z_i$. In the residual list of length $r=n-|Q|$, let $L_h$ and $U_h$ be the sums of the $h$ smallest and largest costs. Empty sums are zero. The sharp lower and upper endpoints of $R$ are
$ (A+K+L_h)/B quad "and" quad (A+K+U_h)/B. $
Assigning the residual flags to the corresponding tails attains each endpoint. The interior may contain unattainable values because flags are binary. These extrema are the finite binary case of rearrangement bounds for fixed marginals [3]. The uniform-pairing estimate $A/B+m/n$ is a random-permutation expectation. It equals the paired ratio exactly when the empirical covariance between the costs and flags vanishes.

= Equal-price audits
For costs in a residual set $S$, define $D_k(S)=U_k(S)-L_k(S)$. For a fixed budget $q$ write $r=n-q$ and
$ k = min(m,n-m,floor(r/2)). $
#note([Theorem 1.], [Sort the costs as $x_1 <= dots.c <= x_n$. Among all deterministic audits of at most $q$ flags, the minimum worst-case residual width in cost units is
$ W(q) = min_(0 <= s <= q) D_k({x_(s+1),dots.c,x_(s+r)}). $
Braces denote an indexed multiset. An optimal batch checks the $s$ cheapest and the $q-s$ most expensive records. A sequential audit choosing its next index after each answer has the same worst-case value.])

_Proof._ For a fixed unchecked set $S$, the residual count ranges from $max(0,m-q)$ to $min(m,r)$. The width at count $h$ is $D_h(S)=D_(r-h)(S)$. Up to the middle rank this width increases weakly, since extending the two tails adds a nonnegative difference. The attainable count nearest $r/2$ therefore gives $D_k(S)$. In particular, even a very small failure count can place almost all of the uncertainty on a few extreme runtimes.

To minimize this width, take any residual subsequence with indices $i_1 < dots.c < i_r$. For $k>0$, anchor a consecutive block so that its $k$th index equals $i_k$. Its first $k$ indices are at least as large as the corresponding indices of the subsequence. Its remaining indices are at most as large. The bottom-$k$ sum increases weakly and the top-$k$ sum decreases weakly, since $2k <= r$. The block lies in $1,dots,n$ because the original subsequence has enough indices on either side of the anchor. For $k=0$ every design has zero width.

For the sequential lower bound an adversary answers with the more numerous remaining flag, breaking ties arbitrarily. After any number of queries the less numerous flag has remaining count $min(m,n-m,floor(r/2))$. Each answer has a compatible completion, independently of the chosen index. Thus the terminal width is $D_k(S)$ for the residual set on that path, at least the best block value. Padding an early-stopping rule with further queries can only tighten its interval. The fixed block achieves the bound. $square.stroked$

With sorted prefix sums, the scan checks $q+1$ candidate blocks in $O(q+1)$ time after $O(n log n)$ preprocessing. The row identities travel with the sorting permutation. Stable ordering handles ties. If a decision requires a worst-case width at most $epsilon B$, monotonicity of $W$ permits binary search over budgets. A realized transcript can settle a decision much earlier, even when its endpoints are far apart on the same side of parity.

For example, take costs $(1,2,100,101,102)$, two failures and two checks. Checking costs 1 and 2 leaves worst-case width 2. Checking 101 and 102 leaves width 99. In heavy right tails the best block can instead start at rank one. A rule that always checks the slowest records has no general minimax guarantee relative to the optimal width: increasing the separation between the two clusters makes its relative loss arbitrarily large.

= Shared budgets and unequal prices
#note([Corollary 2 (known group counts).], [Suppose group $g$ has its own fixed count $m_g$ and aggregate cost is additive across groups. Let $W_g(b)$ be the width from Theorem 1 on that group. The minimum worst-case width is $min sum_g W_g(q_g)$ subject to $sum_g q_g=q$ and $0 <= q_g <= n_g$. This holds even if queries and group allocations may depend on earlier answers.])

_Proof._ Widths add because the extrema within distinct groups can be attained simultaneously. Apply the majority adversary separately within each group. At termination it attains the worst width for the actual residual subset in every group, and their sum is bounded below by the best allocation. Fixed optimal blocks attain equality. The usual budget recurrence minimizes over the queries assigned to the last group. After tabulating widths, $G$ groups require at most $O(G q^2)$ work. Positive fixed group weights multiply the corresponding widths. $square.stroked$

#note([Proposition 3 (priced checks).], [With a positive integer price per flag and budget $C$, the minimum worst-case width is NP-hard to compute, even for one group with exactly half the flags positive. An exact dynamic program is pseudopolynomial.])

_Proof._ For each of $p$ knapsack items introduce a positive runtime equal to its value and a query price equal to its weight. Add $p$ zero runtimes, each priced at $C+1$, and set $m=p$. After $j$ affordable queries there are $p-j$ positive costs and all $p$ zeros left. The top $floor((2p-j)/2)$ positions include every surviving positive cost and the bottom positions can all be zero. The worst width is the sum of the surviving positive costs. Minimizing it maximizes the value packed into the budget, which is the 0–1 knapsack problem [4]. A proposed query set and its attained worst-case width can be checked in polynomial time. The majority adversary gives the same lower bound for sequential querying with a price budget. Adding a common positive constant to every runtime leaves each width unchanged.

For an exact algorithm fix the final residual size $r$ and compute $k$ as above. In sorted order the $j$th retained item contributes its cost times $-1$ for $j<=k$, $+1$ for $j>r-k$, and zero otherwise. After scanning a prefix, keep the smallest signed sum for each pair (retained count, spent budget). Retaining an item appends its signed contribution; querying it charges its price. Minimize over final spend at most $C$ and over all $r$. With rolling tables this costs $O(n^3(C+1))$ time and $O(n(C+1))$ storage. The reduction and algorithm identify weak NP-hardness for integer inputs. $square.stroked$

Robust optimization with information discovery also studies which uncertain coefficients to observe before a decision [5, 6]. In robust selection, a decision maker can choose an item or a feasible solution after observing information. Here the solver schedule is fixed and the objective is the diameter of its compatible aggregate runtimes. The no-query interval follows from classical extremal coupling, while the block and majority arguments address the additional query-design problem. The minimax comparison takes the worst transcript, with no probability model on labels. Randomized audits evaluated in expectation against an oblivious adversary have a different risk criterion.

#include "empirical.typ"
