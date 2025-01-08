import pytest

def is_valid_hex_string(hex_string):
    """Check if a string is a valid hexadecimal string."""
    try:
        bytes.fromhex(hex_string)  # Try converting the string to bytes
        return True
    except ValueError:
        return False

def parse_spend_bundle(hex_string):
    """Convert the hex string into a spend bundle."""
    if not hex_string or not is_valid_hex_string(hex_string):
        raise ValueError("Invalid hex string or empty input.")
    return bytes.fromhex(hex_string)

# Test cases

def test_valid_hex_string():
    """Test for valid hexadecimal strings."""
#    valid_hex = "27ae41e4649b934ca495991b7852b85500000000000000000000000000000001"
    puzzle_hashes2 : bytes = fromhex("0x74d42ddc2e8fe2fdb21bdb402564ec412bec69ac3c3eb53a4da594aea81717aa")
    result = parse_spend_bundle(valid_hex)
    assert isinstance(result, bytes), "The result should be of type 'bytes'"

def test_invalid_hex_string():
    """Test for an invalid hexadecimal string."""
    invalid_hex = "invalidHex123Z"
    with pytest.raises(ValueError, match="Invalid hex string or empty input."):
        parse_spend_bundle(invalid_hex)

def test_empty_string():
    """Test for an empty string."""
    empty_hex = ""
    with pytest.raises(ValueError, match="Invalid hex string or empty input."):
        parse_spend_bundle(empty_hex)

def test_hex_string_with_whitespace():
    """Test for hex string with leading or trailing whitespace."""
    hex_with_whitespace = "   27ae41e4649b934ca495991b7852b85500000000000000000000000000000001   "
    result = parse_spend_bundle(hex_with_whitespace.strip())  # Strip the input before parsing
    assert isinstance(result, bytes), "The result should be of type 'bytes'"

def test_invalid_characters_in_hex():
    """Test for a hex string with non-hex characters."""
    invalid_char_hex = "G27ae41e4649b934ca495991b7852b85500000000000000000000000000000001"
    with pytest.raises(ValueError, match="Invalid hex string or empty input."):
        parse_spend_bundle(invalid_char_hex)
