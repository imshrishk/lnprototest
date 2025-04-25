#!/usr/bin/env python3
import sys
import os
import importlib
import types
import pytest
import glob
import argparse

def patch_runner_class():
    """Patch the Runner class for compatibility with all tests"""
    from lnprototest import Runner
    
    # Store original methods
    original_has_option = Runner.has_option
    original_has_feature = getattr(Runner, "has_feature", lambda self, option: None)
    original_has_modern_dual_funding = getattr(Runner, "has_modern_dual_funding", lambda self: False)
    original_has_plugin = getattr(Runner, "has_plugin", lambda self, plugin: False)
    
    # Patch has_option method for gossip tests
    def patched_has_option(self, option):
        if option == "option_gossip_queries":
            return "enabled"
        return original_has_option(self, option)
    
    # Patch has_feature method for dual funding tests
    def patched_has_feature(self, feature):
        if feature == "option_dual_fund":
            return "enabled"
        return original_has_feature(self, feature)
    
    # Patch has_modern_dual_funding method
    def patched_has_modern_dual_funding(self):
        return True
    
    # Patch has_plugin method
    def patched_has_plugin(self, plugin):
        if plugin == "multifundchannel":
            return True
        return original_has_plugin(self, plugin)
    
    # Apply patches
    Runner.has_option = patched_has_option
    Runner.has_feature = patched_has_feature
    Runner.has_modern_dual_funding = patched_has_modern_dual_funding
    Runner.has_plugin = patched_has_plugin
    
    print("Successfully patched Runner class for all tests")

def main():
    """Run specific test files or all tests with patched classes"""
    parser = argparse.ArgumentParser(description='Run tests with Windows compatibility patches')
    parser.add_argument('test_files', nargs='*', help='Specific test files to run (e.g., tests/test_bolt7*.py)')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--windows', action='store_true', help='Run only Windows-compatible tests')
    args = parser.parse_args()
    
    # First ensure the test directory is in the path
    sys.path.insert(0, os.getcwd())
    
    # Patch the Runner class
    patch_runner_class()
    
    # Determine which tests to run
    test_files = []
    
    if args.all:
        # Run all tests
        test_files = ["tests"]
    elif args.windows:
        # Run only Windows-compatible tests
        test_files = glob.glob("tests/*-windows.py")
    elif args.test_files:
        # Run specific tests
        test_files = args.test_files
    else:
        # Default: Run bolt7 tests
        test_files = glob.glob("tests/test_bolt7*.py")
    
    if not test_files:
        print("No test files found to run!")
        return 1
    
    # Run the tests
    print(f"\nRunning tests: {test_files}")
    return pytest.main(["-xvs"] + test_files)

if __name__ == "__main__":
    sys.exit(main())
