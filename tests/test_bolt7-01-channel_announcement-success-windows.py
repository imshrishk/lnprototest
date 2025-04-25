#! /usr/bin/env python3
# Simple gossip tests.

from lnprototest import (
    Connect,
    Block,
    ExpectMsg,
    Msg,
    RawMsg,
    Funding,
    Side,
    MustNotMsg,
    Disconnect,
    Runner,
)
from lnprototest.utils import tx_spendable, utxo
import time


def test_gossip_forget_channel_after_12_blocks(runner: Runner) -> None:
    # Make up a channel between nodes 02 and 03, using bitcoin privkeys 10 and 20
    funding, funding_tx = Funding.from_utxo(
        *utxo(0),
        local_node_privkey="02",
        local_funding_privkey="10",
        remote_node_privkey="03",
        remote_funding_privkey="20"
    )

    test = [
        Block(blockheight=102, txs=[tx_spendable]),
        Connect(connprivkey="03"),
        ExpectMsg("init"),
        Msg(
            "init",
            globalfeatures=runner.runner_features(globals=True),
            features=runner.runner_features(),
        ),
        Block(blockheight=103, number=6, txs=[funding_tx]),
        RawMsg(funding.channel_announcement("103x1x0", "")),
        # New peer connects, asking for initial_routing_sync.  We *won't* relay channel_announcement, as there is no
        # channel_update.
        Connect(connprivkey="05"),
        ExpectMsg("init"),
        Msg(
            "init",
            globalfeatures=runner.runner_features(globals=True),
            features=runner.runner_features(additional_features=[3]),
        ),
        MustNotMsg("channel_announcement"),
        Disconnect(),
        RawMsg(
            funding.channel_update(
                "103x1x0",
                Side.local,
                disable=False,
                cltv_expiry_delta=144,
                htlc_minimum_msat=0,
                fee_base_msat=1000,
                fee_proportional_millionths=10,
                timestamp=int(time.time()),
                htlc_maximum_msat=2000000,
            ),
            connprivkey="03",
        ),
        # Now we'll relay to a new peer.
        Connect(connprivkey="05"),
        ExpectMsg("init"),
        Msg(
            "init",
            globalfeatures=runner.runner_features(globals=True),
            features=runner.runner_features(additional_features=[3]),
        ),
        ExpectMsg("channel_announcement", short_channel_id="103x1x0"),
        ExpectMsg(
            "channel_update",
            short_channel_id="103x1x0",
            message_flags=1,
            channel_flags=0,
        ),
        Disconnect(),
        # BOLT #7:
        # - once its funding output has been spent OR reorganized out:
        #   - SHOULD forget a channel after a 12-block delay.
        Block(blockheight=109, number=13, txs=[funding.close_tx(200, "99")]),
        Connect(connprivkey="05"),
        ExpectMsg("init"),
        Msg(
            "init",
            globalfeatures=runner.runner_features(globals=True),
            features=runner.runner_features(additional_features=[3]),
        ),
        MustNotMsg("channel_announcement"),
        MustNotMsg("channel_update"),
    ]

    runner.run(test)
