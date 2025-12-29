# Development Guide

## Getting Started with Development

### Setup Development Environment

```bash
# Clone the repository
cd pyomo_solver_analyzer

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from pyomo_solver_analyzer import SolverDiagnostics; print('OK')"
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v

# Run specific test class
pytest tests/test_analyzer.py::TestConstraintIntrospector -v

# Run specific test
pytest tests/test_analyzer.py::TestConstraintIntrospector::test_constraint_body_value -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/ --max-line-length=88

# Type checking
mypy src/ --ignore-missing-imports
```

### Building Documentation

```bash
# Documentation is in markdown in docs/ folder
# View directly or convert with pandoc if needed
```

## Project Structure

```
pyomo_solver_analyzer/
├── src/
│   ├── __init__.py           # Package exports
│   ├── introspection.py      # Low-level constraint evaluation
│   ├── analyzer.py           # Constraint tightness analysis
│   ├── unfeasibility.py      # Infeasibility detection
│   └── diagnostics.py        # High-level unified API
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py      # Comprehensive tests
│   └── test_edge_cases.py    # Edge case tests
├── docs/
│   ├── architecture.md       # System design and architecture
│   ├── mathematics.md        # Mathematical foundations
│   ├── api_reference.md      # API documentation
│   ├── examples.md           # Usage examples
│   └── DEVELOPMENT.md        # This file
├── README.md                 # Package overview
├── setup.py                  # Setup script
├── pyproject.toml            # Project configuration
└── pytest.ini                # Pytest configuration
```

## Adding New Features

### Adding a New Analysis Metric

1. Add computation method to `ConstraintIntrospector`:
   ```python
   def compute_new_metric(self, constraint):
       """Compute new metric for constraint."""
       # Implementation
       return result
   ```

2. Use in `ConstraintAnalyzer`:
   ```python
   def analyze_constraint(self, constraint):
       # ... existing code ...
       new_metric = self.introspector.compute_new_metric(constraint)
       # Add to ConstraintTightness or create new dataclass
   ```

3. Expose through `SolverDiagnostics`:
   ```python
   def get_constraints_by_new_metric(self):
       # Use analyzer to compute and return results
   ```

4. Add tests in `tests/test_analyzer.py`

### Adding a New Detection Type

Similar process for `UnfeasibilityDetector`:

1. Add detection method to detector class
2. Expose through `SolverDiagnostics`
3. Update `DiagnosticsReport` if needed
4. Add comprehensive tests

## Testing Guidelines

### Test Organization

- `test_analyzer.py`: All tests for core functionality
- `test_edge_cases.py`: Edge cases, error handling, numerical edge cases
- Use fixtures for common test models

### Writing Good Tests

```python
class TestFeatureName:
    """Test suite for FeatureName."""
    
    @pytest.fixture
    def test_model(self):
        """Create test fixture."""
        model = ConcreteModel()
        # ... setup ...
        return model
    
    def test_specific_behavior(self, test_model):
        """Test specific behavior with clear assertion."""
        # Setup
        component = ClassToTest(test_model)
        
        # Action
        result = component.method()
        
        # Assert
        assert result == expected_value
        assert other_property_holds
```

### Coverage Goals

- Aim for >90% line coverage on core modules
- 100% coverage on public API methods
- Include negative test cases

## Common Issues and Solutions

### Issue: Import errors when running tests

**Solution**: Ensure you've installed in development mode:
```bash
pip install -e .
```

Or add src to PYTHONPATH:
```bash
export PYTHONPATH=/path/to/pyomo_solver_analyzer/src:$PYTHONPATH
```

### Issue: Solver not found in tests

**Solution**: Tests skip gracefully when solvers unavailable:
```python
try:
    SolverFactory('solver_name')
except:
    pytest.skip("Solver not available")
```

### Issue: NaN values in computations

**Solution**: Check for NaN using `math.isnan()`:
```python
if math.isnan(value):
    handle_nan_case()
else:
    process_value()
```

## Performance Optimization

### Current Performance Characteristics

- Single constraint analysis: O(1)
- All constraints analysis: O(n) where n = number of constraints
- Expression decomposition: O(n_terms) where n_terms = terms in expression

### Potential Optimizations

1. **Caching**: Store computed metrics in `_cache` dict
2. **Lazy evaluation**: Don't compute duals if not requested
3. **Vectorization**: Use NumPy for large-scale analysis

## Future Enhancements

Potential features for future versions:

1. **Sensitivity Analysis**: RHS coefficient ranges
2. **IIS Detection**: Irreducible Infeasible Sets (solver-specific)
3. **Warm-Start Support**: Analyzing incremental changes
4. **Parallel Analysis**: Multi-threaded constraint evaluation
5. **Advanced Metrics**: Entropy, correlation analysis
6. **Visualization**: Constraint tightness plots
7. **Export Formats**: JSON, CSV reports

## Contributing

When contributing:

1. Create a feature branch
2. Add tests for new functionality
3. Ensure all tests pass: `pytest tests/`
4. Ensure code quality: `black` and `flake8`
5. Update documentation
6. Submit pull request with clear description

## Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version bumped in setup.py and __init__.py
- [ ] CHANGELOG updated
- [ ] Examples tested and working
- [ ] Code reviewed
- [ ] Commit and tag release
- [ ] Build distribution: `python setup.py sdist bdist_wheel`
- [ ] Upload to PyPI: `twine upload dist/*`
