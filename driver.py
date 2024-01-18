import requests
import asyncio
from chia.types.spend_bundle import SpendBundle
from chia.types.coin_spend import CoinSpend
from blspy import AugSchemeMPL, G2Element, G1Element, PrivateKey
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.wallet.puzzles.load_clvm import load_clvm
from chia.util.bech32m import encode_puzzle_hash
import json
from chia.rpc.full_node_rpc_client import FullNodeRpcClient

AMOUNT_IN_MOJOS =   1000000000 #1 000 000 000 = 1 Majuju or .03 $USD
FEE_IN_MOJOS_SPEND = 200000000 #pc spend. typically higher. don't want it to get stuck.
FEE_IN_MOJOS_SEND =  70000000 # 70 Jujus Initial standard tx. typically lower
MEMO = "<your memo here>"
FINGERPRINT = "<your fingerprint here>"
PC_CLSP = "pyramid_coin.clsp"
HOME_PATH = "/<your path here>" 
ENVIRONMENT = "mainnet" #choices are "mainnet", "testnet", or "simulator"
config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
self_hostname = config["self_hostname"] # localhost
full_node_rpc_port = config["full_node"]["rpc_port"]
wallet_rpc_port = config["wallet"]["rpc_port"]
file_list = open("XCH_address_list.txt").readlines()
XCH_ADDRESS_LIST = []
for puzzlehash in file_list:
    puzzlehash = puzzlehash.replace("\n","")
    puzzlehash = bytes.fromhex(puzzlehash)
    XCH_ADDRESS_LIST.append(puzzlehash)

if ENVIRONMENT == "simulator":
    CHIA_ENV = "simulator"
    ADD_DATA = bytes.fromhex("abc123ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce")  #genesis challenge(works for simulator) #find out the value later 20240114
    CHAIN_PREFIX = "txch"
elif ENVIRONMENT == "testnet":
    CHIA_ENV = "testnet11"
    ADD_DATA = bytes.fromhex("37a90eb5185a9c4439a91ddc98bbadce7b4feba060d50116a067de66bf236615")  #genesis challenge 
    CHAIN_PREFIX = "txch"
else:
    CHIA_ENV = "mainnet"
    ADD_DATA = bytes.fromhex("ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb") #genesis challenge(works for mainnet)
    CHAIN_PREFIX = "xch"   
#overide for my dumb setup gneale 20240114
CHIA_ENV = "testnet10"
CERT = ('{}/.chia/{}/config/ssl/full_node/private_full_node.crt'.format(HOME_PATH,CHIA_ENV), '{}/.chia/{}/config/ssl/full_node/private_full_node.key'.format(HOME_PATH,CHIA_ENV))
HEADERS = {'Content-Type': 'application/json'}  

def pc_puzzlehash():
    mod = load_clvm(PC_CLSP, package_or_requirement=__name__).curry(MEMO)
    treehash = mod.get_tree_hash()
    return treehash

def pc_xch_adress():  
    treehash = pc_puzzlehash()
    pc_xch_address = encode_puzzle_hash(treehash, CHAIN_PREFIX)
    return pc_xch_address 

def solution_pc():
    dispersion_quantity = AMOUNT_IN_MOJOS - FEE_IN_MOJOS_SPEND
    return Program.to([XCH_ADDRESS_LIST, dispersion_quantity, FEE_IN_MOJOS_SPEND])

async def get_coin_async(coinid: str):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_record = await full_node_client.get_coin_record_by_name(bytes32.fromhex(coinid))
        return coin_record.coin
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

def get_pc_coin(coinid: str):
    return asyncio.run(get_coin_async(coinid))

def create_sig():
    return G2Element()     #empty signature

#using Wallet RPC port 9256 # to update to send_transaction in the future gneale 20240117 https://github.com/Chia-Network/chia-blockchain/blob/71c8223f02ccebe3a3a73b26b085894122457e90/tests/wallet/rpc/test_wallet_rpc.py#L289
def send_xch_rpc(amount: int, target_address: str, fee: int, memo: str):    
    url = "https://localhost:9256/send_transaction"
    data = {"fingerprint": FINGERPRINT,"wallet_id": 1, "address": target_address, "amount": amount, "fee": fee, "memos":[memo]} 
    print(data) 
    response = json.loads(requests.post(url, json=data, headers=HEADERS, cert=CERT, verify=False).text)
    print(response)
    json_str = json.dumps(response, indent=4, sort_keys=True)
    mempool_items = json.loads(json_str)
    return mempool_items

async def find_spendable_pc_async(puzzlehash: bytes32):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_records = await full_node_client.get_coin_records_by_puzzle_hash(puzzlehash,include_spent_coins = False,start_height = 4791939) #arbitrary starting point to theoretically speed things up
        print("Looking for a spendable pyramid coin...")
        for coin_record in coin_records:
            if coin_record.coin.amount == AMOUNT_IN_MOJOS:
                return coin_record.coin #CoinRecord references coin object
        await asyncio.sleep(10)
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

def find_spendable_pc(puzzlehash: str):
    return asyncio.run(find_spendable_pc_async(puzzlehash))

def create_spendbundle(pc: Coin):
    pc_spend = CoinSpend(
        pc,
        load_clvm(PC_CLSP, package_or_requirement=__name__).curry(MEMO),
        solution_pc()
    )
    spend_bundle = SpendBundle(
            # coin spend(s)
            [
                pc_spend
            ],
            # aggregated_signature
            create_sig(),
        )
    json_string=spend_bundle.to_json_dict()
    with open('spend_bundle.json', 'w') as spend_bundle_file:
        json.dump(json_string, spend_bundle_file, indent=4)
    spend_bundle_file.close()     
    return spend_bundle

def ready_verification(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] in ['y','Y']:
            return True
        else:
            break
        
async def push_tx_async(spend_bundle: SpendBundle):
    try:
        # create a full node client
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        print("Fees: {}".format(FEE_IN_MOJOS_SPEND))    
        status = await full_node_client.push_tx(spend_bundle)
        return status
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

def push_tx(spend_bundle: SpendBundle):
    return asyncio.run(push_tx_async(spend_bundle))

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))        

if __name__=='__main__':
    pc_confirmed = False
    wallet_ready = ready_verification("Are you sure wallet fingerprint {} is synced and ready?".format(FINGERPRINT))
    if wallet_ready:
        create_pc_ready = ready_verification("Would you like to create a pyramid coin?")
        if create_pc_ready:
            send_xch_rpc(AMOUNT_IN_MOJOS,pc_xch_adress(),FEE_IN_MOJOS_SEND,MEMO)
        counter = 0    
        while True:
            if counter < 50:
                pc_confirmed: Coin = find_spendable_pc(pc_puzzlehash())
                if pc_confirmed:
                    break
                else:          
                    counter += 1
            else:
                break

    if pc_confirmed:
        print("Unspent Pyramid Coin found onchain: {}".format(pc_confirmed))
        pc_ready = ready_verification("Would you like to spend it?")
        if pc_ready:                                            
            spend_bundle = create_spendbundle(pc_confirmed)
            status = push_tx(spend_bundle)
            print_json(status)
    else:
        print("End Program.")
