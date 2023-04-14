import React, { Component } from 'react'
import CreateCommunity from '../components/CreateCommunity'
import MakePost from '../components/MakePost'

export default class Create extends Component {

    constructor(props) {
        super(props)
        this.state = {
        }
    }

    render() {
        return (
            <div>
                <CreateCommunity
                    publicKey={this.props.publicKey} privateKey={this.props.privateKey}
                    backendContractAddress={this.props.backendContractAddress} />
                <MakePost
                    publicKey={this.props.publicKey} privateKey={this.props.privateKey}
                    backendContractAddress={this.props.backendContractAddress}
                />
            </div>
        )
    }
}
