import hmac
import hashlib

input = bytes.fromhex("027b578d62bbbfe192658fdf4b634ea8a4a60b62931626767c3b9f769ffa35a996000000006e6b0da7c569284facf04cbb1f9f9a7b0ccc511181b3101d266ad15cb353bbc0")
print(hmac.new(input,digestmod=hashlib.sha3_512).digest().hex())