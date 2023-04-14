
import json
from web3 import Web3

print("Attempting to upload corpus....")

# with open("contracts/Backend.sol", "r") as file:
#     backend_file = file.read()
#     print(backend_file)

# Opening JSON file
f = open('abis/Backend.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list

# get bytecode
bytecode = data["data"]["bytecode"]["object"]
abi = data["abi"]

print(bytecode)
print(abi)

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
address = "0x2d829E5aCDD12E398087245de3e044177f8629a6"
private = "0x058297ff32e8d319a97150976e7668b2c5d16384d2f97e6dbedd3a44b9e2864b"

backend_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
print(backend_contract)
nonce = w3.eth.getTransactionCount(address)
print(nonce)

transaction = backend_contract.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": address,
        "nonce": nonce,
    }
)
print(transaction)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private)

print(signed_txn)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_recipe = w3.eth.wait_for_transaction_receipt(tx_hash)
#print("TX Recipt:" + tx_recipe)

pull_backend_contract = w3.eth.contract(address=tx_recipe.contractAddress, abi=abi)

# How do I get the variable of a contract, e.g. name from Backend?


# print(pull_backend_contract.functions.)
communityName = "New Community #10"

nonce = w3.eth.getTransactionCount(address)
createCommunityTx = pull_backend_contract.functions\
    .createCommunity(communityName, address, 6500)\
    .buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": address,
        "nonce": nonce,
    }
)
create_community_signed_txn = w3.eth.account.sign_transaction(createCommunityTx, private_key=private)
tx_hash = w3.eth.send_raw_transaction(create_community_signed_txn.rawTransaction)
tx_recipe = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_recipe)










