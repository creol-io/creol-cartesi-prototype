from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

transaction = {
    'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
    'value': 1000000000,
    'gas': 2000000,
    'gasPrice': 234567897654321,
    'nonce': 0,
    'chainId': 1
}

networkKey = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'

signed = w3.eth.account.sign_transaction(transaction, networkKey)
print("Signed Local Transaction Hash is: \n")
print(w3.toHex(signed.hash))

print("Loading \"Transmitted Thread Txn\"...")
with open('signedTxn.json') as json_file:
    signed2 = json.load(json_file)
    print('Txn loaded:...')
print('Comparing local transaction sign against transmitted transaction...')

result = signed.hash.hex() == signed2['hash']
if result:
    print("Success! Matching hashes, this txn was signed from within the network")
    exit(0)
else:
    print("Hashes do not match, not transmitting txn onchain")
    exit(1)