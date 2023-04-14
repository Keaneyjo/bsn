# Analysis Graphs: [
# 1. chain sizes vs number of posts,
# 2. number of blocks vs posts,
# 3. chain creation vs time,
# 4. histogram posts per community
# vs number of shards per community
# 4.5 histogram length per post
# vs block size per post
# 5. costs per post fo reach chain
# 6. number of blocks with x 0 bit starting hashes
# # Potential: Cost per block, Cost per community, Cost per post]
# Evaluations: [Look at each graph and comment on result, comment on frontend]
# maybe an IPFS upload graph
# =
# 7. Cost per per post / block
# 8. Different m security parameters
# 9. Time to validate proof

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew
import os
from os import listdir
from os.path import isfile, join

def chain_sizes_over_time():
    # Time on x
    # Size on y
    print("Generate chain_sizes_per_post_graph")
    # Go through each file and return an array with entries = [time, cumulative_size]
    # 163,8965,0,1.1465864181518555,0x0d0f29
    first_naive_block = 0

    # Naive Chain
    time = 0
    cumulative_size = 0
    naive_times = []
    naive_cumulative_size = []
    exists = []
    i = 0
    with open('naive_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            if entry[0] not in exists:
                cumulative_size += int(int(entry[1]) / 1024)
                naive_times.append(time)
                naive_cumulative_size.append(cumulative_size)
            exists.append(entry[0])
    plt.plot(naive_times, naive_cumulative_size, label=str("naive"))

    # Sharding Chain
    time = 0
    cumulative_size = 0
    sharding_times = []
    sharding_cumulative_size = []
    exists = []
    i = 0
    with open('sharding_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            if entry[0] not in exists:
                cumulative_size += int(int(entry[1]) / 1024)
                sharding_times.append(time)
                sharding_cumulative_size.append(cumulative_size)
            exists.append(entry[0])
    # 960,8968,0,1.393059253692627,0x0d0f29
    plt.plot(sharding_times, sharding_cumulative_size, label=str("sharding"))

    # NiPoPoW Chain
    cumulative_size = 0
    nipopow_times = []
    nipopow_cumulative_size = []
    upper_chain_block_count = []
    nipopow_size_at_blocks = []
    with open('nipopow_proof_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            upper_chain_block_count.append(int(entry[4]))

    block_count = 0
    with open('nipopow_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])

            cumulative_size += int(int(entry[1]) / 1024)
            nipopow_size_at_blocks.append(cumulative_size)
            upper_chain_blocks_amount = upper_chain_block_count[block_count]
            nipopow_cumulative_size.append(nipopow_size_at_blocks[upper_chain_blocks_amount])
            nipopow_times.append(time)
            block_count += 1
    plt.plot(nipopow_times, nipopow_cumulative_size, label=str("nipopow"))

    plt.title("Chain Sizes Over Time")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Chain Size (kilobytes)')
    plt.legend()
    plt.show()

    print(naive_times[len(naive_times)-1])
    print(sharding_times[len(sharding_times) - 1])
    print(nipopow_times[len(nipopow_times) - 1])

    print(sum(naive_times))
    print(sum(sharding_times))
    print(sum(nipopow_times))

    print(naive_cumulative_size[len(naive_cumulative_size) - 1])
    print(sharding_cumulative_size[len(sharding_cumulative_size) - 1])
    print(nipopow_cumulative_size[len(nipopow_cumulative_size) - 1])


def number_of_blocks_per_post():
    # Time on x
    # Size on y
    print("Generate chain_sizes_per_post_graph")
    # Go through each file and return an array with entries = [time, cumulative_size]
    # 163,8965,0,1.1465864181518555,0x0d0f29
    first_naive_block = 0

    # Naive Chain
    total_blocks_per_post = []
    total_block_count = 0
    last_post_count = -1
    exists = []
    with open('naive_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            total_block_count += 1
            post_count = int(entry[2])
            if last_post_count != post_count:
                last_post_count = post_count
                total_blocks_per_post.append(total_block_count)
    plt.plot(range(len(total_blocks_per_post)), total_blocks_per_post, label=str("naive"))
    print(total_blocks_per_post[-1])

    # Sharding Chain
    total_blocks_per_post = []
    total_block_count = 0
    last_post_count = -1
    exists = []
    earliest_block = -1
    with open('sharding_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            if earliest_block == -1:
                earliest_block = int(entry[0])
            current_block = int(entry[0])
            post_count = int(entry[2])
            if last_post_count != post_count:
                last_post_count = post_count
                total_blocks_per_post.append(current_block - earliest_block)
            # exists.append(entry[0])
    plt.plot(range(post_count + 1), total_blocks_per_post, label=str("sharding"))
    print(total_blocks_per_post[-1])

    # # NiPoPoW Chain
    # total_blocks_per_post = []
    # total_block_count = 0
    # exists = []
    # post_count = 0
    # with open('nipopow_proof_stats.txt') as file:
    #     for line in file:
    #         entry = line.split(",")
    #         post_count += 1
    #         total_blocks_per_post.append(int(entry[4]))
    # plt.plot(range(post_count), total_blocks_per_post, label=str("nipopow"))
    # print(total_blocks_per_post[-1])
    # NiPoPoW Chain
    total_blocks_per_post = []
    nipopow_blocks_per_post = []
    upper_chain_block_count = []
    nipopow_post_at_blocks = []
    with open('nipopow_proof_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            upper_chain_block_count.append(int(entry[4]))

    block_count = 0
    last_post_count = 0
    with open('nipopow_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            post_count = int(entry[2])
            total_blocks_per_post.append(block_count)
            if last_post_count != post_count:
                last_post_count = post_count
                upper_chain_blocks_amount = upper_chain_block_count[block_count]
                nipopow_blocks_per_post.append(total_blocks_per_post[upper_chain_blocks_amount])
                nipopow_post_at_blocks.append(block_count)
            block_count += 1
    plt.plot(range(last_post_count), nipopow_blocks_per_post, label=str("nipopow"))

    plt.title("Number Of Blocks Per Post")
    plt.xlabel('Total Posts')
    plt.ylabel('Number of Blocks Per Chain')
    plt.legend()
    plt.show()

def chain_sizes_per_post():
    # Naive Chain
    total_size_per_post = []
    cumulative_size = 0
    last_post_count = -1
    exists = []
    with open('naive_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            cumulative_size += int(int(entry[1]) / 1024)
            post_count = int(entry[2])
            if last_post_count != post_count:
                last_post_count = post_count
                total_size_per_post.append(cumulative_size)
    plt.plot(range(len(total_size_per_post)), total_size_per_post, label=str("naive"))
    print(total_size_per_post[-1])

    # Sharding Chain
    total_size_per_post = []
    last_post_count = -1
    cumulative_size = 0
    last_block = -1
    with open('sharding_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            current_block = int(entry[0])
            if last_block != current_block:
                last_block = current_block
                cumulative_size += int(int(entry[1]) / 1024)
            post_count = int(entry[2])
            if last_post_count != post_count:
                last_post_count = post_count
                total_size_per_post.append(cumulative_size)
            # exists.append(entry[0])
    plt.plot(range(post_count + 1), total_size_per_post, label=str("sharding"))
    print(total_size_per_post[-1])

    # # NiPoPoW Chain
    # total_blocks_per_post = []
    # total_block_count = 0
    # exists = []
    # post_count = 0
    # with open('nipopow_proof_stats.txt') as file:
    #     for line in file:
    #         entry = line.split(",")
    #         post_count += 1
    #         total_blocks_per_post.append(int(entry[4]))
    # plt.plot(range(post_count), total_blocks_per_post, label=str("nipopow"))
    # print(total_blocks_per_post[-1])
    # NiPoPoW Chain
    cumulative_size = 0
    total_size_per_post = []
    nipopow_size_per_post = []
    upper_chain_block_count = []
    with open('nipopow_proof_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            upper_chain_block_count.append(int(entry[4]))

    block_count = 0
    last_post_count = 0
    with open('nipopow_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            post_count = int(entry[2])
            cumulative_size += int(int(entry[1]) / 1024)
            total_size_per_post.append(cumulative_size)
            if last_post_count != post_count:
                last_post_count = post_count

                upper_chain_blocks_amount = upper_chain_block_count[block_count]
                nipopow_size_per_post.append(total_size_per_post[upper_chain_blocks_amount])
            block_count += 1
    plt.plot(range(last_post_count), nipopow_size_per_post, label=str("nipopow"))

    plt.title("Chain Size Per Post")
    plt.xlabel('Total Posts')
    plt.ylabel('Chain Size (Kilobytes)')
    plt.legend()
    plt.show()

# def chain_sizes_per_post():
#
#     # Naive Chain
#     last_post_count = -1
#     cumulative_size = 0
#     total_size_per_post = []
#     exists = []
#     with open('naive_stats.txt') as file:
#         for line in file:
#             entry = line.split(",")
#             if entry[0] not in exists:
#                 cumulative_size += int(int(entry[1]) / 1024)
#                 post_count = int(entry[2])
#                 if last_post_count != post_count:
#                     last_post_count = post_count
#                     total_size_per_post.append(cumulative_size)
#             exists.append(entry[0])
#     plt.plot(range(len(total_size_per_post)), total_size_per_post, label=str("naive"))
#
#     # Sharding Chain
#     cumulative_size = 0
#     total_size_per_post = []
#     last_post_count = -1
#     exists = []
#     with open('sharding_stats.txt') as file:
#         for line in file:
#             entry = line.split(",")
#             if entry[0] not in exists:
#                 cumulative_size += int(int(entry[1]) / 1024)
#                 post_count = int(entry[2])
#                 if last_post_count != post_count:
#                     last_post_count = post_count
#                     total_size_per_post.append(cumulative_size)
#             exists.append(entry[0])
#     plt.plot(range(post_count + 1), total_size_per_post, label=str("sharding"))
#
#     # NiPoPoW Chain
#     cumulative_size = 0
#     upper_chain_block_count = []
#     nipopow_size_at_blocks = []
#     total_size_per_post = []
#     with open('nipopow_proof_stats.txt') as file:
#         for line in file:
#             entry = line.split(",")
#             upper_chain_block_count.append(int(entry[4]))
#
#     block_count = 0
#     with open('nipopow_stats.txt') as file:
#         for line in file:
#             entry = line.split(",")
#
#             cumulative_size += int(int(entry[1]) / 1024)
#             nipopow_size_at_blocks.append(cumulative_size)
#             post_count = int(entry[2])
#             if last_post_count != post_count:
#                 last_post_count = post_count
#                 upper_chain_blocks_amount = upper_chain_block_count[block_count]
#                 total_size_per_post.append(nipopow_size_at_blocks[upper_chain_blocks_amount])
#
#             block_count += 1
#
#     plt.plot(range(len(total_size_per_post)), total_size_per_post, label=str("nipopow"))
#
#     plt.title("Chain Size Per Post")
#     plt.xlabel('Total Posts')
#     plt.ylabel('Chain Size (Kilobytes)')
#     plt.legend()
#     plt.show()


def mainchain_cost_over_time():
    # Naive Chain
    cost_over_time = []
    cumulativate_cost = 0
    times = []
    cost_divider = 1E9
    with open('naive_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            cumulativate_cost += float(int(entry[4], 16) / cost_divider)
            times.append(time)
            cost_over_time.append(cumulativate_cost)
    plt.plot(times, cost_over_time, label=str("naive"))
    print(cost_over_time[-1])

    # Sharding Chain
    cost_over_time = []
    cumulativate_cost = 0
    times = []
    with open('sharding_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            cumulativate_cost += float(int(entry[4], 16) / cost_divider)
            times.append(time)
            cost_over_time.append(cumulativate_cost)
    plt.plot(times, cost_over_time, label=str("sharding"))
    print(cost_over_time[-1])

    # NiPoPoW Chain
    cost_over_time = []
    cumulativate_cost = 0
    times = []
    with open('nipopow_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            cumulativate_cost += float(int(entry[4], 16) / cost_divider)
            times.append(time)
            cost_over_time.append(cumulativate_cost)
    plt.plot(times, cost_over_time, label=str("nipopow"))
    print(cost_over_time[-1])

    plt.title("Mainchain Cost Over Time")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Gas Cost (ETH)')
    plt.legend()
    plt.show()

def mainchain_cost_per_block():
    # Naive Chain
    cost_over_time = []
    times = []

    cost_divider = 1E9

    # One gas = 1E-9 Eth
    # 1E-9 + 1E8 = 1E

    with open('naive_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            cost = float(int(entry[4], 16) / cost_divider)
            times.append(time)
            cost_over_time.append(cost)
    plt.plot(times, cost_over_time, label=str("naive"))

    # Sharding Chain
    cost_over_time = []
    times = []
    with open('sharding_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            cost = float(int(entry[4], 16) / cost_divider)
            times.append(time)
            cost_over_time.append(cost)
    plt.plot(times, cost_over_time, label=str("sharding"))

    # NiPoPoW Chain
    cost_over_time = []
    times = []
    with open('nipopow_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            time = float(entry[3])
            cost = float(int(entry[4], 16) / cost_divider)
            times.append(time)
            cost_over_time.append(cost)
    plt.plot(times, cost_over_time, label=str("nipopow"))

    plt.title("Mainchain Cost Per Block")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Gas Cost (ETH)')
    plt.legend()
    plt.show()

def time_to_validate_proof():
    # NiPoPoW Chain
    block_count = 0
    pow_times = []
    nipopow_times = []

    with open('nipopow_proof_stats.txt') as file:
        for line in file:
            entry = line.split(",")
            pow_time = float(entry[2])
            nipopow_time = float(entry[1])
            pow_times.append(pow_time)
            nipopow_times.append(nipopow_time)
    plt.plot(range(len(pow_times)), pow_times, label=str("pow"))
    plt.plot(range(len(pow_times)), nipopow_times, label=str("nipopow"))

    plt.title("Chain Proof Validation Times")
    plt.xlabel('Iteration')
    plt.ylabel('Proof Validation Time (Seconds)')
    plt.legend()
    plt.show()

def number_of_blocks_with_T_leading_zeros():

    leading_zeros_count = []
    with open('interlinks_sharding.txt') as file:
        for line in file:
            entry = line.split(":")
            t_leading_zeros = int(entry[0])
            blocks_at_level_t = entry[1][1:len(entry[1])-2].split(", ")
            if entry[1] != '[]\n':
                leading_zeros_count.append(len(blocks_at_level_t))

    print(leading_zeros_count)
    fig, ax = plt.subplots()
    labels, counts = np.unique(leading_zeros_count, return_counts=True)
    bars = ax.bar(range(len(leading_zeros_count)), leading_zeros_count, align='center', alpha=0.5)
    ax.bar_label(bars)

    ax.set_xticks(np.arange(len(leading_zeros_count)))
    ax.set_xticklabels(range(len(leading_zeros_count)))

    # plt.bar(range(len(leading_zeros_count)), leading_zeros_count, align='center', alpha=0.5)
    plt.title("Distribution of e extra leading zeros")
    plt.xlabel('Hashes with extra e zeros')
    plt.ylabel('Block Count')
    plt.show()


from main import filter_dataset

def posts_per_community_histogram(path):
    dataset, total_posts, total_subreddits = filter_dataset(path)
    posts_per_community = []
    for subreddit in dataset:
        posts = dataset[subreddit]
        posts_per_community.append(len(posts))

    # bins = int(skew(posts_per_community))
    # plt.hist(posts_per_community, bins=bins)
    # plt.title("Posts per Community")
    # plt.xlabel('Number of Communities with x Posts')
    # plt.ylabel('Number of Posts')
    # plt.show()

    fig, ax = plt.subplots()
    labels, counts = np.unique(posts_per_community, return_counts=True)
    bars = ax.bar(labels, counts, align='center', alpha=0.5)
    # bars = ax.bar(range(len(posts_per_community)), posts_per_community, align='center', alpha=0.5)
    ax.bar_label(bars)
    plt.gca().set_xticks(labels)
    plt.title("Posts per Community")
    plt.xlabel('Number of Posts')
    plt.ylabel('Number of Community with X Posts')
    plt.show()

    # fig, ax = plt.subplots()
    # # posts_per_community.sort()
    # bars = ax.bar(range(len(posts_per_community)), posts_per_community, align='center', alpha=0.5)
    # ax.bar_label(bars)
    # # plt.bar(range(len(leading_zeros_count)), leading_zeros_count, align='center', alpha=0.5)
    # plt.title("Posts per Community")
    # plt.xlabel('Each Community')
    # plt.ylabel('Number of Posts')
    # plt.show()


def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def size_per_shard_histogram(path):

    size_of_shards = []

    for folder in listdir(path):
        # This line from here:
        # https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
        size_of_shards.append(int(get_size(join(path, folder)) / 1024))

    # fig, ax = plt.subplots()
    # labels, counts = np.unique(size_of_shards, return_counts=True)
    # bars = ax.bar(labels, counts, align='center', alpha=0.5)
    # ax.bar_label(bars)
    # plt.gca().set_xticks(labels)
    # plt.title("Makeup of Shards")
    # plt.xlabel('Number of Shards of Size Y')
    # plt.ylabel('Size of Shards (Kilobyte)')
    # plt.show()

    bins = int(skew(size_of_shards) * 25)
    plt.hist(size_of_shards, bins=bins)
    plt.title("Makeup of Shards")
    plt.ylabel('Number of Shards of Size Y')
    plt.xlabel('Size of Shards (Kilobyte)')
    plt.show()


# chain_sizes_over_time()
# number_of_blocks_per_post()
# chain_sizes_per_post()
# mainchain_cost_over_time()
# mainchain_cost_per_block()
# time_to_validate_proof()
# number_of_blocks_with_T_leading_zeros()
#
# dataset_path = "datasets/Reddit_Corpus_2016_01_0.1mb.txt"
# posts_per_community_histogram(dataset_path)
# sidechains_path = "chainSidechains/NiPoPoW"
# size_per_shard_histogram(sidechains_path)

# Analysis Graphs: [
# 4. histogram posts per community vs number of shards per community
# Size of chain with different m's

print(1166572 / 1E9)

# 1 gas = 0.000000001 Eth