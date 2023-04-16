
from os.path import isfile, join
import time
from rlp import encode
import json
import requests
from web3 import Web3
from subprocess import Popen, PIPE
import os
import math

proj_id = ''
proj_secret = ''

chain_id = 1337
address = ""
private = ""

sidechain_address = address
sidechain_private = private

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def deploy_backend():
    print("Attempting to upload corpus....")

    backend_json = json.load(open('abis/Backend.json'))
    bytecode = backend_json["data"]["bytecode"]["object"]
    abi = backend_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

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

    create_backend_signed_txn = w3.eth.account.sign_transaction(create_backend_tx, private_key=private)
    create_backend_signed_txn_hash = w3.eth.send_raw_transaction(create_backend_signed_txn.rawTransaction)
    create_backend_signed_txn_receipt = w3.eth.wait_for_transaction_receipt(create_backend_signed_txn_hash)
    backend_contract_address = create_backend_signed_txn_receipt.contractAddress
    return backend_contract_address


def add_community(backend_contract_address, community_name, community_port):
    posting_contract_address = deploy_community_posting_contract(community_port)
    community_contract_address = deploy_community(posting_contract_address, community_port, backend_contract_address,
                                                  posting_contract_address)
    crosslink_community_recipt = crosslink_community(backend_contract_address, community_name,
                                                     community_contract_address, community_port)
    return (posting_contract_address, community_contract_address, crosslink_community_recipt)


def deploy_community_posting_contract(community_port):
    print("Creating posting contract for community.")
    posting_json = json.load(open('abis/Posting.json'))
    bytecode = posting_json["data"]["bytecode"]["object"]
    abi = posting_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))

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

    create_posting_contract_signed_tx = w3.eth.account.sign_transaction(create_posting_contract_tx,
                                                                        private_key=sidechain_private)

    create_posting_contract_signed_tx_hash = w3.eth.send_raw_transaction(
        create_posting_contract_signed_tx.rawTransaction)
    create_posting_contract_signed_tx_receipt = w3.eth.wait_for_transaction_receipt(
        create_posting_contract_signed_tx_hash)
    posting_contract_address = create_posting_contract_signed_tx_receipt.contractAddress
    return posting_contract_address


def deploy_community(community_name, community_port, parent_address, posting_contract_address):
    print("Deploying community to sidechain.")
    posting_json = json.load(open('abis/Community.json'))
    bytecode = posting_json["data"]["bytecode"]["object"]
    abi = posting_json["abi"]

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))

    community_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(sidechain_address)

    community_contract_tx = community_contract.constructor(community_name, community_port, parent_address,
                                                           posting_contract_address).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": sidechain_address,
            "nonce": nonce,
        }
    )

    community_contract_signed_tx = w3.eth.account.sign_transaction(community_contract_tx, private_key=sidechain_private)
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

    signed_create_community_tx = w3.eth.account.sign_transaction(create_community_tx, private_key=private)
    signed_create_community_tx_hash = w3.eth.send_raw_transaction(signed_create_community_tx.rawTransaction)
    signed_create_community_tx_receipt = w3.eth.wait_for_transaction_receipt(signed_create_community_tx_hash)
    return signed_create_community_tx_receipt


def make_post(backend_contract_address, community_port, post_title, post_content):
    print("Post Title: " + post_title + " | Post Content: " + post_content)

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

    posting_contract_address = community_contract.functions.postingContract().call()
    posting_json = json.load(open('abis/Posting.json'))
    abi = posting_json["abi"]
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:" + str(community_port)))
    posting_contract = w3.eth.contract(address=posting_contract_address, abi=abi)

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

    signed_make_post_tx = w3.eth.account.sign_transaction(make_post_tx, private_key=sidechain_private)
    signed_make_post_tx_hash = w3.eth.send_raw_transaction(signed_make_post_tx.rawTransaction)
    signed_make_post_tx_receipt = w3.eth.wait_for_transaction_receipt(signed_make_post_tx_hash)
    return signed_make_post_tx_receipt.contractAddress


def start_node(port, subreddit_name, db_path_extra):
    print("Starting node at port: " + str(port))

    wallets = [
        private[2:len(private)],
    ]

    starting_amount = "10000000000000000000000000"

    accounts = ""
    for wallet in wallets:
        accounts += "0x" + str(wallet) + "," + str(starting_amount) + " "
    accounts = accounts[0:-1]

    # Example command:
    # ganache --chain.allowUnlimitedContractSize=true --port=6545 --database.dbPath=chain4
    # --wallet.accounts 0x058297ff32e8d319a97150976e7668b2c5d16384d2f97e6dbedd3a44b9e2864b,10000000000000000000000000 0x7f94f5966f7bc2c04958d2ee7f1e7d2ae25cf778aed8aa66d95f54b8442ccd42,10000000000000000000000000 0x345d0671103a3f88d80794679d9a6c4bf1ab5f88749e1e9f7f4d75d26c925a0a,10000000000000000000000000
    # --miner.blockTime=0 --miner.instamine eager
    command = Popen(
        "ganache --chain.allowUnlimitedContractSize=true --port={i:d} --database.dbPath=chain{path:s}{i:d}{subreddit:s} --wallet.accounts {accounts:s} --miner.blockTime=0 --miner.instamine=strict -D".format(
            i=port, path=db_path_extra, subreddit=subreddit_name, accounts=accounts), shell=True,
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


def record_stats(start_time, chain_path, post_count, text_file_name):
    f = "!blocks!length"
    if isfile(join(chain_path, f)):
        with open(join(chain_path, f), 'r') as block_length_file:
            most_recent_block_index = int(block_length_file.read()) - 1
            most_recent_block_size = os.path.getsize(join(chain_path, '!blocks!' + str(most_recent_block_index)))
            elapsed_time = time.time() - start_time
            with open(join(chain_path, ('!blocks!' + str(most_recent_block_index))), 'r') as block:
                block_json_string = block.read()
                block_json = json.loads(block_json_string)
                gas_used = block_json["header"]["gasUsed"]

                f = open(text_file_name, "a")
                # block_index, block_size, post_count, time, gas_used
                block_stats = str(most_recent_block_index) + "," + str(most_recent_block_size) + "," + str(post_count) + "," + str(elapsed_time) + "," + str(gas_used) + "\n"
                f.write(block_stats)
                f.close()
                print("Stats: " + block_stats)
    return


def generate_naive_approach(dataset_info, chain_path):

    start_time = time.time()
    uploaded_posts_count = 0

    (dataset, total_posts, total_subreddits) = dataset_info
    print("Generating naive approach")

    backend_contract_address = deploy_backend()
    record_stats(start_time, chain_path, uploaded_posts_count, "naive_stats.txt")

    current_subreddit_count = 0

    # mainchain port
    main_port = 7545

    for subreddit in dataset:
        posts = dataset[subreddit]

        # Create a new community for each subreddit
        posting_contract_address = deploy_community_posting_contract(main_port)
        record_stats(start_time, chain_path, uploaded_posts_count, "naive_stats.txt")

        community_contract_address= deploy_community(posting_contract_address, main_port,
                                                      backend_contract_address,
                                                      posting_contract_address)
        record_stats(start_time, chain_path, uploaded_posts_count, "naive_stats.txt")

        crosslink_community_recipt = crosslink_community(backend_contract_address, "",
                                                         community_contract_address, main_port)
        record_stats(start_time, chain_path, uploaded_posts_count, "naive_stats.txt")

        current_subreddit_count += 1
        posts_length = len(posts)

        for post in posts:
            make_post(backend_contract_address, main_port, "", post)
            record_stats(start_time, chain_path, uploaded_posts_count, "naive_stats.txt")

            uploaded_posts_count += 1
            if uploaded_posts_count % 10 == 0:
                print("Post for this sub:" + str(main_port) + "/" + str(
                    posts_length) + " | Posts total: " + str(uploaded_posts_count) + "/" + str(total_posts))
                print("Currently on subreddit " + str(current_subreddit_count) + "/" + str(total_subreddits))


def generate_sharding_approach(dataset_info, chain_path):
    start_time = time.time()
    uploaded_posts_count = 0

    (dataset, total_posts, total_subreddits) = dataset_info
    print("Generate sharding approach")

    starting_node_port = 6000
    current_node_port = starting_node_port
    subreddit_assigned_port = {}

    backend_contract_address = deploy_backend()
    record_stats(start_time, chain_path, uploaded_posts_count, "sharding_stats.txt")

    # mainchain port
    main_port = 7545

    uploaded_posts_count = 0
    current_subreddit_count = 0

    for subreddit in dataset:
        posts = dataset[subreddit]

        chain_name = start_node(current_node_port, subreddit, "Sidechains/Sharding/")[0]
        chain_name = chain_name[0:-1]
        print(chain_name)

        current_subreddit_count += 1
        current_post_number = 0
        posts_length = len(posts)

        add_community(backend_contract_address, subreddit, current_node_port)

        current_subreddit_count += 1
        posts_length = len(posts)

        for post in posts:
            make_post(backend_contract_address, current_node_port, "", post)
            record_stats(start_time, chain_path, uploaded_posts_count, "sharding_stats.txt")

            current_post_number += 1
            uploaded_posts_count += 1
            if uploaded_posts_count % 10 == 0:
                print("Post for this sub:" + str(current_post_number) + "/" + str(
                    posts_length) + " | Posts total: " + str(uploaded_posts_count) + "/" + str(total_posts))
                print("Currently on subreddit " + str(current_subreddit_count) + "/" + str(total_subreddits))

        subreddit_assigned_port[subreddit] = current_node_port
        stop_node(current_node_port, chain_name)
        current_node_port += 1


def update_interlinks(interlinks):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    block = w3.eth.get_block('latest')
    hash = block['hash'].hex()
    block_index = int(block['number'])
    hash_as_int = int(hash, 16)

    hash_binary = format(hash_as_int, '0>42b')
    leading_zeros = (256 - len(hash_binary))

    for i in range(leading_zeros + 1):
        subchain = interlinks[i].copy()
        subchain.append(block_index)
        interlinks[i] = subchain

    return interlinks


def fetch_block_json(chain_path, block_index):
    with open(join(chain_path, ('!blocks!' + str(block_index))), 'r') as block:
        block_json_string = block.read()
        block_json = json.loads(block_json_string)
        return block_json


def to_byte_array(input):
    return bytearray.fromhex(input[2:len(input)])


def get_block_hash(block):
    header = block["header"]
    parentHash = to_byte_array(header["parentHash"].replace("'", '"'))
    uncleHash = to_byte_array(header["uncleHash"].replace("'", '"'))
    coinbase = to_byte_array(header["coinbase"].replace("'", '"'))
    stateRoot = to_byte_array(header["stateRoot"].replace("'", '"'))
    transactionsTrie = to_byte_array(header["transactionsTrie"].replace("'", '"'))
    receiptTrie = to_byte_array(header["receiptTrie"].replace("'", '"'))
    bloom = to_byte_array(header["bloom"].replace("'", '"'))
    difficulty = to_byte_array(header["difficulty"].replace("'", '"'))
    number = to_byte_array(header["number"].replace("'", '"'))
    gasLimit = to_byte_array(header["gasLimit"].replace("'", '"'))
    gasUsed = to_byte_array(header["gasUsed"].replace("'", '"'))
    timestamp = to_byte_array(header["timestamp"].replace("'", '"'))
    extraData = to_byte_array(header["extraData"].replace("'", '"'))
    mixHash = to_byte_array(header["mixHash"].replace("'", '"'))
    nonce = to_byte_array(header["nonce"].replace("'", '"'))

    filtered_block_array = [
        parentHash, uncleHash, coinbase, stateRoot,
        transactionsTrie, receiptTrie, bloom, difficulty,
        number, gasLimit, gasUsed, timestamp, extraData,
        mixHash, nonce
    ]

    rlp_encoded_string = encode(filtered_block_array)
    block_hash = Web3.keccak(hexstr=("0x" + str(rlp_encoded_string.hex()))).hex()

    return block_hash


def get_block_validator(chain_path, hash):
    if isfile(join(chain_path, ("!blockHashes!" + hash))):
        with open(join(chain_path, ("!blockHashes!" + hash)), 'r') as file:
            block_index = file.read()
            return block_index


def record_stats_nipopow(chain_path, proof_time, nipopow_proof_time, bottom_chain_length, top_chain_length, text_file_name):
    f = "!blocks!length"
    if isfile(join(chain_path, f)):
        with open(join(chain_path, f), 'r') as block_length_file:
            most_recent_block_index = int(block_length_file.read()) - 1

            f = open(text_file_name, "a")
            # block_index, block_size, post_count, time, gas_used
            block_stats = str(most_recent_block_index) + "," + str(proof_time) + "," + str(
                nipopow_proof_time) + "," + str(bottom_chain_length) + "," + str(top_chain_length) + "\n"
            f.write(block_stats)
            f.close()
    return


def validate_nipopow_proof(interlinks, chain_path, security_parameter_m, security_parameter_suffix_k):
    pow_proof_start_time = time.time()

    bottom_chain = interlinks[0]
    for block_index in bottom_chain:
        block_json = fetch_block_json(chain_path, block_index)
        block_hash = get_block_hash(block_json)

        validator_block_index = get_block_validator(chain_path, block_hash)
        if validator_block_index != str(block_index):
            print(bcolors.OKCYAN + "Warning: Block hash invalid!" + bcolors.ENDC)
    pow_proof_time = time.time() - pow_proof_start_time

    # nipopow_proof_generation
    nipopow_proof_start_time = time.time()
    nipopow_proof_time = pow_proof_time
    height_of_structure = 0
    chain_length = len(interlinks[0])
    upper_chain = interlinks[0]

    if chain_length > 0:
        required_nipopow_proof_length = 4 * security_parameter_m * math.log(chain_length, 2)

        if required_nipopow_proof_length < len(interlinks[0]) and security_parameter_suffix_k < len(interlinks[0]):
            for i in range(256):
                if required_nipopow_proof_length < len(interlinks[i]) and security_parameter_suffix_k < len(interlinks[i]):
                    height_of_structure = i

            upper_chain = interlinks[height_of_structure]
            for block_index in upper_chain:
                block_json = fetch_block_json(chain_path, block_index)
                block_hash = get_block_hash(block_json)

                validator_block_index = get_block_validator(chain_path, block_hash)
                if validator_block_index != str(block_index):
                    print(bcolors.OKCYAN + "Warning: Block hash invalid!" + bcolors.ENDC)
                else:
                    print(bcolors.OKCYAN + "Block hash correct :) [index:" + str(block_index) + "," + str(block_hash) + "]" + bcolors.ENDC)
        else:
            bottom_chain = interlinks[0]
            for block_index in bottom_chain:
                block_json = fetch_block_json(chain_path, block_index)
                block_hash = get_block_hash(block_json)

                validator_block_index = get_block_validator(chain_path, block_hash)
                if validator_block_index != str(block_index):
                    print(bcolors.OKCYAN + "Warning: Block hash invalid!" + bcolors.ENDC)
    else:
        bottom_chain = interlinks[0]
        for block_index in bottom_chain:
            block_json = fetch_block_json(chain_path, block_index)
            block_hash = get_block_hash(block_json)

            validator_block_index = get_block_validator(chain_path, block_hash)
            if validator_block_index != str(block_index):
                print(bcolors.OKCYAN + "Warning: Block hash invalid!" + bcolors.ENDC)
    nipopow_proof_time = time.time() - nipopow_proof_start_time

    record_stats_nipopow(chain_path, nipopow_proof_time, pow_proof_time, len(bottom_chain), len(upper_chain), "nipopow_proof_stats.txt")


def generate_nipopow_approach(dataset_info, chain_path):
    start_time = time.time()
    uploaded_posts_count = 0

    (dataset, total_posts, total_subreddits) = dataset_info
    print("Generate sharding approach")

    starting_node_port = 6000
    current_node_port = starting_node_port
    subreddit_assigned_port = {}

    interlinks = [[]] * 256

    security_parameter_m = 6
    security_parameter_suffix_k = 5

    backend_contract_address = deploy_backend()
    record_stats(start_time, chain_path, uploaded_posts_count, "nipopow_stats.txt")
    validate_nipopow_proof(interlinks, chain_path, security_parameter_m, security_parameter_suffix_k)
    interlinks = update_interlinks(interlinks)

    current_subreddit_count = 0

    for subreddit in dataset:
        posts = dataset[subreddit]

        chain_name = start_node(current_node_port, subreddit, "Sidechains/NiPoPoW/")[0]
        chain_name = chain_name[0:-1]
        print(chain_name)

        current_subreddit_count += 1
        current_post_number = 0

        add_community(backend_contract_address, subreddit, current_node_port)

        current_subreddit_count += 1
        posts_length = len(posts)

        for post in posts:
            make_post(backend_contract_address, current_node_port, "", post)
            validate_nipopow_proof(interlinks, chain_path, security_parameter_m, security_parameter_suffix_k)
            record_stats(start_time, chain_path, uploaded_posts_count, "nipopow_stats.txt")
            interlinks = update_interlinks(interlinks)

            current_post_number += 1
            uploaded_posts_count += 1
            if uploaded_posts_count % 10 == 0:
                print("Post for this sub:" + str(current_post_number) + "/" + str(
                    posts_length) + " | Posts total: " + str(uploaded_posts_count) + "/" + str(total_posts))
                print("Currently on subreddit " + str(current_subreddit_count) + "/" + str(total_subreddits))

        subreddit_assigned_port[subreddit] = current_node_port
        stop_node(current_node_port, chain_name)
        current_node_port += 1

    print(interlinks)
    f = open("interlinks_sharding.txt", "a")
    row_count = 0
    for row in interlinks:
        f.write(str(row_count) + ":")
        f.write(str(row) + "\n")
    f.close()


def generate_chains(dataset_path, naive_path):
    dataset, total_posts, total_subreddits = filter_dataset(dataset_path)
    generate_naive_approach((dataset, total_posts, total_subreddits), naive_path)
    generate_sharding_approach((dataset, total_posts, total_subreddits), naive_path)
    generate_nipopow_approach((dataset, total_posts, total_subreddits), naive_path)


# Private Public keys must be set before run.
# IPFS config must be set before run.
dataset_path = "datasets/Reddit_Corpus_2016_01_0.01mb.txt"
naive_chain_path = "C:/Users/John/AppData/Roaming/Ganache/workspaces/Mainchain-0.1MB/chaindata"
generate_chains(dataset_path, naive_chain_path)




