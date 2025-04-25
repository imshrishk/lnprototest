# Running lnprototest on Windows

This project was primarily developed for Unix-like environments, but can be run on Windows with some adaptations. This guide provides instructions for setting up and running the tests on Windows systems.

## Prerequisites

- Python 3.9 or later
- PowerShell (recommended for Windows compatibility)
- Make (optional, but recommended)

## Setup

1. Install Python 3.9+ from [python.org](https://www.python.org/downloads/)
2. Install Poetry (for dependency management):
   ```
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```
3. Clone this repository and navigate to it
4. Install dependencies:
   ```
   poetry install
   ```

## Running Tests on Windows

You have several options for running the tests on Windows:

### Option 1: Run Make with Windows Makefile

If you have Make installed (e.g., from MinGW, Cygwin, or Git Bash), you can run:

```
make -f Makefile.windows check
```

Other available targets include:
- `make -f Makefile.windows fmt` - Format the code
- `make -f Makefile.windows check-source` - Run source checks
- `make -f Makefile.windows run-windows-tests` - Run only Windows-compatible tests

### Option 2: Direct Python Execution

You can bypass Make entirely and run tests directly with Python:

```
python direct_run_all_tests.py --windows
```

To run all tests (including those that might not be Windows-compatible):
```
python direct_run_all_tests.py --all
```

Or run pytest directly:
```
python -m pytest tests
```

## Windows-Compatible Tests

Some test files have Windows-specific versions (ending with `-windows.py`). The `--windows` flag for `direct_run_all_tests.py` will run only these files.

## Troubleshooting

### Common Issues

1. **Command Not Found Errors**:
   - Ensure Python is in your PATH
   - Try using `python -m <command>` format (e.g., `python -m pytest` instead of `pytest`)

2. **PowerShell Execution Policy**:
   - If you can't run PowerShell scripts, you may need to adjust your execution policy:
     ```
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

3. **Path Issues**:
   - Windows uses backslashes (`\`) in paths, while many scripts expect forward slashes (`/`)
   - Most Python libraries handle this automatically, but you may need to modify paths in custom scripts

4. **Finding Windows-Specific Files**:
   - Windows-compatible test files end with `-windows.py`
   - Windows-compatible Makefile is `Makefile.windows`

## Contributing

If you find Windows-specific issues or have improvements for Windows compatibility, please create a PR or issue on the repository. 