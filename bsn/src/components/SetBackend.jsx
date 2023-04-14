import React, { Component } from 'react'
import { TextField, Box, Button, Container } from '@mui/material';

export default class SetBackend extends Component {
    constructor(props) {
        super(props)
        this.state = {
            backendContractAddress: this.props.backendContractAddress,
        }

        this.setBackendAddress = this.setBackendAddress.bind(this);
    }

    setBackendAddress = async => {
        this.props.setBackendContractAddress(this.state.backendContractAddress)
    }

    render() {
        return (
            <div>
                <Container component="main" maxWidth="xs">
                    <Box
                        sx={{
                            marginTop: 4,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        Set Previous Backend Contract Address
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Backend Contract Address"
                            label="Backend Contract Address"
                            defaultValue={this.state.backendContractAddress}
                            id="BackendContractAddress"
                            onChange={(event) => this.setState({ backendContractAddress: event.target.value })}
                        />
                        <Button
                            onClick={() => {
                                this.setBackendAddress();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Set Address
                        </Button>
                    </Box>
                </Container>
            </div>
        )
    }
}
