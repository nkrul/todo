# Contributing to Natural Language Todo App

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- No harassment or discrimination

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check if the issue already exists.

When reporting a bug, include:
- Clear and descriptive title
- Detailed description of the behavior
- Steps to reproduce the problem
- Expected behavior vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

When suggesting an enhancement, include:
- Clear and descriptive title
- Detailed description of the suggested enhancement
- Why this enhancement would be useful
- Possible implementation approaches

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write or update tests as needed
5. Run tests: `pytest tests/ -v`
6. Run code quality checks: `make lint`
7. Format code: `make format`
8. Commit with clear messages: `git commit -m 'Add feature: description'`
9. Push to your fork: `git push origin feature/your-feature-name`
10. Open a Pull Request

### PR Guidelines

- Reference any related issues: `Fixes #123`
- Describe the changes and why
- Include tests for new functionality
- Update documentation if needed
- Ensure all tests pass
- Keep commits clean and logical

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (on Windows: `venv\Scripts\activate`)
4. Install dev dependencies: `pip install -r requirements-dev.txt`
5. Run tests: `pytest tests/`

## Code Style

We follow PEP 8 and use:
- **black** for code formatting (line length: 100)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Format your code before submitting:
```bash
make format
```

Run checks:
```bash
make lint
make type-check
```

## Testing

- Write tests for new features
- Write tests for bug fixes
- Maintain or improve code coverage
- Run tests before submitting PR

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=todo_core --cov-report=html
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update this file if contribution process changes
- Include examples for new features

## Git Commit Messages

- Use imperative mood ("Add feature" not "Added feature")
- Reference issues and PRs: "Fix #123", "Closes #456"
- Limit first line to 72 characters
- Separate subject from body with blank line
- Wrap body at 72 characters

Example:
```
Add natural language parsing for recurring tasks

- Parse "every day", "weekly", "monthly" patterns
- Calculate next occurrence automatically
- Store recurrence rule in TodoItem

Fixes #123
```

## Areas for Contribution

- **Core Parser**: Improve natural language understanding
- **Web UI**: Enhance Streamlit interface
- **Mobile UI**: Improve Kivy interface
- **Tests**: Increase coverage
- **Documentation**: Improve clarity and examples
- **Performance**: Optimize algorithms
- **Accessibility**: Make UI more accessible
- **Internationalization**: Add language support

## Questions?

Open an issue with your question or reach out to the maintainers.

---

Thank you for contributing! 🎉
