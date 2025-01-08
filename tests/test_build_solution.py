import json
import pytest
from chia_rs import AugSchemeMPL, G2Element, G1Element, PrivateKey

from chia.clvm.spend_sim import CostLogger, sim_and_client
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.serialized_program import SerializedProgram
from chia.types.coin_spend import CoinSpend
from chia.types.spend_bundle import SpendBundle
from chia.wallet.puzzles.load_clvm import load_clvm, load_clvm_maybe_recompile
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.sized_bytes import bytes32

def fromhex(s):
    if s.lower().startswith("0x"):
        s = s[2:]
    if len(s) & 1 == 1:
        s = f"0{s}"
    return bytes.fromhex(s)


@pytest.mark.asyncio
async def test_build_solution() -> None:
    async with sim_and_client() as (sim, client):
        FAKE_ACS: Program = Program.to([3, (1, "fake"), 1, None])
#        PC_MOD = load_clvm(FAKE_ACS, package_or_requirement="chialisp")
        PC: SerializedProgram = SerializedProgram.to(FAKE_ACS)
        PC_TYPE = type(PC)  # This should output: <class 'builtins.Program'>
        PC_PH = PC.get_tree_hash()
        await sim.farm_block(puzzle_hash=PC_PH)
        coin_records = await client.get_coin_records_by_puzzle_hash(PC_PH)
        coin = coin_records[0].coin
#        holders_file = "holders.txt" #eventually get the phs from a file, but not at first 20250101
        puzzle_hashes = [
        0x74d42ddc2e8fe2fdb21bdb402564ec412bec69ac3c3eb53a4da594aea81717ac,
        0x02df5fa6dab7320eef167ed242dc22c7b37d5cb3cf622720d95ee4b616c35a38,
        0x5265c0f7fd37c2e42f99e93b389c8cb536aaa7a207bb0003429be2d1ae960fd5,
        0x873c0b21c059291e316cea5b8a41a9eca7e263d2f230c2eccbd86b0062bf18b7,
        0x35b17f6402acb8073154b7b0994de1ed463301cb8b6c310ad3ffda36a93840e5,
        0xdd9d9594f335dc17f606677988eff97b1c51d09490f4715527c4b41786daeb75,
        0x65f410973a6457d82dc5f4b295c1c7816f8628d450cd6acd4e4b586f36db90c9,
        0x2748818182c0c06341479a29b316924705ff0ea497f232db879278cb40712b2e,
        0xa6dcac1ce83905cb08265db87f7ae9ca686685f8f5f95b39d5b2415e8db95f1f,
        0xa6dcac1ce83905cb08265db87f7ae9ca686685f8f5f95b39d5b2415e8db95f1f,
        0x1b147fd24462187b4346288cd7348f148fdae36aefb3225a4bbc213b9bb7ae87,
        0xa6dcac1ce83905cb08265db87f7ae9ca686685f8f5f95b39d5b2415e8db95f1f,
        0xe85607223493688fb109922c751f82c5d4d4c0e8c071fba11351cf8c0d57275b,
        0x3fd068c050826aa6d26a1f14a8f5dbc2c67b5965076c7545258b5b3d23d861a4,
        0x7aef5c0deb1b90bdde6de76b1619be4ff31340b5a7eb699cad89f8660740d97b
        ]
        puzzle_hashes2 : bytes = bytes.fromhex("74d42ddc2e8fe2fdb21bdb402564ec412bec69ac3c3eb53a4da594aea81717aa")
        SOLUTION = SerializedProgram.to([[51, puzzle_hashes2, 100]])
        SOLUTION_TYPE = type(SOLUTION)  # This should output: <class 'builtins.Program'>
        OLD_PC:Program = FAKE_ACS #old format for run
        OLD_SOLUTION:Program = Program.to([[]])
        cds = OLD_PC.run(OLD_SOLUTION) 
        coin_spend = CoinSpend(coin, PC, SOLUTION)
        sig: G2Element = G2Element()
        spend_bundle = SpendBundle([coin_spend],sig)
        json_string=spend_bundle.to_json_dict()    
        #for reference only
        with open('spend_bundle.json', 'w') as spend_bundle_file:
                json.dump(json_string, spend_bundle_file, indent=4)
        spend_bundle_file.close() 
        pusht_sb = await client.push_tx(spend_bundle) 
        breakpoint()
        await sim.farm_block()
        breakpoint()
#        new_coin = await client.get_coin_records_by_puzzle_hash(puzzle_hashes[0])
#        new_coin1 = await client.get_coin_records_by_puzzle_hash(puzzle_hashes[1])
#        new_coins = []
#        for ph in puzzle_hashes:
#            new_coins.append(await client.get_coin_records_by_puzzle_hash(ph))      
        
