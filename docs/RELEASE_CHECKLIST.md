# Release Checklist

## Pre-Release Validation

### Code Quality
- [ ] Tests pass: `python -m pytest`
- [ ] Code formatted and linted
- [ ] Documentation updated

### Package Configuration
- [ ] Unique package name verified on PyPI
- [ ] Version updated in `setup.py` and `pyproject.toml`
- [ ] Author/maintainer information correct
- [ ] Dependencies specified correctly
- [ ] License attribution complete

### Repository
- [ ] Changes committed and pushed
- [ ] Repository URLs updated in configuration files

### Build Verification
- [ ] Clean build: `python -m build`
- [ ] Package validation: `python -m twine check dist/*`
- [ ] Local installation test: `pip install dist/*.whl`
- [ ] Import functionality verified

## Release Process

### Test Release
```bash
pip install build twine
python publish.py --test
pip install --index-url https://test.pypi.org/simple/ pyqttoast-enhanced
```

### Production Release
```bash
python publish.py
pip install pyqttoast-enhanced
```

### Post-Release
- [ ] Create GitHub release with version tag
- [ ] Update documentation as needed

## Commands Reference

```bash
# Build package
python -m build

# Validate package
python -m twine check dist/*

# Check package contents
python -m tarfile -l dist/*.tar.gz

# Development install
pip install -e .
```
