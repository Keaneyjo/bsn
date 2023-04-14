import os
from os import listdir
from os.path import isfile, join

import math

def length_of_nipopow_chain(path = "Mainchain/chaindata"):
    print("Calculating length of nipopow chain")

    count_of_blocks_with_e_extra_leading_zeros = {}
    bytes_of_blocks_with_e_extra_leading_zeros = {}

    # Open up the folder,
    # Create a dictionary for counting the blocks with extra leading zeros:
    # {"0": 140, "1": 70}
    # At the same time create a dictionary that counts the total amount of mbs that blocks with z extra leading zeros:
    # {"0": 1400kb, "1": 700kb}

    # Open the file and get the number of blocks
    # Go through the folder and get the hash of each block

    # try:
    #     with open(path + "/!blocks!length", 'r') as file:
    #         number_of_blocks = file.read()
    # except:
    #     print("Unable to find number of blocks.")
    #     number_of_blocks = -1

    # !blockHashes!0x0a2b714be4727fdee6ae9bea7b9918ff48a16f60ffeaffd02942e9bf28dff1c0

    for f in listdir(path):
        if isfile(join(path, f)) and f[0:13] == "!blockHashes!":
            # Use 15:len(f) to remove the extra 0x at the start
            hash = f[15:len(f)]
            hash_as_int = int(hash, 16)

            # Convert hex string to binary:
            # https://stackoverflow.com/questions/1425493/convert-hex-to-binary
            hash_binary = format(hash_as_int, '0>42b')
            # This converts string to 256 long binary

            # When converting to binary above it doesn't add the leading zeros to make it a full 256 bits
            # So 256 - len(hash_binary) will give us the number of leading zeros
            leading_zeros = (256 - len(hash_binary))

            if leading_zeros in count_of_blocks_with_e_extra_leading_zeros:
                count_of_blocks_with_e_extra_leading_zeros[leading_zeros] += 1
            else:
                count_of_blocks_with_e_extra_leading_zeros[leading_zeros] = 1

            with open(join(path, f), 'r') as file:
                block_index = file.read()
                size_of_block = os.path.getsize(join(path, '!blocks!' + str(block_index)))
                if leading_zeros in bytes_of_blocks_with_e_extra_leading_zeros:
                    bytes_of_blocks_with_e_extra_leading_zeros[leading_zeros] += size_of_block
                else:
                    bytes_of_blocks_with_e_extra_leading_zeros[leading_zeros] = size_of_block

    print(count_of_blocks_with_e_extra_leading_zeros)
    print(bytes_of_blocks_with_e_extra_leading_zeros)
    print("Total Blocks: " + str(sum(count_of_blocks_with_e_extra_leading_zeros.values())))
    print("Total Size of Blocks: " + str(sum(bytes_of_blocks_with_e_extra_leading_zeros.values())))
    temp_total_blocks = sum(count_of_blocks_with_e_extra_leading_zeros.values())
    for i in range(9):
        print(temp_total_blocks)
        temp_total_blocks = math.log(temp_total_blocks, 2)



def length_of_naive_chain(path = "Sidechains/chaindata"):
    print("Calculating length of naive chain (Implementation #1)")

    count_of_blocks_with_e_extra_leading_zeros = {}
    bytes_of_blocks_with_e_extra_leading_zeros = {}


    for f in listdir(path):
        if isfile(join(path, f)) and f[0:13] == "!blockHashes!":
            # Use 15:len(f) to remove the extra 0x at the start
            hash = f[15:len(f)]
            hash_as_int = int(hash, 16)

            # Convert hex string to binary:
            # https://stackoverflow.com/questions/1425493/convert-hex-to-binary
            hash_binary = format(hash_as_int, '0>42b')
            # This converts string to 256 long binary

            # When converting to binary above it doesn't add the leading zeros to make it a full 256 bits
            # So 256 - len(hash_binary) will give us the number of leading zeros
            leading_zeros = (256 - len(hash_binary))

            if leading_zeros in count_of_blocks_with_e_extra_leading_zeros:
                count_of_blocks_with_e_extra_leading_zeros[leading_zeros] += 1
            else:
                count_of_blocks_with_e_extra_leading_zeros[leading_zeros] = 1

            with open(join(path, f), 'r') as file:
                block_index = file.read()
                size_of_block = os.path.getsize(join(path, '!blocks!' + str(block_index)))
                if leading_zeros in bytes_of_blocks_with_e_extra_leading_zeros:
                    bytes_of_blocks_with_e_extra_leading_zeros[leading_zeros] += size_of_block
                else:
                    bytes_of_blocks_with_e_extra_leading_zeros[leading_zeros] = size_of_block

    print(count_of_blocks_with_e_extra_leading_zeros)
    print(bytes_of_blocks_with_e_extra_leading_zeros)
    print("Total Blocks: " + str(sum(count_of_blocks_with_e_extra_leading_zeros.values())))
    print("Total Size of Blocks: " + str(sum(bytes_of_blocks_with_e_extra_leading_zeros.values())))
    temp_total_blocks = sum(count_of_blocks_with_e_extra_leading_zeros.values())
    for i in range(9):
        print(temp_total_blocks)
        temp_total_blocks = math.log(temp_total_blocks, 2)




# def trim_dataset(path):
#
#     corpus_file = open("Reddit_Corpus_2016_01_1mb.txt", "w")
#
#     for line in open(path, 'r'):
#         # entry = json.loads(line)
#         corpus_file.write(line)
#
#         file_size = os.path.getsize("Reddit_Corpus_2016_01_1mb.txt")
#         print(file_size)
#         # Desired file size of 50mb
#         # 50mb == 5e+7
#         # 100mb == 10e+7
#         if file_size > 1E+6:
#             corpus_file.close()
#             break
#
#     for line in open(path, 'r'):
#         entry = json.loads(line)




#



length_of_nipopow_chain()

def check_polylog():
    normal = []
    polylogs = []
    logs = []
    c = 4

    for i in range(1, 1001, 100):
        normal.append(i)
        logs.append(math.log(i))
        polylog_sum = i
        for i in range(1, c):
            if polylog_sum > 0:
                polylog_sum = math.log(polylog_sum, 2)
        polylogs.append(polylog_sum)

    print(normal)
    print(logs)
    print(polylogs)

# check_polylog()


def draw_skip_list(n):
    levels = int(max(0, math.log(n, 2)))
    blocks_per_level = [0] * levels
    for level in range(levels, 0, -1):
        print(str(level) + "|", end='')
        for place in range(n):
            if place % 2**level == 0:
                blocks_per_level[level - 1] += 1
                print(level, end='')
            else:
                print(" ", end='')
        print()
    print(blocks_per_level)


# draw_skip_list(64)
