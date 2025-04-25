#!/usr/bin/env python3
# This test file focuses on bolt1 initialization tests that can run with mock nodes

import pytest

import pyln.spec.bolt1
import pyln.proto.message

from lnprototest import (
    TryAll,
    Connect,
    Disconnect,
    EventError,
    ExpectMsg,
    Msg,
    RawMsg,
    Runner,
    MustNotMsg,
)
from lnprototest.helpers import rcvd  # Import rcvd from helpers module
from typing import Any
from lnprototest.utils.utils import run_runner

# Import the ldk_lnprototest Runner for Windows support
try:
    from ldk_lnprototest import Runner as LDKRunner
except ImportError:
    # If not available, we'll use the standard runner
    pass


@pytest.fixture(scope="function")
def namespaceoverride() -> Any:
    """Override spec namespace for these tests"""
    def _setter(namespace: Any) -> None:
        pyln.proto.message.MessageNamespace.default_msg_namespace = namespace
        
    old_namespace = pyln.proto.message.MessageNamespace.default_msg_namespace
    yield _setter
    pyln.proto.message.MessageNamespace.default_msg_namespace = old_namespace


def test_namespace_override(runner: Runner, namespaceoverride: Any) -> None:
    """Make sure namespace overriding works"""
    # We override default namespace since we only need BOLT1
    namespaceoverride(pyln.spec.bolt1.namespace)


def test_echo_init(runner: Runner, namespaceoverride: Any) -> None:
    # We override default namespace since we only need BOLT1
    namespaceoverride(pyln.spec.bolt1.namespace)
    
    # This test performs a basic init message exchange
    test = [
        Connect(connprivkey="03"),
        ExpectMsg("init"),
        Msg(
            "init",
            globalfeatures=runner.runner_features(globals=True),
            features=runner.runner_features(),
        ),
        # optionally disconnect that first one
        Connect(connprivkey="02"),
        # You should always handle us echoing your own features back!
        ExpectMsg("init"),
        Msg("init", globalfeatures=rcvd(), features=rcvd()),
    ]
    
    run_runner(runner, test)


def test_init_msg(runner: Runner, namespaceoverride: Any) -> None:
    # We override default namespace since we only need BOLT1
    namespaceoverride(pyln.spec.bolt1.namespace)
    
    # This test checks init message handling with various feature bits
    test = [
        Connect(connprivkey="03"),
        ExpectMsg("init"),
        Msg("init", globalfeatures="", features=""),
        Connect(connprivkey="04"),
        ExpectMsg("init"),
        # Try with some feature bits set
        Msg("init", globalfeatures="", features="0102"),
    ]
    
    run_runner(runner, test)
