import React, { Component } from 'react';
import Web3 from 'web3';

import { Box, Button, Container, Alert } from '@mui/material';

import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';



export default class ListCommunities extends Component {

    constructor(props) {
        super(props)
        this.state = {
            communityNames: [],
            communityAddress: [],
            communityPort: [],
            tableLoaded: false,
            displayAlert: false
        }

        this.loadCommunites = this.loadCommunites.bind(this);
    }

    loadCommunites = async () => {

        let web3 = new Web3('HTTP://127.0.0.1:7545');

        let contract = require('../abis/Backend.json');
        let abi = contract.abi;

        try {
            const backend = new web3.eth.Contract(abi, this.props.backendContractAddress);
            console.log("Backend Contract pulled sucessfully.")
            console.log("Backend contract: ", backend)

            let numberOfCommunities = await backend.methods.communitiesNumber().call();


            let tempCommunityName, tempCommunityAddress, tempCommunityPort;
            let tempCommunityNamesList = [], tempCommunityAddressList = [], tempCommunityPortList = [];
            for (var i = 0; i < numberOfCommunities; i++) {
                // string [] public communitiesNames;
                tempCommunityName = await backend.methods.communitiesNames(i).call();
                tempCommunityNamesList.push(tempCommunityName)

                // mapping(string => address) public communityAddresses;
                tempCommunityAddress = await backend.methods.communityAddresses(tempCommunityName).call();
                tempCommunityAddressList.push(tempCommunityAddress)

                // mapping(address => uint16) public communityPorts;
                tempCommunityPort = await backend.methods.communityPorts(tempCommunityAddress).call();
                tempCommunityPortList.push(tempCommunityPort);
            }

            this.setState({ communityNames: tempCommunityNamesList });
            this.setState({ communityAddress: tempCommunityAddressList });
            this.setState({ communityPort: tempCommunityPortList });

            this.setState({ tableLoaded: true });
            this.setState({ displayAlert: false })

            numberOfCommunities = await backend.methods.communitiesNumber().call();
            console.log("Total Number of Communities: ", numberOfCommunities)
        } catch {
            this.setState({ displayAlert: true })
        }
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
                        <Button
                            onClick={() => {
                                this.loadCommunites();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Refresh Community Table
                        </Button>
                    </Container>
                    <Box
                        sx={{
                            marginTop: 6,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    ></Box>
                    {this.state.tableLoaded ?
                        <TableContainer component={Paper}>
                            <Table sx={{ minWidth: 700 }} aria-label="customized table">
                                <TableHead>
                                    <TableRow>
                                        <StyledTableCell>Community Name</StyledTableCell>
                                        <StyledTableCell align="right">Contract Address</StyledTableCell>
                                        <StyledTableCell align="right">Community Port</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {this.state.communityNames.map((_, i) => (
                                        <StyledTableRow key={i}>
                                            <StyledTableCell component="th" scope="row">{this.state.communityNames[i]}</StyledTableCell>
                                            <StyledTableCell align="right">{this.state.communityAddress[i]}</StyledTableCell>
                                            <StyledTableCell align="right">{this.state.communityPort[i]}</StyledTableCell>
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
                            {this.state.displayAlert ? <Alert severity="error">Unable to load communities. Is the Backend Contract Address correct?</Alert> : ""}
                        </Container>
                    }
                </Container>
            </div>
        );
    }
}