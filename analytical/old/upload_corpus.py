
import json
import requests
from web3 import Web3

# IPFS auths
proj_id = '2MWnLdSYBRH5iyPG53RVgJbXu3r'
proj_secret = 'd1174b0df2ccc7759932bfb0fe84e2a9'

chain_id = 1337
address = "0x2d829E5aCDD12E398087245de3e044177f8629a6"
private = "0x058297ff32e8d319a97150976e7668b2c5d16384d2f97e6dbedd3a44b9e2864b"

sidechain_address = "0x448A827221612A314e4805486de959B3499cD6b7"
sidechain_private = "0x714c23764123926619a6a06b06a591089118ff4ba4bce8258cae6b8f0ca43459"

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



upload_one_hundred_posts_to_one_sidechain()
