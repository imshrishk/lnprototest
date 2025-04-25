#!/usr/bin/env python3
"""
Script to run pytest with enhanced mock support for LDK runner.
This allows tests to run even without the actual LDK binary.
"""

import os
import sys
import subprocess
import argparse
import pytest
import pyln.spec.bolt1
import ldk_lnprototest

def main():
    parser = argparse.ArgumentParser(description="Run pytest with enhanced mock support")
    parser.add_argument("--test", "-t", default="tests", help="Test file or directory to run (default: tests)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Run with verbose output")
    parser.add_argument("--failfast", "-f", action="store_true", help="Stop on first failure")
    parser.add_argument("--listonly", "-l", action="store_true", help="List tests only, don't run them")
    
    args = parser.parse_args()
    
    # Construct pytest arguments
    pytest_args = []
    
    # Add options
    if args.verbose:
        pytest_args.extend(["-v", "--log-cli-level=info"])
    else:
        pytest_args.append("--log-cli-level=info")
    
    if args.failfast:
        pytest_args.append("-x")
    
    if args.listonly:
        pytest_args.append("--collect-only")
    
    # Always run with no-captured output so we can see the progress
    pytest_args.append("-s")
    
    # Add test target
    pytest_args.append(args.test)
    
    print(f"Running tests with: {' '.join(pytest_args)}")
    
    # Set environment variable to use LDK runner
    os.environ["PYTEST_RUNNER"] = "ldk_lnprototest.Runner"
    
    # Run pytest directly
    return pytest.main(pytest_args)

if __name__ == "__main__":
    sys.exit(main())
