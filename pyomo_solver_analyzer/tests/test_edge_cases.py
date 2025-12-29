"""
Unit tests for individual modules.
"""

import math

import pytest
from pyomo.environ import ConcreteModel, Constraint, Var

from pyomo_solver_analyzer.introspection import ConstraintIntrospector


class TestConstraintIntrospectorEdgeCases:
    """Test edge cases and error handling."""

    def test_nan_handling(self):
        """Test handling of NaN values."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x >= 0)

        # Don't set value - should get NaN
        introspector = ConstraintIntrospector(model)
        body_val = introspector.get_constraint_body_value(model.c)

        assert isinstance(body_val, float)

    def test_unbounded_constraints(self):
        """Test constraints without bounds."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x == 5)
        model.x.set_value(5)

        introspector = ConstraintIntrospector(model)
        lower, upper = introspector.get_constraint_bounds(model.c)

        assert lower == 0.0 or lower is not None
        assert upper == 0.0 or upper is not None

    def test_equality_constraint(self):
        """Test equality constraint handling."""
        model = ConcreteModel()
        model.x = Var()
        model.y = Var()
        model.c = Constraint(expr=model.x + model.y == 10)
        model.x.set_value(5)
        model.y.set_value(5)

        introspector = ConstraintIntrospector(model)
        slack = introspector.compute_slack(model.c)

        assert abs(slack - 0.0) < 1e-6

    def test_slack_zero(self):
        """Test handling of zero slack (binding constraint)."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x >= 5)
        model.x.set_value(5)

        introspector = ConstraintIntrospector(model)
        slack = introspector.compute_slack(model.c)

        assert abs(slack - 0.0) < 1e-6

    def test_large_slack(self):
        """Test handling of very large slack."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x >= 1)
        model.x.set_value(1e10)

        introspector = ConstraintIntrospector(model)
        slack = introspector.compute_slack(model.c)

        assert slack > 0
        assert not math.isnan(slack)


class TestConstraintAnalyzerEdgeCases:
    """Test edge cases for constraint analyzer."""

    def test_empty_model(self):
        """Test analyzer on model with no constraints."""
        model = ConcreteModel()
        model.x = Var()

        from pyomo_solver_analyzer.analyzer import ConstraintAnalyzer

        analyzer = ConstraintAnalyzer(model)

        analyses = analyzer.analyze_all_constraints()
        assert len(analyses) == 0

    def test_single_constraint(self):
        """Test analyzer with single constraint."""
        model = ConcreteModel()
        model.x = Var(bounds=(0, 10))
        model.c = Constraint(expr=model.x >= 5)
        model.x.set_value(7)

        from pyomo_solver_analyzer.analyzer import ConstraintAnalyzer

        analyzer = ConstraintAnalyzer(model)

        analyses = analyzer.analyze_all_constraints()
        assert len(analyses) == 1

    def test_dual_value_handling(self):
        """Test handling of missing dual values."""
        model = ConcreteModel()
        model.x = Var(bounds=(0, 10))
        model.c = Constraint(expr=model.x >= 5)
        model.x.set_value(7)

        # No dual suffix defined
        from pyomo_solver_analyzer.analyzer import ConstraintAnalyzer

        analyzer = ConstraintAnalyzer(model)

        analysis = analyzer.analyze_constraint(model.c)
        assert analysis.dual is None


class TestUnfeasibilityDetectorEdgeCases:
    """Test edge cases for unfeasibility detector."""

    def test_marginally_feasible(self):
        """Test constraint that is feasible but very tight."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x >= 5.0)
        model.x.set_value(5.0 + 1e-7)  # Just barely feasible

        from pyomo_solver_analyzer.unfeasibility import UnfeasibilityDetector

        detector = UnfeasibilityDetector(model, tolerance=1e-6)

        violation = detector.check_constraint_feasibility(model.c)
        assert violation is None

    def test_marginally_infeasible(self):
        """Test constraint that is infeasible by tiny amount."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x >= 5.0)
        model.x.set_value(5.0 - 1e-5)  # Barely infeasible

        from pyomo_solver_analyzer.unfeasibility import UnfeasibilityDetector

        detector = UnfeasibilityDetector(model, tolerance=1e-6)

        violation = detector.check_constraint_feasibility(model.c)
        assert violation is not None
        assert violation.violation_amount > 0

    def test_custom_severity_levels(self):
        """Test custom severity level configuration."""
        model = ConcreteModel()
        model.x = Var()
        model.c = Constraint(expr=model.x >= 10)
        model.x.set_value(0)

        from pyomo_solver_analyzer.unfeasibility import UnfeasibilityDetector

        custom_levels = {
            "critical": 1.0,
            "high": 0.1,
            "medium": 0.01,
            "low": 0.0,
        }
        detector = UnfeasibilityDetector(model, severity_levels=custom_levels)

        violations = detector.find_infeasible_constraints()
        assert len(violations) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
