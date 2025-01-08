import pytest

def process_spend_bundle(spend_bundle_json):
    try:
        # Loop through coin spends
        for coin_spend in spend_bundle_json["coin_spends"]:
            coin_info = coin_spend["coin"]
            
            # Convert hexadecimal strings to bytes
            parent_coin_info = coin_info["parent_coin_info"][2:]  # Remove the '0x'
            puzzle_hash = coin_info["puzzle_hash"][2:]  # Remove the '0x'
            puzzle_reveal = coin_spend["puzzle_reveal"][2:]  # Remove the '0x'
            solution = coin_spend["solution"][2:]  # Remove the '0x'
            
            # Convert them from hex to bytes
            parent_coin_info_bytes = bytes.fromhex(parent_coin_info)
            puzzle_hash_bytes = bytes.fromhex(puzzle_hash)
            puzzle_reveal_bytes = bytes.fromhex(puzzle_reveal)
            solution_bytes = bytes.fromhex(solution)
            
            # For aggregated signature
            aggregated_signature = spend_bundle_json["aggregated_signature"][2:]  # Remove '0x'
            aggregated_signature_bytes = bytes.fromhex(aggregated_signature)
            
            # Print results or do further processing
            print(f"Parent Coin Info: {parent_coin_info_bytes}")
            print(f"Puzzle Hash: {puzzle_hash_bytes}")
            print(f"Puzzle Reveal: {puzzle_reveal_bytes}")
            print(f"Solution: {solution_bytes}")
            print(f"Aggregated Signature: {aggregated_signature_bytes}")
            
    except ValueError as e:
        print(f"Error while processing spend bundle: {e}")

# Example usage
spend_bundle_json = {
    "coin_spends": [
        {
            "coin": {
                "parent_coin_info": "0x27ae41e4649b934ca495991b7852b85500000000000000000000000000000001",
                "puzzle_hash": "0x6ade68fd907f830073ea335d2e47340d05ae5d6f6c08096112bc717bb5ca48a3",
                "amount": 250000000000
            },
            "puzzle_reveal": "0xff03ffff018466616b65ff01ff8080",
            "solution": "0xffa074d42ddc2e8fe2fdb21bdb402564ec412bec69ac3c3eb53a4da594aea81717aa80"
        }
    ],
    "aggregated_signature": "0xc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
}

# Run this in pytest as a normal function, no async needed
def test_sb() -> None:
    print("Test is running")
    sb = process_spend_bundle(spend_bundle_json)
    breakpoint()