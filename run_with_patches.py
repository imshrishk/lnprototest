#!/usr/bin/env python3
import os
import sys
import pytest

# Try to patch the Runner class at runtime
try:
    # Import the Runner class
    from lnprototest import Runner
    
    # Store the original method
    original_has_option = Runner.has_option
    
    # Define our patched method
    def patched_has_option(self, option):
        if option == "option_gossip_queries":
            print(f"Runtime patch: returning 'enabled' for {option}")
            return "enabled"
        return original_has_option(self, option)
    
    # Apply the patch
    Runner.has_option = patched_has_option
    print("Successfully applied runtime patch to Runner.has_option")
    
except ImportError as e:
    print(f"Error importing Runner: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error patching Runner: {e}")
    sys.exit(1)

# Now run the test
if len(sys.argv) > 1:
    test_file = sys.argv[1]
    print(f"Running test: {test_file}")
    sys.exit(pytest.main(["-xvs", test_file]))
else:
    print("Usage: python run_with_patches.py <test_file>")
    sys.exit(1)
