"""Independent source and target oracles for the fixed preparation corpus."""

import argparse
import json
import subprocess
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target, dict):
        return False
    n = target.get("jobs")
    deadline = target.get("deadline")
    edges = target.get("edges")
    if type(n) is not int or n < 0 or type(deadline) is not int or deadline < 0 or not isinstance(edges, list):
        return False
    if any(not isinstance(edge, list) or len(edge) != 2 or any(type(vertex) is not int or vertex < 0 or vertex >= n for vertex in edge) for edge in edges):
        return False
    successors = [[] for _ in range(n)]
    indegree = [0] * n
    for parent, child in edges:
        successors[parent].append(child)
        indegree[child] += 1
    frontier = [vertex for vertex in range(n) if indegree[vertex] == 0]
    seen = 0
    while frontier:
        parent = frontier.pop()
        seen += 1
        for child in successors[parent]:
            indegree[child] -= 1
            if indegree[child] == 0:
                frontier.append(child)
    return seen == n


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal target schedule instance")
    n, deadline = target["jobs"], target["deadline"]
    starts = [z3.Int(f"start{i}") for i in range(n)]
    solver = z3.Solver()
    for start in starts:
        solver.add(0 <= start, start < deadline)
    for parent, child in target["edges"]:
        solver.add(starts[parent] + 1 <= starts[child])
    for slot in range(deadline):
        solver.add(z3.Sum(*(z3.If(start == slot, 1, 0) for start in starts)) <= 3)
    answers = []
    while len(answers) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        answer = [model.eval(start).as_long() for start in starts]
        answers.append({"start": answer})
        solver.add(z3.Or(*(start != value for start, value in zip(starts, answer))))
    return answers or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, limit=1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    starts = output.get("start")
    if set(output) != {"start"} or not isinstance(starts, list) or len(starts) != target["jobs"] or any(type(slot) is not int or slot < 0 or slot >= target["deadline"] for slot in starts):
        return False
    counts = Counter(starts)
    return all(count <= 3 for count in counts.values()) and all(starts[parent] + 1 <= starts[child] for parent, child in target["edges"])


def self_test():
    from generate_cases import EDGE_CASES, random_source

    root = Path(__file__).resolve().parents[3]
    cases_path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(cases_path)], check=True, cwd=root)
    cases = json.loads(cases_path.read_text())
    for n, clauses, expected_satisfiable in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars": n, "clauses": clauses})) == expected_satisfiable
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        expected = case["expected"]
        assert ("assignment" in current) == ("assignment" in expected)
        assert ("assignment" in current) == any(valid_source(source, {"assignment": list(values)})
                                                  for values in product((False, True), repeat=source["num_vars"]))
        assert valid_source(source, expected)
        assert valid_source(source, current)

    satisfiable = {"num_vars": 1, "clauses": [[1]]}
    contradictory = {"num_vars": 1, "clauses": [[1], [-1]]}
    assert valid_source(satisfiable, {"assignment": [True]})
    assert not valid_source(satisfiable, {"assignment": [False]})
    assert valid_source(satisfiable, solve_source(satisfiable))
    assert solve_source(contradictory) == {"status": "NO-SOLUTION"}
    assert not valid_source(satisfiable, {"assignment": [1]})

    schedulable = {"jobs": 2, "edges": [[0, 1]], "deadline": 2}
    over_capacity = {"jobs": 4, "edges": [], "deadline": 1}
    assert valid_target(schedulable, {"start": [0, 1]})
    assert not valid_target(schedulable, {"start": [0, 0]})
    assert valid_target(schedulable, solve_target(schedulable))
    assert solve_target(over_capacity) == {"status": "NO-SOLUTION"}
    assert valid_target(over_capacity, {"status": "NO-SOLUTION"})
    assert not valid_target(schedulable, {"start": ["0", 1]})
    assert not legal_target({"jobs": 1, "edges": [[0, 0]], "deadline": 1})
    target_cases = 0
    for n in range(5):
        possible_edges = list(combinations(range(n), 2))
        for mask in range(1 << len(possible_edges)):
            edges = [list(edge) for index, edge in enumerate(possible_edges) if mask & (1 << index)]
            for deadline in range(4):
                target = {"jobs": n, "edges": edges, "deadline": deadline}
                brute = any(valid_target(target, {"start": list(starts)})
                            for starts in product(range(deadline), repeat=n))
                assert ("start" in solve_target(target)) == brute
                target_cases += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {target_cases} exhaustive target checks")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Candidate produced an illegal target from {source}")
        for target_output in target_solutions(target):
            if not valid_target(target, target_output):
                raise AssertionError(f"Target oracle returned an invalid output: {target_output}")
            payload = {"source": source, "target_solution": target_output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            source_output = json.loads(extraction.stdout)
            if not valid_source(source, source_output):
                raise AssertionError(f"Invalid recovery from {target_output}: {source_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} independently solved target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
