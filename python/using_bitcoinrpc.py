from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_connection = AuthServiceProxy("http://alice:password@127.0.0.1:18443")
descriptor = "wpkh(tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp/*)"
desc = rpc_connection.getdescriptorinfo(descriptor)
descriptor  = desc["descriptor"]
# scantxoutset = rpc_connection.scantxoutset("start",[descriptor])
gap = 0
idx = 0
balance = 0.0
idx = 0
while (gap<10):
    address = rpc_connection.deriveaddresses(descriptor,[idx,idx])
    idx += 1
    print(address)
    scantxoutset = rpc_connection.scantxoutset("start",[f"addr({address[0]})"])
    # print(scantxoutset)
    if not scantxoutset["unspents"]:
        gap += 1
    else:
        gap = 0
    balance += float(scantxoutset["total_amount"])
print(balance)