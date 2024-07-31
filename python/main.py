from bitcoinrpc.authproxy import AuthServiceProxy
import hmac
import hashlib
import secp256k1
import base58
import b32_ref as b32

def main():
  rpc_connection = AuthServiceProxy("http://alice:password@127.0.0.1:18443")
  descriptor = "wpkh(tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp/*)"
  desc = rpc_connection.getdescriptorinfo(descriptor)
  descriptor  = desc["descriptor"]

  def hash160(data):
     preimage = hashlib.sha256(data).digest()
     return hashlib.new("ripemd160",preimage).digest()
  
  def spk_to_bech32(data):
    network = "bcrt"
    version = 0
    if (data[0]):
      version = data[0]-bytes.fromhex("50")
    return b32.encode(network,version,data[2:])
  
  def deriveWPKH(idx):
    tpub = base58.b58decode("tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp")[:-4] # ignore checksum at end of base58 decoded value
    data = tpub[-33:] + idx.to_bytes(4,"big",signed=False) #use last 32 bytes of pubkey
    key = tpub[-65:-33]
    # print(key.hex())
    digest = hmac.new(key,data,digestmod=hashlib.sha512).digest()
    child_chain_code = digest[32:]
    PubKey = secp256k1.PublicKey(tpub[-33:],True)
    # print(PubKey.serialize().hex())

    PubKey = PubKey.tweak_add(digest[0:32])
    # print(PubKey.serialize().hex())


    pk_hash = hash160(PubKey.serialize())

    prefix = bytes.fromhex("0014")
    return spk_to_bech32(prefix + pk_hash)
    
  # scantxoutset = rpc_connection.scantxoutset("start",[descriptor])
  gap = 0
  idx = 0
  balance = 0.0
  idx = 0
  while (gap<10):
      address = deriveWPKH(idx)
      print(address)
      idx += 1
      scantxoutset = rpc_connection.scantxoutset("start",[f"addr({address})"])
      # print(scantxoutset)
      if not scantxoutset["unspents"]:
          gap += 1
      else:
          gap = 0
      balance += float(scantxoutset["total_amount"])
  print(balance)


if __name__ == "__main__":
    main()

"""
  - References:
  - descriptors: https://thunderbiscuit.github.io/Learning-Bitcoin-from-the-Command-Line/03_5_Understanding_the_Descriptor.html and https://medium.com/@nagasha/understanding-output-script-descriptors-in-bitcoin-8af8f20e0008#:~:text=Output%20descriptors%20are%20simple%2C%20human,(spend)%20the%20associated%20script. and https://github.com/bitcoin/bips/blob/master/bip-0380.mediawiki and https://www.tftc.io/issue-843-bitcoin-output-descriptors/
  - reference: https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md and https://developer.bitcoin.org/reference/rpc/index.html
  - https://bitcoin.stackexchange.com/questions/99287/how-can-i-get-addresss-balance-that-doesnt-belong-to-my-bitcoin-core-wallet?noredirect=1&lq=1
  - https://bitcoin.stackexchange.com/questions/95893/get-balance-for-an-array-of-addresses-with-bitcoin-core
  - as always: https://learnmeabitcoin.com/technical/keys/hd-wallets/derivation-paths/
  - tpub : https://bitcoin.stackexchange.com/questions/74056/basic-concept-of-bitcoin-public-and-private-keys#:~:text=So%2C%20in%20bitcoinj%2C%20we%20use,'t%20contain%20real%20coins).
  - hmac-sha512: https://docs.python.org/3/library/hmac.html
  - wow: https://outputdescriptors.org/
  - converting to xpub to pubkey : https://bitcoin.stackexchange.com/questions/80724/converting-xpub-key-to-core-format
  - p2wpkh to address: https://github.com/chaincodelabs/bitcoin-tx-tutorial/blob/main/functions/addresses.py
  - bech32 address reference: https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
"""