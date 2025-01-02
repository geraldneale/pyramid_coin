from __future__ import annotations

import itertools
from typing import List, Optional, Tuple

import pytest
from chia_rs import AugSchemeMPL, G2Element, G1Element, PrivateKey
#from blspy import AugSchemeMPL, G2Element, G1Element, PrivateKey #keep until settled where to find these in current chia imports
from chia.clvm.spend_sim import CostLogger, sim_and_client
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.serialized_program import SerializedProgram
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.mempool_inclusion_status import MempoolInclusionStatus
from chia.types.spend_bundle import SpendBundle
from chia.util.errors import Err
from chia.util.hash import std_hash
from chia.util.ints import uint32, uint64
from chia.wallet.lineage_proof import LineageProof
from chia.wallet.payment import Payment
from chia.wallet.puzzles.singleton_top_layer_v1_1 import (
    launch_conditions_and_coinsol,
    puzzle_for_singleton,
    solution_for_singleton,
)
from chia.wallet.uncurried_puzzle import uncurry_puzzle
from chia.wallet.puzzles.load_clvm import load_clvm, load_clvm_maybe_recompile
from secrets import token_bytes
from chia.consensus.default_constants import DEFAULT_CONSTANTS

@pytest.mark.asyncio
async def test_pc() -> None:
    async with sim_and_client() as (sim, client):
        SEED: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  129,
                             19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
                             12, 62, 89, 110, 182, 9,   44, 20,  254, 22])
        SK: PrivateKey = AugSchemeMPL.key_gen(SEED)
        print("Private key:", SK)
        PUBLIC_KEY: G1Element = SK.get_g1()
        print("Public key:", PUBLIC_KEY)

        FAKE_PUBLIC_KEY = PUBLIC_KEY
        PC_CLSP = "pyramid_coin.clsp"
        PC_MOD = load_clvm(PC_CLSP, package_or_requirement="chialisp").curry(FAKE_PUBLIC_KEY)
        PC = SerializedProgram.to(PC_MOD)
        PC_type = type(PC)  # Output: <class 'builtins.Program'>
        print("Program type:", PC_type)

        PC_PH = PC.get_tree_hash()
        await sim.farm_block(puzzle_hash=PC_PH)
        coin_records = await client.get_coin_records_by_puzzle_hash(PC_PH)
        coin = coin_records[0].coin
        puzzle_hashes = [token_bytes(32) for _ in range(100)]

        MEMO = "PC_TEST-GW"
        PC_FEE = 100 
        PAYOUT_AMOUNT = coin.amount - PC_FEE     
        SOLUTION = SerializedProgram.to([MEMO, puzzle_hashes, PAYOUT_AMOUNT, PC_FEE])

        # Coin spend
        coin_spend = CoinSpend(coin, PC, SOLUTION)
        ADD_DATA = DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
        message = Program.to([MEMO, puzzle_hashes, PAYOUT_AMOUNT, PC_FEE]).get_tree_hash()

        # Debugging the message and signature
        print(f"Message (tree hash) for signing: {message}")
        print(f"Coin name: {coin.name()}")
        print(f"Additional data: {ADD_DATA}")
        print(f"Message to be signed: {message + coin.name() + ADD_DATA}")

        # Signature generation
        sig = AugSchemeMPL.sign(SK, message + coin.name() + ADD_DATA)
        print(f"Generated signature: {sig}")

        # Signature verification
        try:
            ver = AugSchemeMPL.verify(FAKE_PUBLIC_KEY, message + coin.name()+ ADD_DATA, sig)
            print(f"Signature verification result: {ver}")
            if ver:
                print("Verification succeeded.")
            else:
                print("Verification failed.")
        except Exception as e:
            print(f"Verification failed: {e}")
            return

        spend_bundle = SpendBundle([coin_spend], sig)
        pusht_sb = await client.push_tx(spend_bundle)
        await sim.farm_block()

        # Fetch new coins
        new_coins = []    
        for ph in puzzle_hashes:
            new_coins.append(await client.get_coin_records_by_puzzle_hash(ph))
    # Add breakpoint for inspection
    breakpoint()     
        
        
