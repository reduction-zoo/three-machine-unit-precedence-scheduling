# 3-SAT → Three-machine unit-job precedence scheduling

Independent research campaign for the [fixed question](campaigns/three-machine-unit-precedence-scheduling/question.md). [State](campaigns/three-machine-unit-precedence-scheduling/state.md) records the current evidence and next action.

The initial commit fixes the question and setup. [Prepare](campaigns/three-machine-unit-precedence-scheduling/work/preparation.md)
has 120 checked source cases and an independently cross-checked target oracle.
No reduction or solution is claimed. Run the campaign from this repository and
follow `AGENTS.md`.

Reproduce with `uv sync --locked`, then run
`uv run --locked python campaigns/three-machine-unit-precedence-scheduling/work/check.py --self-test`.
