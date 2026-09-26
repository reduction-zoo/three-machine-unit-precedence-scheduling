# Prepared input and output contract

The source is 3-SAT with clauses of at most three signed literals. Its JSON input
is `{"num_vars": n, "clauses": [[literals], ...]}` with `n >= 0`, each literal a
nonzero integer of absolute value at most `n`, and each clause of length at most
three. Repeated literals, empty clauses and unused variables are legal. A source
output is `{"assignment": [bool, ...]}` of length `n` satisfying every clause,
or `{"status": "NO-SOLUTION"}` exactly when no assignment exists.

The target is unit-job precedence scheduling on three identical machines. Its
JSON input is `{"jobs": n, "edges": [[u, v], ...], "deadline": T}` with `n,T >= 0`
and a directed acyclic edge graph over job indices `0..n-1`. A target output is
`{"start": [slot, ...]}` of length `n`: integer slots are nonnegative and below
`T`, every edge `u -> v` has `start[u] + 1 <= start[v]`, and no slot has more than
three jobs. This is equivalent to an assignment to three identical machines.
The alternative `{"status": "NO-SOLUTION"}` is valid only if no such schedule
exists. The empty job set has a valid empty schedule even when `T = 0`.

A candidate `algorithm.py` reads one source JSON object from stdin and writes one
legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source output.
Both commands must exit nonzero on errors and send diagnostics to stderr. The
candidate must be deterministic and polynomial time. For every legal source
instance and every valid target output, recovery must return a valid source
output. This includes alternate schedules and explicit NO-SOLUTION outputs.

`check.py` derives source and target answers independently of any candidate.
Positive outputs are checked by direct clause or schedule evaluation. Negative
outputs require a conclusive solver result. `--candidate PATH` injects the fixed
source corpus, solves each constructed target independently, and validates every
recovered source output.
