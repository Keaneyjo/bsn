import requests
import os
import json

proj_id = '2MWnLdSYBRH5iyPG53RVgJbXu3r'
proj_secret = 'd1174b0df2ccc7759932bfb0fe84e2a9'

# make sure to use absolute path
dir_name = '/Users/christian/Desktop/Infura/IPFS/folder_test/'
dir_name = "C:/Users/John/Music/ipfs_test/"

# items = {}
# for f in os.listdir(dir_name):
#     item = open(dir_name + f, 'rb')
#     items[f] = item
#
# # replace above for loop with the code below for checking sub-directories
# # for root, dirs, files in os.walk(dir_name):
# #     for file in files:
# #         filepath = root + os.sep + file
# #         item = open(filepath, 'rb')
# #         items[file]= item
#
# response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=true&wrap-with-directory=true",
#                          auth=(proj_id, proj_secret),files=items)
#
# # for printing the CIDs in the console:
# dec = json.JSONDecoder()
# i = 0
# while i < len(response.text):
#     data, s = dec.raw_decode(response.text[i:])
#     i += s + 1
#     if data['Name'] == '':
#         data['Name'] = 'Folder CID'
#     print("%s: %s" % (data['Name'], data['Hash']))
#
# # url: https://an-nft-marketplace.infura-ipfs.io/ipfs/QmUjnR3NzUgoWcJdL8YfaSD3aYHcWRb9bXi75wfb95Ppsm

# Trying to upload one file at a time now:
files = {
'file': ("This is some sample text John. Listening to MHA followed by GGD"),
}

response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=false",
                         auth=(proj_id, proj_secret), files=files)
p = response.json()
hash = p['Hash']
print(p['Name'])
print(hash)
print(response.json)
#
# dec = json.JSONDecoder()
# i = 0
# while i < len(response.text):
#     data, s = dec.raw_decode(response.text[i:])
#     i += s + 1
#     if data['Name'] == '':
#         data['Name'] = 'Folder CID'
#     print("%s: %s" % (data['Name'], data['Hash']))

response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=false",
                         auth=(proj_id, proj_secret), files=files)
p = response.json()
hash = p['Hash']
print(p['Name'])
print(len(p['Hash']))
print(hash)
print(response.json)