import secp256k1
import base58
import hmac
import hashlib

idx = bytes.fromhex("00000000")
tpub = base58.b58decode("tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp")[:-4]
data = tpub[-33:] + idx
key = tpub[-65:-33]
digest = hmac.new(data+key,digestmod=hashlib.sha512).digest()
child_chain_code = digest[32:]
PubKey = secp256k1.PublicKey(data[0:33],raw=True)
PubKey.tweak_add(digest[0:32])
print(PubKey.serialize().hex())