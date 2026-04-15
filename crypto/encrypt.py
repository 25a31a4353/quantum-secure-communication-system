def string_to_bits(s):
    """Converts a string to a list of bits."""
    result = []
    for c in s:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])
    return result

def bits_to_string(bits):
    """Converts a list of bits back to a string."""
    s = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char_code = int(''.join(str(b) for b in byte), 2)
        s += chr(char_code)
    return s

def xor_encrypt(plaintext, key_bits_str):
    """
    Encrypts a plaintext string using XOR with the given binary key string.
    Returns cipher bits, the actual key used, and the decrypted plaintext (for verification).
    """
    if not plaintext or not key_bits_str:
        return "", "", ""
        
    pt_bits = string_to_bits(plaintext)
    key_bits = [int(b) for b in key_bits_str]
    
    # Extend or truncate key to match plaintext size
    extended_key = []
    for i in range(len(pt_bits)):
        extended_key.append(key_bits[i % len(key_bits)])
        
    # XOR encryption
    cipher_bits = [p ^ k for p, k in zip(pt_bits, extended_key)]
    
    # XOR decryption (should match plaintext, used for verification step in UI)
    decrypted_bits = [c ^ k for c, k in zip(cipher_bits, extended_key)]
    decrypted_str = bits_to_string(decrypted_bits)
    
    cipher_result = ''.join(str(b) for b in cipher_bits)
    used_key_result = ''.join(str(b) for b in extended_key)
    
    return cipher_result, used_key_result, decrypted_str
