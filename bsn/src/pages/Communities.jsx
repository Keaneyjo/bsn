import React, { Component } from 'react'
import ListCommunities from '../components/ListCommunities'

export default class Communities extends Component {
    render() {
        return (
            <div>
                <ListCommunities backendContractAddress={this.props.backendContractAddress} />
            </div>
        )
    }
}
