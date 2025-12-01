# Contributing Guide

Thank you for your interest in the HydroSEBench project! We welcome contributions of all kinds.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature suggestion, please submit it through:

1. Create a new issue on GitHub Issues
2. Provide a detailed description of the problem or suggestion
3. If possible, provide reproduction steps or example code

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make changes and commit**
   - Ensure code follows project conventions
   - Add necessary tests (if applicable)
   - Update relevant documentation
4. **Push to your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request**
   - Create a Pull Request on GitHub
   - Provide a detailed description of your changes and reasons

## Code Standards

- Follow PEP 8 Python code style guidelines
- Use meaningful variable and function names
- Add necessary docstrings
- Keep code concise and readable

## Development Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sheishijun/Hydro-SE-Bench.git
   cd hydrosebench
   ```

2. **Install development dependencies**
   ```bash
   cd hydrosebench-eval
   pip install -e ".[all]"
   ```

3. **Run example code**
   ```bash
   cd ../examples
   python example_1_basic_evaluation.py
   ```

## Testing

Before submitting code, please ensure:

- Code runs correctly
- Example code executes successfully
- No new errors or warnings are introduced

## Documentation

If you modify features or add new features, please:

- Update relevant README.md files
- Update example code (if needed)
- Update CHANGELOG.md

## Questions and Feedback

If you encounter any issues during contribution, please feel free to ask questions in Issues.

Thank you again for your contribution!
