
import json
import requests
from web3 import Web3

import subprocess
from subprocess import Popen
import os
import shutil
from subprocess import PIPE
import math
import numpy as np


# IPFS auths
proj_id = '2MWnLdSYBRH5iyPG53RVgJbXu3r'
proj_secret = 'd1174b0df2ccc7759932bfb0fe84e2a9'

chain_id = 1337
address = "0xAE0f8d7E9BD3dc06ABA60Ab94Af1a59286864499"
private = "0x44879aad238642eaf122b3b229f5820c866494fc7b528689aafad215bb78de40"

sidechain_address = "0xAE0f8d7E9BD3dc06ABA60Ab94Af1a59286864499"
sidechain_private = "0x44879aad238642eaf122b3b229f5820c866494fc7b528689aafad215bb78de40"

#
# tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# #print("TX Recipt:" + tx_receipt)
#
# pull_backend_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#
# # How do I get the variable of a contract, e.g. name from Backend?
#
#
# # print(pull_backend_contract.functions.)
# communityName = "New Community #10"
#
# nonce = w3.eth.getTransactionCount(address)
# createCommunityTx = pull_backend_contract.functions\
#     .createCommunity(communityName, address, 6500)\
#     .buildTransaction(
#     {
#         "gasPrice": w3.eth.gas_price,
#         "chainId": chain_id,
#         "from": address,
#         "nonce": nonce,
#     }
# )
# create_community_signed_txn = w3.eth.account.sign_transaction(createCommunityTx, private_key=private)
# tx_hash = w3.eth.send_raw_transaction(create_community_signed_txn.rawTransaction)
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(tx_receipt)


def deploy_backend():
    print("Attempting to upload corpus....")

    backend_json = json.load(open('abis/Backend.json'))
    bytecode = backend_json["data"]["bytecode"]["object"]
    abi = backend_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    # Create a fresh version of the backend contract
    backend_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(address)

    create_backend_tx = backend_contract.constructor().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": address,
            "nonce": nonce,
        }
    )
    # print(create_backend_tx)
    create_backend_signed_txn = w3.eth.account.sign_transaction(create_backend_tx, private_key=private)
    # print(signed_txn)
    create_backend_signed_txn_hash = w3.eth.send_raw_transaction(create_backend_signed_txn.rawTransaction)
    create_backend_signed_txn_receipt = w3.eth.wait_for_transaction_receipt(create_backend_signed_txn_hash)
    backend_contract_address = create_backend_signed_txn_receipt.contractAddress
    return backend_contract_address

def add_community(backend_contract_address, community_name, community_port):
    posting_contract_address = deploy_community_posting_contract(community_port)
    community_contract_address = deploy_community(posting_contract_address, community_port, backend_contract_address, posting_contract_address)
    crosslink_community_recipt = crosslink_community(backend_contract_address, community_name, community_contract_address, community_port)
    # Turns out the contracts address doesn't change after you update it's state by calling a function
    # Used to return this: (posting_contract_address, community_contract_address, updated_backend_address)
    return (posting_contract_address, community_contract_address, crosslink_community_recipt)

def deploy_community_posting_contract(community_port):
    print("Creating posting contract for community.")
    posting_json = json.load(open('abis/Posting.json'))
    bytecode = posting_json["data"]["bytecode"]["object"]
    abi = posting_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))

    # Create a fresh version of the backend contract
    posting_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(sidechain_address)

    create_posting_contract_tx = posting_contract.constructor(community_port).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": sidechain_address,
            "nonce": nonce,
        }
    )
    # print(create_backend_tx)
    create_posting_contract_signed_tx = w3.eth.account.sign_transaction(create_posting_contract_tx, private_key=sidechain_private)
    # print(signed_txn)
    create_posting_contract_signed_tx_hash = w3.eth.send_raw_transaction(create_posting_contract_signed_tx.rawTransaction)
    create_posting_contract_signed_tx_receipt = w3.eth.wait_for_transaction_receipt(create_posting_contract_signed_tx_hash)
    posting_contract_address = create_posting_contract_signed_tx_receipt.contractAddress
    return posting_contract_address

def deploy_community(community_name, community_port, parent_address, posting_contract_address):
    print("Deploying community to sidechain.")
    posting_json = json.load(open('abis/Community.json'))
    bytecode = posting_json["data"]["bytecode"]["object"]
    abi = posting_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))

    # Create a fresh version of the backend contract
    community_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(sidechain_address)

    # string memory _name, uint16 _port, address _parent, address _postingContract
    community_contract_tx = community_contract.constructor(community_name, community_port, parent_address, posting_contract_address).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": sidechain_address,
            "nonce": nonce,
        }
    )
    # print(create_backend_tx)
    community_contract_signed_tx = w3.eth.account.sign_transaction(community_contract_tx, private_key=sidechain_private)
    # print(signed_txn)
    community_contract_signed_tx_hash = w3.eth.send_raw_transaction(community_contract_signed_tx.rawTransaction)
    community_contract_signed_tx_receipt = w3.eth.wait_for_transaction_receipt(community_contract_signed_tx_hash)
    community_contract_address = community_contract_signed_tx_receipt.contractAddress
    return community_contract_address

def crosslink_community(backend_contract_address, community_name, community_contract_address, community_port):
    print("Crosslinking community chain to beacon chain.")
    backend_json = json.load(open('abis/Backend.json'))
    bytecode = backend_json["data"]["bytecode"]["object"]
    abi = backend_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    pulled_backend_contract = w3.eth.contract(address=backend_contract_address, abi=abi)

    nonce = w3.eth.getTransactionCount(address)

    create_community_tx = pulled_backend_contract.functions \
        .createCommunity(community_name, community_contract_address, community_port) \
        .buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": address,
            "nonce": nonce,
        }
    )

    # print(create_backend_tx)
    signed_create_community_tx = w3.eth.account.sign_transaction(create_community_tx, private_key=private)
    # print(signed_txn)
    signed_create_community_tx_hash = w3.eth.send_raw_transaction(signed_create_community_tx.rawTransaction)
    signed_create_community_tx_receipt = w3.eth.wait_for_transaction_receipt(signed_create_community_tx_hash)
    return signed_create_community_tx_receipt

def make_post(backend_contract_address, community_port, post_title, post_content):
    print("Post Title: " + post_title + " | Post Content: " + post_content)
    # Get backend contract
    # Fetch community contract address via port
    # Fetch posting contract from community contract
    # Make post

    # Backend contract
    backend_json = json.load(open('abis/Backend.json'))
    abi = backend_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    pulled_backend_contract = w3.eth.contract(address=backend_contract_address, abi=abi)

    # Fetch community contract via port
    community_address = pulled_backend_contract.functions.communityPortToAddress(community_port).call()
    community_json = json.load(open('abis/Community.json'))
    abi = community_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))
    community_contract = w3.eth.contract(address=community_address, abi=abi)

    # print(community_contract.all_functions())
    # print("Posting contract address:", end="")
    # print(community_contract.functions.postingContract().call())

    posting_contract_address = community_contract.functions.postingContract().call()
    posting_json = json.load(open('abis/Posting.json'))
    abi = posting_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))
    posting_contract = w3.eth.contract(address=posting_contract_address, abi=abi)

    # Upload to IPFS first if over 1000 chars long:
    # Otherwise just upload straight to the chain.
    # Might just remove all posts with 800+ chars from the corpus to save space
    if len(post_content) > 1000:
        files = {
            'file': post_content,
        }
        response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=false",
                                 auth=(proj_id, proj_secret), files=files)
        hash = response.json()['Hash']
        post_content = "ipfs|" + hash

    make_post_tx = posting_contract.functions \
        .makePost(post_title, post_content) \
        .buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": sidechain_address,
            "nonce": w3.eth.getTransactionCount(sidechain_address),
        }
    )

    # print(create_backend_tx)
    signed_make_post_tx = w3.eth.account.sign_transaction(make_post_tx, private_key=sidechain_private)
    # print(signed_txn)
    # Prints all the acccount:
    # print(w3.eth.accounts)
    # Print the accounts balance:
    # for acc in w3.eth.accounts:
    #     print("Balance: " + str(w3.eth.get_balance(acc)))
    signed_make_post_tx_hash = w3.eth.send_raw_transaction(signed_make_post_tx.rawTransaction)
    signed_make_post_tx_receipt = w3.eth.wait_for_transaction_receipt(signed_make_post_tx_hash)
    return signed_make_post_tx_receipt.contractAddress


def list_posts(backend_contract_address, community_port):
    # Backend contract
    backend_json = json.load(open('abis/Backend.json'))
    abi = backend_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    pulled_backend_contract = w3.eth.contract(address=backend_contract_address, abi=abi)

    # Fetch community contract via port
    community_address = pulled_backend_contract.functions.communityPortToAddress(community_port).call()
    community_json = json.load(open('abis/Community.json'))
    abi = community_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))
    community_contract = w3.eth.contract(address=community_address, abi=abi)

    # print(community_contract.all_functions())
    # print("Posting contract address:", end="")
    # print(community_contract.functions.postingContract().call())

    posting_contract_address = community_contract.functions.postingContract().call()
    posting_json = json.load(open('abis/Posting.json'))
    abi = posting_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))
    posting_contract = w3.eth.contract(address=posting_contract_address, abi=abi)

    number_of_posts = posting_contract.functions.postCount().call()
    print("Number of posts:" + str(number_of_posts))
    for i in range(number_of_posts):
        post = posting_contract.functions.posts(i).call()
        print(post)
        # Need to index rather than call to a specific variable with objects.
        # eg instead of print(post._title)
        print(post[2])


def test_upload():
    backend_contract_address = deploy_backend()
    print("Backend contract address: ", end="")
    print(backend_contract_address)
    (posting_contract_address, community_contract_address, crosslink_community_receipt) = add_community(backend_contract_address, "Community Attempt 1", 9545)
    make_post(backend_contract_address, 9545, "First Post", "Content of First Post")
    make_post(backend_contract_address, 9545, "Second Post", "Content of Second Post")
    make_post(backend_contract_address, 9545, "Third Post", "Content of Third Post")
    list_posts(backend_contract_address, 9545)

def upload_one_hundred_posts_to_one_sidechain():
    path = "C:/Users/John/Downloads/RC_2009-04/RC_2009-04.jsonl"

    # {"controversiality":0,"body":"A look at Vietnam and Mexico exposes the myth of market liberalisation.","subreddit_id":"t5_6","link_id":"t3_17863","stickied":false,"subreddit":"reddit.com","score":2,"ups":2,"author_flair_css_class":null,"created_utc":1134365188,"author_flair_text":null,"author":"frjo","id":"c13","edited":false,"parent_id":"t3_17863","gilded":0,"distinguished":null,"retrieved_on":1473738411}
    # {"created_utc":1134365725,"author_flair_css_class":null,"score":1,"ups":1,"subreddit":"reddit.com","stickied":false,"link_id":"t3_17866","subreddit_id":"t5_6","controversiality":0,"body":"The site states \"What can I use it for? Meeting notes, Reports, technical specs Sign-up sheets, proposals and much more...\", just like any other new breeed of sites that want us to store everything we have on the web. And they even guarantee multiple levels of security and encryption etc. But what prevents these web site operators fom accessing and/or stealing Meeting notes, Reports, technical specs Sign-up sheets, proposals and much more, for competitive or personal gains...? I am pretty sure that most of them are honest, but what's there to prevent me from setting up a good useful site and stealing all your data? Call me paranoid - I am.","retrieved_on":1473738411,"distinguished":null,"gilded":0,"id":"c14","edited":false,"parent_id":"t3_17866","author":"zse7zse","author_flair_text":null}
    # {"gilded":0,"distinguished":null,"retrieved_on":1473738411,"author":"[deleted]","author_flair_text":null,"edited":false,"id":"c15","parent_id":"t3_17869","subreddit":"reddit.com","score":0,"ups":0,"created_utc":1134366848,"author_flair_css_class":null,"body":"Jython related topics by Frank Wierzbicki","controversiality":0,"subreddit_id":"t5_6","stickied":false,"link_id":"t3_17869"}
    # {"gilded":0,"retrieved_on":1473738411,"distinguished":null,"author_flair_text":null,"author":"[deleted]","edited":false,"parent_id":"t3_17870","id":"c16","subreddit":"reddit.com","created_utc":1134367660,"author_flair_css_class":null,"score":1,"ups":1,"body":"[deleted]","controversiality":0,"stickied":false,"link_id":"t3_17870","subreddit_id":"t5_6"}
    # {"gilded":0,"retrieved_on":1473738411,"distinguished":null,"author_flair_text":null,"author":"rjoseph","edited":false,"id":"c17","parent_id":"t3_17817","subreddit":"reddit.com","author_flair_css_class":null,"created_utc":1134367754,"score":1,"ups":1,"body":"Saft is by far the best extension you could tak onto your Safari","controversiality":0,"link_id":"t3_17817","stickied":false,"subreddit_id":"t5_6"}

    backend_contract_address = deploy_backend()
    print("Backend contract address: ", end="")
    print(backend_contract_address)
    (posting_contract_address, community_contract_address, crosslink_community_receipt) = add_community(backend_contract_address, "Community Attempt 1", 9545)


    subreddits = []
    subs = {}
    number_of_subs = 0
    i = 0
    failed_posts = 0
    for line in open(path, 'r'):
        print(str(i) + "\ ", end="")
        entry = json.loads(line)
        subreddit = entry['subreddit']
        body = entry['body']
        # body_max_length = min(1000, len(body))
        # body = body[0:body_max_length]

        try:
            make_post(backend_contract_address, 9545, "", body)
        except:
            print("Error")
            print("Length of post: " + str(len(body)))
            failed_posts += 1

        i += 1
        if i == 50:
            break

    print("One hundred posts made")
    print("Number of failed posts: " + str(failed_posts))
    list_posts(backend_contract_address, 9545)


def upload_corpus():
    path = "C:/Users/John/Downloads/RC_2009-04/RC_2009-04.jsonl"

    # {"controversiality":0,"body":"A look at Vietnam and Mexico exposes the myth of market liberalisation.","subreddit_id":"t5_6","link_id":"t3_17863","stickied":false,"subreddit":"reddit.com","score":2,"ups":2,"author_flair_css_class":null,"created_utc":1134365188,"author_flair_text":null,"author":"frjo","id":"c13","edited":false,"parent_id":"t3_17863","gilded":0,"distinguished":null,"retrieved_on":1473738411}
    # {"created_utc":1134365725,"author_flair_css_class":null,"score":1,"ups":1,"subreddit":"reddit.com","stickied":false,"link_id":"t3_17866","subreddit_id":"t5_6","controversiality":0,"body":"The site states \"What can I use it for? Meeting notes, Reports, technical specs Sign-up sheets, proposals and much more...\", just like any other new breeed of sites that want us to store everything we have on the web. And they even guarantee multiple levels of security and encryption etc. But what prevents these web site operators fom accessing and/or stealing Meeting notes, Reports, technical specs Sign-up sheets, proposals and much more, for competitive or personal gains...? I am pretty sure that most of them are honest, but what's there to prevent me from setting up a good useful site and stealing all your data? Call me paranoid - I am.","retrieved_on":1473738411,"distinguished":null,"gilded":0,"id":"c14","edited":false,"parent_id":"t3_17866","author":"zse7zse","author_flair_text":null}
    # {"gilded":0,"distinguished":null,"retrieved_on":1473738411,"author":"[deleted]","author_flair_text":null,"edited":false,"id":"c15","parent_id":"t3_17869","subreddit":"reddit.com","score":0,"ups":0,"created_utc":1134366848,"author_flair_css_class":null,"body":"Jython related topics by Frank Wierzbicki","controversiality":0,"subreddit_id":"t5_6","stickied":false,"link_id":"t3_17869"}
    # {"gilded":0,"retrieved_on":1473738411,"distinguished":null,"author_flair_text":null,"author":"[deleted]","edited":false,"parent_id":"t3_17870","id":"c16","subreddit":"reddit.com","created_utc":1134367660,"author_flair_css_class":null,"score":1,"ups":1,"body":"[deleted]","controversiality":0,"stickied":false,"link_id":"t3_17870","subreddit_id":"t5_6"}
    # {"gilded":0,"retrieved_on":1473738411,"distinguished":null,"author_flair_text":null,"author":"rjoseph","edited":false,"id":"c17","parent_id":"t3_17817","subreddit":"reddit.com","author_flair_css_class":null,"created_utc":1134367754,"score":1,"ups":1,"body":"Saft is by far the best extension you could tak onto your Safari","controversiality":0,"link_id":"t3_17817","stickied":false,"subreddit_id":"t5_6"}

    backend_contract_address = deploy_backend()
    print("Backend contract address: ", end="")
    print(backend_contract_address)

    starting_port = 6000
    current_port = starting_port
    subbredit_to_port = {}
    i = 0
    failed_posts = 0
    failed_communities = 0
    failed_posts_string = ""
    for line in open(path, 'r'):
        print(str(i) + "\ ", end="")
        entry = json.loads(line)
        subreddit = entry['subreddit']
        body = entry['body']
        # This should be replaced with uploading to IPFS, and adding the content hash to the chain instead


        # Community exists
        if subreddit in subbredit_to_port:
            port = subbredit_to_port[subreddit]
            try:
                make_post(backend_contract_address, port, "", body)
            except:
                print("Posting failed")
                print("Length of post: " + str(len(body)))
                failed_posts += 1
                failed_posts_string += str(i) + "\n"

        # Community needs to be made
        else:
            try:
                (posting_contract_address, community_contract_address, crosslink_community_receipt) = add_community(
                    backend_contract_address, subreddit, current_port)
                subbredit_to_port[subreddit] = current_port
                try:
                    make_post(backend_contract_address, current_port, "", body)
                    current_port += 1
                except:
                    print("Posting failed")
                    print("Length of post: " + str(len(body)))
                    failed_posts += 1
                    failed_posts_string += str(i) + "\n"
            except:
                print("Failed to make commmunity. Community name:" + str(subreddit))
                failed_communities += 1

        i += 1
        if i == 100:
            break

    f = open("failed_posts.txt", "w")
    f.write(failed_posts_string)
    f.close()

    print("One hundred posts made")
    print("Number of failed posts: " + str(failed_posts))
    list_posts(backend_contract_address, 9545)

# Start by only doing the first 100 lines
# Need to check if I start a chain, then restart it using the same database, will it return the same

# It might just be easier to create a 2d array of all the posts, then


# make_post("0x42e7C73cE698b821f0780E5b3BCB989aFfB05807", 6545, "New Post", "New content")
# list_posts("0x42e7C73cE698b821f0780E5b3BCB989aFfB05807", 6545)


# Go through the entire dataset and order it into a dictionary
# ['subreddit': [post1, post2, post3], 'subreddit2': [post4, post5]]
# Then start uploading
# Iterate through each subreddit and start a node
# Upload each post to the node
# Once finished stop the node and iterate



def start_node(port, subreddit_name):
    print("Starting node at port: " + str(port))

    # wallets = [
    #     "058297ff32e8d319a97150976e7668b2c5d16384d2f97e6dbedd3a44b9e2864b",
    #     "7f94f5966f7bc2c04958d2ee7f1e7d2ae25cf778aed8aa66d95f54b8442ccd42",
    #     "8eb3577411f5ba12545fd5b44ab42bc365a6bf45a24377653b5bd7ab0822f269",
    #     "345d0671103a3f88d80794679d9a6c4bf1ab5f88749e1e9f7f4d75d26c925a0a",
    #     "bba027dca5385468b88f3497285b2002d2cc2b666c5f4bbbefdfe684a6cf258a",
    #     "81f770a630a2c04d2e92d6df0cbef22d7a50334083e3b93b60f7aa412fbfb3ee",
    #     "50a962d8f040495ddf656b1c0ac60edb28cf4ff28244bb11510d5e9285e31d2b",
    #     "09075393bfa62fd5159d645286638b6289b1f9615cf33e7cffa9e13e7c657a40",
    #     "82049d7f85d7aa741078708db7643050ab034eb66ab104ed4f2b1faef906e9e0"
    # ]

    wallets = [
        "44879aad238642eaf122b3b229f5820c866494fc7b528689aafad215bb78de40",
        "d8d790f09d4e286ec9c9cac42bcca0aaeaf1dfeb4651411f6e45332f4c6416c0",
        "69630ba2174a88d94e51339dbc19b6fe933c4cf82ac483da48971ed6f52f478a",
        "cfb5d56c634bd097c910ba594d223a00b877eafde717aa20f1abbe115e73df20"
    ]

    starting_amount = "10000000000000000000000000"

    accounts = ""
    for wallet in wallets:
        accounts += "0x" + str(wallet) + "," + str(starting_amount) + " "
    accounts = accounts[0:-1]

    # ganache --chain.allowUnlimitedContractSize=true --port=6545 --database.dbPath=chain4 --wallet.accounts 0x058297ff32e8d319a97150976e7668b2c5d16384d2f97e6dbedd3a44b9e2864b,10000000000000000000000000 0x7f94f5966f7bc2c04958d2ee7f1e7d2ae25cf778aed8aa66d95f54b8442ccd42,10000000000000000000000000 0x345d0671103a3f88d80794679d9a6c4bf1ab5f88749e1e9f7f4d75d26c925a0a,10000000000000000000000000 --miner.instamine eager

    command = Popen("ganache --chain.allowUnlimitedContractSize=true --port={i:d} --database.dbPath=chain{i:d}{subreddit:s} --wallet.accounts {accounts:s} --miner.instamine eager -D".format(i=port, subreddit=subreddit_name, accounts=accounts), shell=True,
                stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    exitcode = command.wait()
    name = command.communicate()

    if exitcode == 0:
        print("Node started sucessfully.")
    else:
        print("Node failed to start at port: " + str(port))

    return name

def stop_node(port, name):
    print("Stopping node at port: " + str(port) + " with name: " + name)

    # Remove \n
    # name = name[0:-1]

    command = Popen("ganache instances stop {chain_name:s}".format(chain_name=name), shell=True,
                      stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")

    exitcode = command.wait()
    result = command.communicate()
    print(result)

    if result[0] == 'Instance stopped\n':
        print("Node stopped sucessfully.")
    else:
        print("Node failed to stop at port: " + str(port))

def filter_dataset(path):
    print("Filtering dataset.")
    starting_port = 6000
    
    total_posts = 0
    total_subreddits = 0

    dataset = {}
    # ['subreddit': [post1, post2, post3], 'subreddit2': [post4, post5]]

    for line in open(path, 'r'):
        entry = json.loads(line)
        subreddit = entry['subreddit']
        total_posts += 1

        if subreddit in dataset:
            subreddit_posts = dataset[subreddit]
            subreddit_posts.append(entry['body'])
        else:
            subreddit_posts = [entry['body']]
            dataset[subreddit] = subreddit_posts
            total_subreddits += 1

    print("Finished filtering dataset.")
    return dataset, total_posts, total_subreddits


def dynamic_upload(path):
    print("Starting dynamic upload of Reddit Corpus to ledger.")

    starting_node_port = 6000
    current_node_port = starting_node_port

    subreddit_assigned_port = {}

    backend_contract_address = deploy_backend()
    print("Backend contract address: " + backend_contract_address)

    dataset, total_posts, total_subreddits = filter_dataset(path)

    uploaded_posts_count = 0
    current_subreddit_count = 0

    for subreddit in dataset:
        posts = dataset[subreddit]

        chain_name = start_node(current_node_port, subreddit)[0]
        chain_name = chain_name[0:-1]
        print(chain_name)

        current_subreddit_count += 1
        current_post_number = 0
        posts_length = len(posts)
        
        add_community(backend_contract_address, subreddit, current_node_port)
        
        for post in posts:

            # {"controversiality":0,"body":"A look at Vietnam and Mexico exposes the myth of market liberalisation.","subreddit_id":"t5_6","link_id":"t3_17863","stickied":false,"subreddit":"reddit.com","score":2,"ups":2,"author_flair_css_class":null,"created_utc":1134365188,"author_flair_text":null,"author":"frjo","id":"c13","edited":false,"parent_id":"t3_17863","gilded":0,"distinguished":null,"retrieved_on":1473738411}
            # {"created_utc":1134365725,"author_flair_css_class":null,"score":1,"ups":1,"subreddit":"reddit.com","stickied":false,"link_id":"t3_17866","subreddit_id":"t5_6","controversiality":0,"body":"The site states \"What can I use it for? Meeting notes, Reports, technical specs Sign-up sheets, proposals and much more...\", just like any other new breeed of sites that want us to store everything we have on the web. And they even guarantee multiple levels of security and encryption etc. But what prevents these web site operators fom accessing and/or stealing Meeting notes, Reports, technical specs Sign-up sheets, proposals and much more, for competitive or personal gains...? I am pretty sure that most of them are honest, but what's there to prevent me from setting up a good useful site and stealing all your data? Call me paranoid - I am.","retrieved_on":1473738411,"distinguished":null,"gilded":0,"id":"c14","edited":false,"parent_id":"t3_17866","author":"zse7zse","author_flair_text":null}
            # {"gilded":0,"distinguished":null,"retrieved_on":1473738411,"author":"[deleted]","author_flair_text":null,"edited":false,"id":"c15","parent_id":"t3_17869","subreddit":"reddit.com","score":0,"ups":0,"created_utc":1134366848,"author_flair_css_class":null,"body":"Jython related topics by Frank Wierzbicki","controversiality":0,"subreddit_id":"t5_6","stickied":false,"link_id":"t3_17869"}
            # {"gilded":0,"retrieved_on":1473738411,"distinguished":null,"author_flair_text":null,"author":"[deleted]","edited":false,"parent_id":"t3_17870","id":"c16","subreddit":"reddit.com","created_utc":1134367660,"author_flair_css_class":null,"score":1,"ups":1,"body":"[deleted]","controversiality":0,"stickied":false,"link_id":"t3_17870","subreddit_id":"t5_6"}
            # {"gilded":0,"retrieved_on":1473738411,"distinguished":null,"author_flair_text":null,"author":"rjoseph","edited":false,"id":"c17","parent_id":"t3_17817","subreddit":"reddit.com","author_flair_css_class":null,"created_utc":1134367754,"score":1,"ups":1,"body":"Saft is by far the best extension you could tak onto your Safari","controversiality":0,"link_id":"t3_17817","stickied":false,"subreddit_id":"t5_6"}

            make_post(backend_contract_address, current_node_port, "", post)
            current_post_number += 1
            uploaded_posts_count += 1
            if uploaded_posts_count % 10 == 0:
                print("Post for this sub:" + str(current_post_number) + "/" + str(posts_length) + " | Posts total: " + str(uploaded_posts_count) + "/" + str(total_posts))
                print("Currently on subreddit " + str(current_subreddit_count) + "/" + str(total_subreddits))



        subreddit_assigned_port[subreddit] = current_node_port
        stop_node(current_node_port, chain_name)
        current_node_port += 1

# "0x42e7C73cE698b821f0780E5b3BCB989aFfB05807", 6545, "New Post", "New content"

# # path = "C:/Users/John/Downloads/RC_2009-04/RC_2009-04.jsonl"
path = "Reddit_Corpus_2016_01_1mb.txt"
# dynamic_upload(path)

def trim_dataset(path):

    corpus_file = open("datasets/Reddit_Corpus_2016_01_0.1mb.txt", "w")

    for line in open(path, 'r'):
        # entry = json.loads(line)
        corpus_file.write(line)

        file_size = os.path.getsize("datasets/Reddit_Corpus_2016_01_0.1mb.txt")
        print(file_size)
        # Desired file size of 50mb
        # 50mb == 5e+7
        # 100mb == 10e+7
        # 1mb == 1E+6 / 4hr
        # 0.1mb == 1E+5 / 240/4 = 24mins
        if file_size > 1E+5:
            corpus_file.close()
            break


# path = "E:/RC_2016-01"
path = "Reddit_Corpus_2016_01_1mb.txt"
trim_dataset(path)

# def delete_node_ledger():
#     shutil.rmtree('chain{i:s}'.format(i=str(starting_port + i)))

