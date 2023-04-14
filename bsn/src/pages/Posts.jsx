import React, { Component } from 'react'
import ListPosts from '../components/ListPosts'

export default class Posts extends Component {
    render() {
        return (
            <div>
                <ListPosts backendContractAddress={this.props.backendContractAddress} />
            </div>
        )
    }
}
