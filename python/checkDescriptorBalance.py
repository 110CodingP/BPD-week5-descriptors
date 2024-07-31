from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_connection = AuthServiceProxy("http://alice:password@127.0.0.1:18443")
descriptor = "wpkh(tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp/*)"
desc = rpc_connection.getdescriptorinfo(descriptor)
descriptor  = desc["descriptor"]
print(rpc_connection.scantxoutset("start",[descriptor]))