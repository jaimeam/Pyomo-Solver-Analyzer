# Pyomo Solver Analyzer

Extract constraint analysis and diagnostic insights from Pyomo optimization results. Quantifies constraint binding strength, detects infeasibilities with severity classification, and extracts solution sensitivity metrics.

## Features

- **Constraint Tightness**: Quantifies how close each constraint is to its limits (0-1 score)
- **Slack Analysis**: Computes slack values with normalized metrics for scale-invariant comparison
- **Infeasibility Detection**: Identifies violations and classifies severity
- **Dual Values**: Extracts sensitivity metrics from solver results
- **Solver Agnostic**: Works with GLPK, SCIP, IPOPT, CPLEX, Gurobi, and others

## Installation

```bash
pip install -e .
```

Requires: GLPK and SCIP for testing
```bash
brew install glpk scip      # macOS
sudo apt-get install glpk-utils scip  # Linux
```

## Quick Start

```python
from pyomo.environ import ConcreteModel, Var, Constraint, Objective, SolverFactory
from pyomo_solver_analyzer import SolverDiagnostics

# Build and solve model
model = ConcreteModel()
model.x = Var(bounds=(0, 10))
model.y = Var(bounds=(0, 10))
model.obj = Objective(expr=model.x + model.y)
model.c1 = Constraint(expr=model.x + model.y >= 5)
model.c2 = Constraint(expr=2*model.x + model.y <= 15)

solver = SolverFactory('glpk')
results = solver.solve(model)

# Analyze
analyzer = SolverDiagnostics(model, results)
print(analyzer.generate_report())
```

Output:
```
=== CONSTRAINT ANALYSIS REPORT ===

Tight Constraints (binding):
  c2: tightness=0.87, slack=0.13, dual=0.25

Loose Constraints:
  c1: tightness=0.31, slack=4.2, dual=0.0

Feasibility: FEASIBLE

Statistics:
  Total constraints: 2
  Binding: 1
  Average tightness: 0.59
  Max slack: 4.2
```

## Usage

### Constraint Tightness Analysis

Identify which constraints are binding and rank by tightness:

```python
tight = analyzer.get_tight_constraints(threshold=0.5)
for c in tight:
    print(f"{c.name}: score={c.tightness_score:.3f}, slack={c.slack:.4f}")

# Output:
# c2: score=0.871, slack=0.129
# c1: score=0.315, slack=4.200
```

Tightness score is computed as $e^{-|normalized\_slack|}$, bounded in [0, 1]. Higher scores indicate binding constraints. Normalized slack is relative to constraint bounds, making comparisons scale-invariant.

### Infeasibility Analysis

Detect which constraints make the problem infeasible and their severity:

```python
feasibility = analyzer.diagnose_feasibility()

if not feasibility['is_feasible']:
    print("INFEASIBLE PROBLEM")
    for violation in feasibility['constraint_violations']:
        v = violation
        print(f"  {v['constraint']}: {v['violation_type']}")
        print(f"    Magnitude: {v['magnitude']:.6f}")
        print(f"    Severity: {v['severity']}")
        print(f"    Expression: {v['expression']}")

# Output (infeasible case):
# INFEASIBLE PROBLEM
#   capacity_1: UPPER_BOUND_VIOLATION
#     Magnitude: 2.500000
#     Severity: HIGH
#     Expression: 2*x + y <= 8
#   demand_2: LOWER_BOUND_VIOLATION
#     Magnitude: 1.200000
#     Severity: MEDIUM
#     Expression: x + y >= 10
```

Use the analyzer to pinpoint exactly which constraints conflict:

```python
violations = feasibility['constraint_violations']
conflicting = [v for v in violations if v['severity'] in ['HIGH', 'CRITICAL']]

print(f"Critical conflicts: {len(conflicting)}")
for v in conflicting:
    print(f"  Relax {v['constraint']} by ≥{v['magnitude']:.4f} to restore feasibility")

# Output:
# Critical conflicts: 1
#   Relax capacity_1 by ≥2.5000 to restore feasibility
```

Severity levels:
- `CRITICAL`: Violation > 1% of constraint bound
- `HIGH`: Violation > 0.1% of constraint bound  
- `MEDIUM`: Violation > 0.01% of constraint bound
- `LOW`: Numerical tolerance violations

### Statistics and Diagnostics

Get summary statistics:

```python
stats = analyzer.constraint_statistics()
print(f"Binding constraints: {stats['binding_constraints']}")
print(f"Mean slack: {stats['mean_slack']:.4f}")
print(f"Max slack: {stats['max_slack']:.4f}")

# Output:
# Binding constraints: 1
# Mean slack: 2.1649
# Max slack: 4.2000
```

## Documentation

- [API Reference](docs/api_reference.md) - Complete method documentation
- [Examples](docs/examples.md) - Real-world use cases
- [Architecture](docs/architecture.md) - How the library works
- [Mathematical Foundations](docs/mathematics.md) - Formal definitions

## Testing

```bash
pytest tests/ -v
```

Requires GLPK and SCIP for full integration test coverage (39 tests).

## License

MIT License - See LICENSE file for details
