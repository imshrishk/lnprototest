#!/usr/bin/env python3
"""
Simplified script to run tests with the LDK mock runner.
This bypasses the usual pytest command line issues.
"""

import os
import sys
import importlib
from lnprototest.utils.utils import run_runner
import ldk_lnprototest
import pyln.spec.bolt1
import pyln.proto.message
from lnprototest import Connect, ExpectMsg, Msg
from lnprototest.helpers import rcvd

# Get the test file name from command line
test_file = sys.argv[1] if len(sys.argv) > 1 else "test_bolt1-01-init-windows.py"
test_name = sys.argv[2] if len(sys.argv) > 2 else "test_namespace_override"

print(f"Running test: {test_file}::{test_name}")

# Create the LDK runner
runner = ldk_lnprototest.Runner(None)

# Load and run the test
try:
    # Import the test module
    if test_file.endswith(".py"):
        test_file = test_file[:-3]  # Remove .py extension
    test_module = importlib.import_module(test_file)
    
    # Get the test function
    test_func = getattr(test_module, test_name)
    
    # Check if the test function requires the namespaceoverride fixture
    if "namespaceoverride" in test_func.__code__.co_varnames:
        # Create a simple namespace override function
        def namespace_override(namespace):
            old_namespace = pyln.proto.message.MessageNamespace.default_msg_namespace
            pyln.proto.message.MessageNamespace.default_msg_namespace = namespace
            return old_namespace
        
        # Run the test with the namespace override
        test_func(runner, namespace_override)
    else:
        # Run the test directly
        test_func(runner)
    
    print(f"Test {test_name} passed!")
    sys.exit(0)
except Exception as e:
    print(f"Test {test_name} failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
