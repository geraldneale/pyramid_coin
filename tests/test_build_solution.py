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
        #FAKE_ACS: Program = Program.to([3, (1, "fake"), 1, None])
        #FAKE_ACS_PH = FAKE_ACS.get_tree_hash()
        SEED: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  129,
                         19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
                         12, 62, 89, 110, 182, 9,   44, 20,  254, 22])
        SK: PrivateKey = AugSchemeMPL.key_gen(SEED)
        print("Private key: {}".format( SK))
        PUBLIC_KEY: G1Element = SK.get_g1()
        print("Public key: {}".format(PUBLIC_KEY))
        FAKE_PUBLIC_KEY = PUBLIC_KEY
        PC_CLSP = "pyramid_coin.clsp"
        PC_MOD = load_clvm(PC_CLSP, package_or_requirement="chialisp").curry(FAKE_PUBLIC_KEY)
        PC = SerializedProgram.to(PC_MOD)
        PC_type = type(PC)  # This should output: <class 'builtins.Program'>
        PC_PH = PC.get_tree_hash()
        await sim.farm_block(puzzle_hash=PC_PH)
        coin_records = await client.get_coin_records_by_puzzle_hash(PC_PH)
        coin = coin_records[0].coin
        #solution building starts here
        puzzle_hashes = [
        "74d42ddc2e8fe2fdb21bdb402564ec412bec69ac3c3eb53a4da594aea81717ac",
        "02df5fa6dab7320eef167ed242dc22c7b37d5cb3cf622720d95ee4b616c35a38",
        "5265c0f7fd37c2e42f99e93b389c8cb536aaa7a207bb0003429be2d1ae960fd5",
        "873c0b21c059291e316cea5b8a41a9eca7e263d2f230c2eccbd86b0062bf18b7",
        "35b17f6402acb8073154b7b0994de1ed463301cb8b6c310ad3ffda36a93840e5",
        "dd9d9594f335dc17f606677988eff97b1c51d09490f4715527c4b41786daeb75",
        "65f410973a6457d82dc5f4b295c1c7816f8628d450cd6acd4e4b586f36db90c9",
        "2748818182c0c06341479a29b316924705ff0ea497f232db879278cb40712b2e",
        "a6dcac1ce83905cb08265db87f7ae9ca686685f8f5f95b39d5b2415e8db95f1f",
        "a6dcac1ce83905cb08265db87f7ae9ca686685f8f5f95b39d5b2415e8db95f1f",
        "1b147fd24462187b4346288cd7348f148fdae36aefb3225a4bbc213b9bb7ae87",
        "a6dcac1ce83905cb08265db87f7ae9ca686685f8f5f95b39d5b2415e8db95f1f",
        "e85607223493688fb109922c751f82c5d4d4c0e8c071fba11351cf8c0d57275b",
        "3fd068c050826aa6d26a1f14a8f5dbc2c67b5965076c7545258b5b3d23d861a4",
        "7aef5c0deb1b90bdde6de76b1619be4ff31340b5a7eb699cad89f8660740d97b"
        ]
        phs = []
        for ph in puzzle_hashes:
            phs.append(bytes.fromhex(ph))
        print("Puzzle Hashes: {}".format(phs))
        #breakpoint()
        MEMO = "PC_TEST-GW"
        PC_FEE = 100 
        PAYOUT_AMOUNT = coin.amount - PC_FEE     
        SOLUTION = SerializedProgram.to([MEMO,phs,PAYOUT_AMOUNT,PC_FEE])
        OLD_PC:Program = PC_MOD
        OLD_SOLUTION:Program = Program.to([MEMO,phs,PAYOUT_AMOUNT,PC_FEE])
        cds = OLD_PC.run(OLD_SOLUTION) #conditions AttributeError: 'builtins.Program' object has no attribute 'run' fix_later gdn 20241227
        coin_spend = CoinSpend(coin, PC, SOLUTION)
        ADD_DATA = DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
        message = Program.to([MEMO, phs,PAYOUT_AMOUNT,PC_FEE]).get_tree_hash()
        sig = AugSchemeMPL.sign(SK, message + coin.name() + ADD_DATA)
        ver = AugSchemeMPL.verify(FAKE_PUBLIC_KEY, message +coin.name() + ADD_DATA, sig) 
        spend_bundle = SpendBundle([coin_spend],sig)
        pusht_sb = await client.push_tx(spend_bundle) 
        await sim.farm_block()
        new_coin = await client.get_coin_records_by_puzzle_hash(phs[0])
        #new_coin1 = await client.get_coin_records_by_puzzle_hash(puzzle_hashes[1])
        new_coins = []
        for ph in phs:
            new_coins.append(await client.get_coin_records_by_puzzle_hash(ph))      
    breakpoint()