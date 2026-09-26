# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus has
120 distinct legal 3-SAT instances: 20 hand-labelled edge cases and 100 seeded
random cases (seeds 0 through 100, omitting one duplicate source). It contains
64 satisfiable and 56 unsatisfiable formulas; variable counts range from 0 to 6
and clause counts from 0 to 10. The generator and seeds are in
`generate_cases.py`; independently checked outputs are stored in `cases.json`.

The source oracle is Z3 4.16.0: one Boolean per variable and one disjunction per
clause. A satisfying model yields an assignment, checked directly against all
clauses. UNSAT yields NO-SOLUTION; unknown is an error. An exhaustive textbook
enumeration of all Boolean assignments agreed with the oracle on all 120 cases.
The 20 edge-case statuses were hand labelled and checked against it.

The target oracle is also Z3 4.16.0, with one integer start slot per job,
precedence inequalities and at-most-three capacity at each slot. These
constraints are equivalent to a schedule because unit jobs on identical
machines need only a distinct machine for simultaneous jobs. Returned schedules
are checked directly; UNSAT is conclusive and unknown is an error. Exhaustive
slot enumeration agreed with Z3 on 304 DAG/deadline combinations with at most
four jobs and deadline at most three. Hand fixtures cover a required precedence,
over-capacity infeasibility, malformed outputs and an illegal cyclic instance.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/three-machine-unit-precedence-scheduling/work/check.py --self-test
```

The self-test starts with `research/validate_preparation.py`, regenerates every
random source from its seed, recomputes the stored answers, validates positive
witnesses directly, and checks both oracles against the finite exhaustive
references. `check.py --candidate PATH` implements independent target injection
and recovery checks, including up to three distinct target schedules per case.
An injected incorrect candidate was rejected after its legal target schedule
was solved and its NO-SOLUTION recovery failed direct source validation. No
actual reduction candidate exists, so successful end-to-end verification is
untested. The corpus and exhaustive cross-checks cover only the finite sizes
above; they do not prove a reduction, establish hardness, or settle novelty.
