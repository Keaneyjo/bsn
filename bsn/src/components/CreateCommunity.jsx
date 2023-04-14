import React, { Component } from 'react';
import { TextField, Box, Button, Container } from '@mui/material';
import Web3 from 'web3';


export default class CreateCommunity extends Component {

    constructor(props) {
        super(props)
        this.state = {
            name: '',
            port: ''
        }

        this.createCommunity = this.createCommunity.bind(this);
    }

    createCommunity = async () => {

        let web3 = new Web3('HTTP://127.0.0.1:' + this.state.port)

        let contract = require('../abis/Posting.json');
        let abi = contract.abi;
        let bytecode = contract.data.bytecode.object;

        const auth = {
            privateKey: this.props.privateKey,
            address: this.props.publicKey,
        };

        console.log(`Attempting to deploy posting contract from account ${auth.address}`);

        const postingContract = new web3.eth.Contract(abi);

        const postingContractTx = postingContract.deploy({
            data: bytecode,
            arguments: [parseInt(this.state.port)]
        });

        const postingTransaction = await web3.eth.accounts.signTransaction(
            {
                data: postingContractTx.encodeABI(),
                gas: 10000000,
                // gas: await postingContractTx.estimateGas(),
            },
            auth.privateKey
        );

        const postingReceipt = await web3.eth.sendSignedTransaction(postingTransaction.rawTransaction);
        console.log(`Posting contract for new community created at address: ${postingReceipt.contractAddress}`);


        // Now creating the actual community contract
        contract = require('../abis/Community.json');
        abi = contract.abi;
        bytecode = contract.data.bytecode.object;

        console.log(`Creating community of name: ${this.state.name} at port ${this.state.port}.`);
        console.log(`Attempting to deploy from account ${auth.address}`);

        const communityContract = new web3.eth.Contract(abi);

        const communityContractTx = communityContract.deploy({
            data: bytecode,
            arguments: [this.state.name, parseInt(this.state.port), this.props.backendContractAddress, postingReceipt.contractAddress]
        });

        const signedCommunityContractTx = await web3.eth.accounts.signTransaction(
            {
                data: communityContractTx.encodeABI(),
                gas: 10000000,
            },
            auth.privateKey
        );

        const communityContractTxReceipt = await web3.eth.sendSignedTransaction(signedCommunityContractTx.rawTransaction);
        console.log(`Community created at address: ${communityContractTxReceipt.contractAddress}`);


        /////////////////
        // After community has been deployed to side chain, need to add a block to main chain which points to side chain.
        web3 = new Web3('HTTP://127.0.0.1:7545');

        contract = require('../abis/Backend.json');
        abi = contract.abi;
        bytecode = contract.data.bytecode.object;

        const backend = new web3.eth.Contract(abi, this.props.backendContractAddress);

        let estimatedGasCost = await backend.methods.createCommunity(this.state.name, communityContractTxReceipt.contractAddress, parseInt(this.state.port)).estimateGas({ from: this.props.backendContractAddress })
            .then(async function (estimatedGasCost) {
                console.log("Estimated gas cost: ", estimatedGasCost)
                return estimatedGasCost;
            })
            .catch(function (error) {
                console.log("Error: ", error)
            });

        console.log("Communities list (before adding one): ", await backend.methods.communitiesNumber().call())

        await backend.methods.createCommunity(this.state.name, communityContractTxReceipt.contractAddress, parseInt(this.state.port))
            .send({ from: this.props.publicKey, gas: estimatedGasCost })
            .on('transactionHash', function (hash) {
                console.log("Transaction Hash: ", hash)
            }).on('receipt', function (receipt) {
                console.log("Recipt: ", receipt);
            })

        console.log("Communities list (before adding one): ", await backend.methods.communitiesNumber().call())
    }

    render() {
        return (
            <div>
                <Container component="main" maxWidth="xs">
                    <Box
                        sx={{
                            marginTop: 3,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        Create Community
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Community Name"
                            label="Community Name"
                            defaultValue={this.state.name}
                            id="CommunityName"
                            onChange={(event) => this.setState({ name: event.target.value })}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Port Number"
                            label="Port Number"
                            defaultValue={this.state.port}
                            id="PortNumber"
                            onChange={(event) => this.setState({ port: event.target.value })}
                        />
                        <Button
                            onClick={() => {
                                this.createCommunity();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Create Community
                        </Button>
                    </Box>
                </Container>
            </div>
        );
    }
}