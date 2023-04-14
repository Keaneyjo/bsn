# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# from convokit import Corpus, download
# corpus = Corpus(filename=download("reddit-corpus-small"))
# corpus.print_summary_stats()


# path = "C:\Users\John\Downloads\reddit-corpus.corpus\reddit-corpus\utterances.jsonl"
path = "C:/Users/John/Downloads/reddit-corpus.corpus/reddit-corpus/utterances.jsonl"
path = "C:/Users/John/Downloads/RC_2005-12 - newjson.jsonl"
path = "C:/Users/John/Downloads/RC_2005-12.jsonl"
path = "C:/Users/John/Downloads/RC_2009-04/RC_2009-04.jsonl"

import json

# with open('./data/my_filename.jsonl', 'r') as json_file:
# with open(path, 'r') as json_file:
#     json_list = list(json_file)
#
# subreddits = {}

i = 0

# for json_str in json_list:
#     # result = json.loads(json_str)
#     #
#     # meta = result['meta']
#     # subreddit = meta['subreddit']
#     # if subreddit in subreddits:
#     #     subreddits[subreddit] = subreddits[subreddit] + 1
#     # else:
#     #     subreddits[subreddit] = 1
#     result = json.loads(json_str)
#
#     subreddit = result['subreddit']
#     if subreddit in subreddits:
#         subreddits[subreddit] = subreddits[subreddit] + 1
#     else:
#         subreddits[subreddit] = 1
#
# import json

# with open(path, 'r') as data_file:
#     json_data = data_file.read()
#     print(json_data)
#
# data = json.loads(json_data)
# print(data)

# with open(path) as f:
#     for jsonObj in f:
#         studentDict = json.loads(jsonObj)
#         print(studentDict)
#         # studentsList.append(studentDict)
#
# data = json.load(open(path, 'r'))
# print(subreddits)

tweets = []
subreddits = []
subs = {}
number_of_subs = 0
non_deleted_entries = 0
more_than_five_hundred_chars = 0
more_than_eight_hundred_chars = 0
more_than_one_thousand_chars = 0
for line in open(path, 'r'):
    # if i == 1000:
    #     break
    i += 1
    #tweets.append(json.loads(line))
    # print(json.loads(line))
    entry = json.loads(line)
    subreddit = entry['subreddit']
    if entry['body'] != "[deleted]":
        non_deleted_entries += 1
    if len(entry['body']) > 500:
        more_than_five_hundred_chars += 1
    if len(entry['body']) > 1000:
        more_than_one_thousand_chars += 1
    if len(entry['body']) > 800:
        more_than_eight_hundred_chars += 1


    if subreddit in subs:
        subs[subreddit] = subs[subreddit] + 1
    else:
        number_of_subs += 1
        subs[subreddit] = 1
print("Number of entries", i)
print("Number of non-deleted", non_deleted_entries)
print("Number of posts with more than 500 characters", more_than_five_hundred_chars)
print("Number of posts with more than 1000 characters", more_than_one_thousand_chars)
print("Number of posts with more than 800 characters", more_than_eight_hundred_chars)
print("Number of non-deleted", non_deleted_entries)
print("Number of subs", number_of_subs)
print(subs)
max_value = max(subs.values())
print(max_value)


import matplotlib.pyplot as plt
#plt.bar(subs.keys(), subs.values(), color='g')

# mylist = [key for key, val in subs.items() for _ in range(val)]
# plt.hist(mylist, bins=20)
# plt.hist(mylist)
#plt.show()

# a = []
i = 0
less_than_ten, greater_than_ten, less_than_one_hun, less_one_tho = 0, 0, 0, 0
for entry in subs:

    if subs[entry] < 100:
        less_than_one_hun += 1
    if subs[entry] < 1000:
        less_one_tho += 1

    if subs[entry] < 10:
        less_than_ten += 1
    else:
        greater_than_ten += 1

print("Subs with less than 10 posts: ", less_than_ten)
print("Subs with more than 10 posts: ", greater_than_ten)
print(less_one_tho)
print(less_than_one_hun)
#
# import matplotlib.pyplot as plt

# plt.hist(a)
# plt.show()
