import React, { Component } from 'react';
import './App.css';

import Home from './pages/Home';
import Posts from './pages/Posts';
import Communities from './pages/Communities';
import Create from './pages/Create';

import {Route, Routes} from "react-router-dom"
import Navbar from "./components/Navbar"


class App extends Component {

  constructor(props) {
    super(props)
    this.state = {
      publicKey: '',
      privateKey: '',
      backendContractAddress: null,
    }

    this.setBackendContractAddress = this.setBackendContractAddress.bind(this);
    this.setKeys = this.setKeys.bind(this);
  }

  setBackendContractAddress = value => {
    this.setState({backendContractAddress: value})
  }

  async setKeys(publicK, privateK) {
    this.setState({publicKey: publicK})
    this.setState({privateKey: privateK})
    console.log("Set a Public Key: ", publicK)
    console.log("Set a Private Key: ", privateK)
    this.setState({publicKey: publicK})
    this.setState({privateKey: privateK})
  }

  render() {
    return (
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home 
            publicKey={this.state.publicKey} privateKey={this.state.privateKey} 
            setKeys={this.setKeys} 
            backendContractAddress={this.state.backendContractAddress} setBackendContractAddress={this.setBackendContractAddress} />} 
          />
          <Route path="/communities" element={<Communities backendContractAddress={this.state.backendContractAddress} />} />
          <Route path="/posts" element={<Posts backendContractAddress={this.state.backendContractAddress} />} />
          <Route path="/create" element={<Create 
            publicKey={this.state.publicKey} privateKey={this.state.privateKey} 
            backendContractAddress={this.state.backendContractAddress}
          />} />
        </Routes>
      </div>
    )
  }
}

export default App;