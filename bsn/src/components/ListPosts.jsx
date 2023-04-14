import React, { Component } from 'react';
import Web3 from 'web3';

import { TextField, Button, Container } from '@mui/material';

import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default class ListPosts extends Component {

    constructor(props) {
        super(props)
        this.state = {
            tableLoaded: false,
            communityPort: 0,
            authors: [],
            titles: [],
            content: []
        }

        this.listPosts = this.listPosts.bind(this);
    }


    listPosts = async () => {


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
        let postsLength = await postingContract.methods.postCount().call();

        let authorList = [], titleList = [], contentList = []
        for (var i = 0; i < postsLength; i++) {
            let post = await postingContract.methods.posts(i).call()
            authorList.push(post._author)
            titleList.push(post._title)
            contentList.push(post._content)
        }

        this.setState({ authors: authorList })
        this.setState({ titles: titleList })
        this.setState({ content: contentList })
        this.setState({ tableLoaded: true });

    }

    render() {

        const StyledTableCell = styled(TableCell)(({ theme }) => ({
            [`&.${tableCellClasses.head}`]: {
                backgroundColor: theme.palette.common.black,
                color: theme.palette.common.white,
            },
            [`&.${tableCellClasses.body}`]: {
                fontSize: 14,
            },
        }));

        const StyledTableRow = styled(TableRow)(({ theme }) => ({
            '&:nth-of-type(odd)': {
                backgroundColor: theme.palette.action.hover,
            },
            // hide last border
            '&:last-child td, &:last-child th': {
                border: 0,
            },
        }));

        return (
            <div>
                <Container component="main" maxWidth="xl">
                    <Container component="main" maxWidth="xs">
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Community Port"
                            label="Community Port"
                            id="CommunityPort"
                            onChange={(event) => this.setState({ communityPort: event.target.value })}
                        />
                        <Button
                            onClick={() => {
                                this.listPosts();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            List Posts
                        </Button>
                    </Container>
                    {this.state.tableLoaded ?
                        <TableContainer component={Paper}>
                            <Table sx={{ minWidth: 700 }} aria-label="customized table">
                                <TableHead>
                                    <TableRow>
                                        <StyledTableCell>Author Address</StyledTableCell>
                                        <StyledTableCell align="right">Title</StyledTableCell>
                                        <StyledTableCell align="right">Content</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {this.state.authors.map((_, i) => (
                                        <StyledTableRow key={i} >
                                            <StyledTableCell component="th" scope="row">{this.state.authors[i]}</StyledTableCell>
                                            <StyledTableCell align="right">{this.state.titles[i]}</StyledTableCell>
                                            <StyledTableCell align="right">{this.state.content[i]}</StyledTableCell>
                                        </StyledTableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                        :
                        <Container component="main" maxWidth="xs">
                            <TableContainer component={Paper}>
                                <Table aria-label="customized table">
                                    <TableHead>
                                        <TableRow>
                                            <StyledTableCell align="center">Table Not Loaded</StyledTableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Container>
                    }
                </Container>
            </div>
        );
    }
}