import pytest
from blspy import PrivateKey, AugSchemeMPL, G2Element


# Helper function to generate keys
def generate_key_pair(seed: bytes) -> tuple[PrivateKey, bytes]:
    """Generates a private and public key pair from a given seed."""
    private_key = AugSchemeMPL.key_gen(seed)
    public_key = private_key.get_g1()
    return private_key, public_key


# Helper function to sign a message
def sign_message(private_key: PrivateKey, message: bytes) -> bytes:
    """Signs a message with the given private key."""
    return AugSchemeMPL.sign(private_key, message)


# Helper function to verify a signature
def verify_signature(public_key: bytes, message: bytes, signature: bytes) -> bool:
    """Verifies the signature for a message using the public key."""
    return AugSchemeMPL.verify(public_key, message, signature)


@pytest.mark.asyncio
async def test_signature_verification() -> None:
    """Test the key generation, signing, and signature verification process."""
    
    # Step 1: Define the seed and generate key pair
    SEED: bytes = bytes([0, 50, 6, 244, 24, 199, 1, 25, 52, 88, 129,
                         19, 18, 12, 89, 6, 220, 18, 102, 58, 209, 82,
                         12, 62, 89, 110, 182, 9, 44, 20, 254, 22])
    
    private_key, public_key = generate_key_pair(SEED)

    # Step 2: Define the message
    message = b"hello world"

    # Step 3: Sign the message
    signature = sign_message(private_key, message)

    # Step 4: Verify the signature
    is_valid = verify_signature(public_key, message, signature)
    
    # Assert that the signature is valid
    assert is_valid, "Signature verification failed for the correct message."

    # Step 5: Tampering with the message (expecting verification to fail)
    tampered_message = b"hello world!!!"
    tampered_is_valid = verify_signature(public_key, tampered_message, signature)
    
    # Assert that the signature verification fails for the tampered message
    assert not tampered_is_valid, "Signature verification unexpectedly passed for a tampered message."

    # Step 6: Simulate tampering with the signature (generate a new signature for the tampered message)
    tampered_signature = sign_message(private_key, tampered_message)

    # Verify that the tampered signature doesn't match the original signature
    tampered_signature_is_valid = verify_signature(public_key, message, tampered_signature)
    
    # Assert that the verification fails with the tampered signature
    assert not tampered_signature_is_valid, "Signature verification unexpectedly passed for a tampered signature."
    
    # Assert that the verification fails with tampered signature
    #assert not tampered_signature_is_valid, "Signature verification unexpectedly passed for a tampered signature."
    breakpoint()

@pytest.mark.asyncio
async def test_edge_cases() -> None:
    """Test some edge cases around signing and verification."""
    
    # Step 1: Generate a new key pair with a different seed
    SEED: bytes = bytes([0, 50, 6, 244, 24, 199, 1, 25, 52, 88, 130,
                         19, 18, 12, 89, 6, 220, 18, 102, 58, 209, 82,
                         12, 62, 89, 110, 182, 9, 44, 20, 254, 22])    
    private_key, public_key = generate_key_pair(SEED)

    # Step 2: Define the message
    message = b"another message"

    # Step 3: Sign the message
    signature = sign_message(private_key, message)

    # Step 4: Verify the signature
    is_valid = verify_signature(public_key, message, signature)
    
    # Assert that the signature is valid
    assert is_valid, "Signature verification failed for the correct message."

    # Step 5: Verify with a different message (this should fail)
    different_message = b"yet another message"
    different_is_valid = verify_signature(public_key, different_message, signature)
    
    # Assert that signature verification fails for a different message
    assert not different_is_valid, "Signature verification unexpectedly passed for a different message."


@pytest.mark.asyncio
async def test_invalid_public_key() -> None:
    """Test invalid public key during verification."""
    
    INVALID_SEED: bytes = bytes([0, 50, 6, 244, 24, 199, 1, 25, 
                         52, 88, 129, 19, 18, 12, 89, 6, 
                         220, 18, 102, 58, 209, 82, 12, 62, 
                         89, 110, 182, 9, 44, 20, 250, 21])

    # Step 1: Generate key pair
    SEED: bytes = bytes([0, 50, 6, 244, 24, 199, 1, 25, 
                         52, 88, 129, 19, 18, 12, 89, 6, 
                         220, 18, 102, 58, 209, 82, 12, 62, 
                         89, 110, 182, 9, 44, 20, 254, 22])

    private_key, public_key = generate_key_pair(SEED)

    # Step 2: Sign a message
    message = b"message with invalid public key"
    signature = sign_message(private_key, message)

    # Step 3: Create an invalid public key (e.g., public key from a different key pair)
    invalid_public_key = AugSchemeMPL.key_gen(INVALID_SEED).get_g1()

    # Step 4: Verify the signature with the invalid public key (expecting failure)
    invalid_is_valid = verify_signature(invalid_public_key, message, signature)

    # Assert that the signature verification fails for the invalid public key
    assert not invalid_is_valid, "Signature verification unexpectedly passed with an invalid public key."


@pytest.mark.asyncio
async def test_empty_message() -> None:
    """Test edge case with an empty message."""
    
    # Step 1: Generate a key pair
    SEED: bytes = bytes([0, 50, 6, 244, 24, 199, 1, 25, 52, 88, 129,
                         19, 18, 12, 89, 6, 220, 18, 102, 58, 209, 82,
                         12, 62, 89, 110, 182, 9, 44, 20, 254, 22])
    private_key, public_key = generate_key_pair(SEED)

    # Step 2: Define an empty message
    empty_message = b""

    # Step 3: Sign the empty message
    signature = sign_message(private_key, empty_message)

    # Step 4: Verify the signature
    is_valid = verify_signature(public_key, empty_message, signature)
    
    # Assert that the signature is valid for the empty message
    assert is_valid, "Signature verification failed for the empty message."