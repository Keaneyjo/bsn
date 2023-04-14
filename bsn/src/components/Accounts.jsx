import React, { Component } from 'react'
import { TextField, Box, Button, Container } from '@mui/material';

export default class Accounts extends Component {
    constructor(props) {
        super(props)
        this.state = {
            publicKey: this.props.publicKey,
            privateKey: this.props.privateKey,
        }

        this.setKeys = this.setKeys.bind(this);
    }

    setKeys() {
        console.log("Set Public Key: ", this.state.publicKey)
        console.log("Set Private Key: ", this.state.privateKey)
        this.props.setKeys(this.state.publicKey, this.state.privateKey)
    }

    render() {
        return (
            <div>
                <Container component="main" maxWidth="xs">
                    <Box
                        sx={{
                            marginTop: 6,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        Accounts
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Public Key"
                            label="Public Key"
                            defaultValue={this.state.publicKey}
                            id="PublicKey"
                            onChange={(event) => this.setState({ publicKey: event.target.value })}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="Private Key"
                            label="Private Key"
                            defaultValue={this.state.privateKey}
                            id="PrivateKey"
                            onChange={(event) => this.setState({ privateKey: event.target.value })}
                        />
                        <Button
                            onClick={() => {
                                this.setKeys();
                            }}
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Set Keys
                        </Button>
                    </Box>
                </Container>
            </div>
        )
    }
}
