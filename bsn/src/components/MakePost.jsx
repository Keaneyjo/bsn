import React, { Component } from 'react';
import { TextField, Box, Button, Container } from '@mui/material';

import Web3 from 'web3';


export default class MakePost extends Component {

    constructor(props) {
        super(props)
        this.state = {
            tile: '',
            content: '',
            communityPort: 0,
        }

        this.makePost = this.makePost.bind(this);
    }


    makePost = async () => {

        try {
            let port = parseInt(this.state.communityPort)

            // Get backend -> get specific community from backend using port -> get specific posting contract for this community -> use posting contract to make post

            let web3 = new Web3('HTTP://127.0.0.1:7545');

            let contract = require('../abis/Backend.json');
            let abi = contract.abi;
            const backendContract = new web3.eth.Contract(abi, this.props.backendContractAddress);
            let communityAddress = await backendContract.methods.communityPortToAddress(port).call();


            //////////////////////
            web3 = new Web3('HTTP://127.0.0.1:' + port);

            contract = require('../abis/Community.json');
            abi = contract.abi;
            const communityContract = new web3.eth.Contract(abi, communityAddress);
            let postingContractAddress = await communityContract.methods.postingContract().call();

            contract = require('../abis/Posting.json');
            abi = contract.abi;
            const postingContract = new web3.eth.Contract(abi, postingContractAddress);

            ////
            const auth = {
                privateKey: this.props.private,
                address: this.props.publicKey,
            };

            console.log("Uploading post...");

            await postingContract.methods.makePost(this.state.title, this.state.content)
                .send({ from: auth.address, gas: 10000000 })
                .on('transactionHash', function (hash) {
                    console.log("Transaction Hash: ", hash)
                }).on('receipt', function (receipt) {
                    console.log("Recipt: ", receipt);
                })

        } catch (error) {
            console.error("Error in MakePost.jsx: ", error)
        }



    }

    render() {
        return (
            <div>
                <Container component="main" maxWidth="xs">
                    <Box
                        sx={{
                            marginTop: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        Make Post
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Community Port"
                            label="Community Port"
                            id="Community Port"
                            onChange={(event) => this.setState({ communityPort: event.target.value })}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Post Title"
                            label="Post Title"
                            id="PostTitle"
                            onChange={(event) => this.setState({ title: event.target.value })}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Post Content"
                            label="Post Content"
                            id="PostContent"
                            multiline
                            rows={4}
                            onChange={(event) => this.setState({ content: event.target.value })}
                        />
                        <Button
                            onClick={() => {
                                this.makePost();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Post
                        </Button>
                    </Box>
                </Container>
            </div>
        );
    }
}


// makePost = async () => {

//     try {
//         let port = parseInt(this.state.communityPort)

//         const web3 = new Web3('HTTP://127.0.0.1:' + port);

//         let contract = require('../abis/Posting.json');
//         let abi = contract.abi;
//         let bytecode = contract.data.bytecode.object;

//         const auth = {
//             privateKey: this.props.private,
//             address: this.props.public,
//         };

//         console.log("Uploading post...");

//         // var data = fs.readFileSync(file, 'utf-8');
//         // const PARSED_FILE = JSON.parse(data);
//         // const abi = PARSED_FILE.abi;
//         // const bytecode = PARSED_FILE.bytecode;

//         console.log(`Attempting to deploy from account ${auth.address}`);

//         // 6. Create contract instance
//         const postContract = new web3.eth.Contract(abi);

//         // 7. Create constructor tx
//         const postContractTx = postContract.deploy({
//             data: bytecode,
//             arguments: [this.state.title, this.state.content, port]
//         });

//         // console.log("Got here!")
//         // 8. Sign transacation and send
//         const createTransaction = await web3.eth.accounts.signTransaction(
//             {
//                 data: postContractTx.encodeABI(),
//                 gas: await postContractTx.estimateGas(),
//             },
//             auth.privateKey
//         );

//         // 9. Send tx and wait for receipt
//         const createReceipt = await web3.eth.sendSignedTransaction(createTransaction.rawTransaction);
//         console.log(`Post ${this.state.title}, deployed at address: ${createReceipt.contractAddress}`);

//     } catch (error) {
//         console.error("Error in MakePost.jsx: ", error)
//     }

// }
