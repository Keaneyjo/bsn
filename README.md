# Blockchain-based Social Network

## For the frontend implementation: 
In the project directory bsn/ run:
### `npm install`

Then again in directory bsn/bsn/ run:
### `npm install`

Then to open the app run in bsn/bsn:
### `npm install`

In order for the application to work, a Ganache GUI instance at RPC Server HTTP://127.0.0.1:7545 must be running
In order for communities or posts to be created a shard instance must be run on a free port via Ganache CLI

More info on running Ganache CLI shards is available [here](https://github.com/trufflesuite/ganache#readme)
Or by searching the commands in the analytical folder.

## For the analytical implementation
Enter directory analytical/

In order for the application to work, a Ganache GUI instance at RPC Server HTTP://127.0.0.1:7545 must be running
In order for communities or posts to be created a shard instance must be run on a free port via Ganache CLI

More info on running Ganache CLI shards is available [here](https://github.com/trufflesuite/ganache#readme)
Or by searching the commands in the analytical folder.

If shards have not been generated:
Configure wallet public and private key pair based on Ganache CLI
Configure IPFS key via infura

Then after installing requirements run:
### `python main.py`

Then to generate graphs run:
### `python generate_graphs.py`