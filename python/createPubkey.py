import ecdsa

def priv_to_pub(privkey:bytes)->bytes:
        sk = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1) # privkey should be in bytes
        ver_key = sk.verifying_key
        uncompressed_pubkey = ver_key.to_string().hex()

        x_cor = bytes.fromhex(uncompressed_pubkey)[:32]
        y_cor = bytes.fromhex(uncompressed_pubkey)[32:]


        if int.from_bytes(y_cor,byteorder="big",signed=True)%2==0 :
            compressed_pubkey = bytes.fromhex("02") + x_cor
        else:
            compressed_pubkey = bytes.fromhex("03") + x_cor
        
        return compressed_pubkey