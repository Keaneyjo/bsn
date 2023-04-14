import React, { Component } from 'react'
import { Box, Button, Container } from '@mui/material';
import Web3 from 'web3';

export default class DeployBackend extends Component {

    constructor(props) {
        super(props)
        this.state = {
            backendContractAddress: this.props.backendContractAddress
        }

        this.deployBackend = this.deployBackend.bind(this);
    }

    deployBackend = async () => {

        let contract = require('../abis/Backend.json');
        let abi = contract.abi;
        let bytecode = contract.data.bytecode.object;

        const web3 = new Web3('HTTP://127.0.0.1:7545');
        const auth = {
            privateKey: this.props.privateKey,
            address: this.props.publicKey,
        };

        console.log("Deploying backend...");
        console.log(`Attempting to deploy from account ${auth.address}`);

        const backendContract = new web3.eth.Contract(abi);

        const backendContractTx = backendContract.deploy({
            data: bytecode,
        });

        const signedBackendContractTx = await web3.eth.accounts.signTransaction(
            {
                data: backendContractTx.encodeABI(),
                gas: await backendContractTx.estimateGas(),
            },
            auth.privateKey
        );

        const backendContractTxReceipt = await web3.eth.sendSignedTransaction(signedBackendContractTx.rawTransaction);
        this.props.setBackendContractAddress(backendContractTxReceipt.contractAddress)
        console.log(`Backend Contract deployed at address: ${backendContractTxReceipt.contractAddress}`);
        this.setState({ backendContractAddress: backendContractTxReceipt.contractAddress })
    }

    render() {
        return (
            <div>
                <Container component="main" maxWidth="xs">
                    <Box
                        sx={{
                            marginTop: 5,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        Backend Contract Address: {this.props.backendContractAddress == "" || this.props.backendContractAddress == null ? "Not Set" : this.props.backendContractAddress}
                        <Button
                            onClick={() => {
                                this.deployBackend();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Deploy Backend
                        </Button>
                    </Box>
                </Container>
            </div>
        )
    }
}
