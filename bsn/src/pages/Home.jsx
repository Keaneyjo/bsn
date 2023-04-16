import React, { Component } from 'react';
import Web3 from 'web3';

import Accounts from '../components/Accounts';
import SetBackend from '../components/SetBackend';
import DeployBackend from '../components/DeployBackend';

export default class Home extends Component {

    constructor(props) {
        super(props)
        this.state = {
            publicKey: this.props.publicKey,
            privateKey: this.props.privateKey,
            web3: new Web3('HTTP://127.0.0.1:7545'),
            backendContractAddress: this.props.backendContractAddress,
        }

        this.setBackendContractAddress = this.setBackendContractAddress.bind(this);
    }

    setBackendContractAddress = value => {
        this.setState({ backendContractAddress: value })
        this.props.setBackendContractAddress(value)
    }

    render() {

        return (
            <div className="App">
                <Accounts
                    publicKey={this.props.publicKeyy}
                    privateKey={this.props.privateKey}
                    setKeys={this.props.setKeys}
                />
                <SetBackend
                    backendContractAddress={this.state.backendContractAddress}
                    setBackendContractAddress={this.setBackendContractAddress}
                />
                <DeployBackend
                    publicKey={this.props.publicKey} privateKey={this.props.privateKey}
                    backendContractAddress={this.state.backendContractAddress}
                    setBackendContractAddress={this.setBackendContractAddress}
                />
            </div>
        )
    }
}