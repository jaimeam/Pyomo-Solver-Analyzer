"""
Pyomo Solver Analyzer - Constraint analysis and debugging for Pyomo models.

This package provides tools for analyzing linear solver results from Pyomo models,
with focus on:
- Constraint tightness analysis
- Feasibility diagnostics
- Sensitivity analysis
- Identification of limiting constraints
"""

from .src.analyzer import ConstraintAnalyzer
from .src.diagnostics import SolverDiagnostics
from .src.introspection import ConstraintIntrospector
from .src.unfeasibility import UnfeasibilityDetector

__version__ = "0.1.0"
__all__ = [
    "SolverDiagnostics",
    "ConstraintAnalyzer",
    "UnfeasibilityDetector",
    "ConstraintIntrospector",
]
