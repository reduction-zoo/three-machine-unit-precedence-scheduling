# Research instructions

Read the [fixed question](campaigns/three-machine-unit-precedence-scheduling/question.md), [prior state](campaigns/three-machine-unit-precedence-scheduling/state.md) and [preparation notes](campaigns/three-machine-unit-precedence-scheduling/work/preparation.md). The fixed [test corpus](campaigns/three-machine-unit-precedence-scheduling/work/cases.json) and [verifier](campaigns/three-machine-unit-precedence-scheduling/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/three-machine-unit-precedence-scheduling/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
