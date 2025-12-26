import hashlib

def hash_md5_bytes(text: str) -> bytes:
    """
    Hash un texte en MD5 et retourne le résultat sous forme de bytes (comme b'...')
    """
    encoded_text = text.encode("utf-8")      # Encode le texte en bytes
    md5_hash = hashlib.md5(encoded_text)     # Crée le hash MD5
    return md5_hash.digest()                  # Retourne le hash en bytes

if __name__ == "__main__":
    texte = input("Entrez le texte à hasher : ")
    hashed_bytes = hash_md5_bytes(texte)
    print(f"EXPECTED_HASH = {hashed_bytes}")
