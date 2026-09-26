# 3-SAT → Three-machine unit-job precedence scheduling

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

The target gives a precedence DAG of unit-time jobs and an integer deadline T. Find an integer-slot schedule on three identical machines respecting precedences and finishing by T, or report NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This is a longstanding small-machine scheduling boundary with broad relevance to precedence-constrained computation.

## Difficulty

With only three machines and unit jobs, gadgets have little numerical freedom and must enforce choices through precedences alone.

## Literature context

The three-machine unit-job precedence case is a classical scheduling question; hardness when the number of machines varies does not resolve this fixed-machine case.

Literature checked 2026-09-15. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [A Subexponential Time Algorithm for Makespan Scheduling of Unit Jobs with Precedence Constraints](https://arxiv.org/html/2312.03495): - R10: Nederlof, Swennenhuis, Węgrzycki, A Subexponential Time Algorithm for Makespan Scheduling of Unit Jobs with Precedence Constraints, Open Question 1, Theorem 1.1 and ensuing discussion; 2026 ACM journal record. Full proof inspected in the preprint; journal publication metadata checked separately.
- [2026 ACM journal record](https://doi.org/10.1145/3785365): - R10: Nederlof, Swennenhuis, Węgrzycki, A Subexponential Time Algorithm for Makespan Scheduling of Unit Jobs with Precedence Constraints, Open Question 1, Theorem 1.1 and ensuing discussion; 2026 ACM journal record. Full proof inspected in the preprint; journal publication metadata checked separately.

Fixed from board record `website/questions/three-machine-unit-precedence-scheduling.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
