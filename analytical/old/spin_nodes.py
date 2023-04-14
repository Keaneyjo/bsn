import subprocess
from subprocess import Popen
import os
import shutil
from subprocess import PIPE
import math
import numpy as np

print("Hellow World!")

# > # 1. Run a cmd command that opens the terminal
# > # 2. Make sure I can close that terminal to stop the daemons - instead use ganache stop instances <name>
# > # 3. Command to make a folder for blockchain storage
# > # 4. Command to make multiple of the folder above
# > # 5. Command to clear out these folders
# 6. Spin up one blockchain node
# 7. Spin up 10 nodes
# 8. Spin up 100, 200, 500, 1000 nodes

# 1
# os.system('cmd /k "dir"')
# os.rmdir('chain4')


# True - turn on nodes
# False - turn off nodes
# turn_on_nodes = False

# True - deletes the chains
# False - keeps the chains
# delete_chains = False

starting_port = 6000

# 0 - turn on nodes
# 1 - turn off nodes, keep chains
# 2 - turn off nodes, delete chains
status = 2

no_nodes = 1

# if turn_on_nodes:
if status == 0:
    commands = [Popen("ganache --chain.allowUnlimitedContractSize=true --port={i:d} --database.dbPath=chain{i:d} --miner.instamine eager -D".format(i=starting_port + i), shell=True,
                stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
                for i in range(no_nodes)]

    exitcodes = [p.wait() for p in commands]
    results = [p.communicate() for p in commands]
    print(results)
    print("Exitcodes should equal 0. Exitcodes = " + str(np.sum(exitcodes)))
    print(exitcodes)

    chain_names = open("chain_names.txt", "w")
    for names in results:
        chain_names.write(names[0])
    chain_names.close()

if status == 1 or status == 2:
    # print("Stopping nodes")
    # # for i in range(0, no_nodes, 1):
    # #    command = ganache
    # commands = [Popen("ganache instances stop {chain_name:s}".format(chain_name=starting_port + i), shell=True,
    #             stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    #             for i in range(2)]
    # shutil.rmtree("chain4")

    # #!/usr/bin/env python
    from subprocess import Popen

    chain_names_file = open('chain_names.txt', 'r')
    chain_names = chain_names_file.readlines()

    count = 0
    names = []
    # Strips the newline character
    for name in chain_names:
        count += 1
        names.append(name[0:-1])
        print(name[0:-1])

    commands = [Popen("ganache instances stop {chain_name:s}".format(chain_name=names[i]), shell=True,
                      stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
                for i in range(no_nodes)]

    print("Turning off chains....")
    exitcodes = [p.wait() for p in commands]
    print(exitcodes)
    results = [p.communicate() for p in commands]
    print(results)


if status == 2:
    print("Removing Chains....")

    for i in range(no_nodes):
        shutil.rmtree('chain{i:s}'.format(i=str(starting_port + i)))
    # commands = [Popen('shutil.rmtree("chain{i:s})'.format(i=str(starting_port + i)), shell=True,
    #             stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    #             for i in range(2)]

    # exitcodes = [p.wait() for p in commands]
    # print(exitcodes)
    # results = [p.communicate() for p in commands]
    # print(results)

# shutil.rmtree("chain4")
    # # run commands in parallel
    # processes = [Popen("echo {i:d}; sleep 2; echo {i:d}".format(i=i), shell=True)
    #              for i in range(5)]
    # # collect statuses
    # exitcodes = [p.wait() for p in processes]
