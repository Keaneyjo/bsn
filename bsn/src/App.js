import React, { Component } from 'react';
import './App.css';

import Home from './pages/Home';
import Posts from './pages/Posts';
import Communities from './pages/Communities';
import Create from './pages/Create';

import {Route, Routes} from "react-router-dom"
import Navbar from "./components/Navbar"


// IPFS
// import {Buffer} from 'buffer';
// import { create as ipfsHttpClient } from 'ipfs-http-client';
// const projectId = '2K6kFTG5PWdzMMu8nlKfPqyJWhn';
// const projectSecret = '76ab4986c73843be7272555b9a6990f4';
// const auth = `Basic ${Buffer.from(`${projectId}:${projectSecret}`).toString('base64')}`;
// const client = ipfsHttpClient({
//   host: 'ipfs.infura.io',
//   port: 5001,
//   protocol: 'https',
//   headers: {
//     authorization: auth,
//   },
// });
//

// async uploadToIPFS() {
//   let text = this.state.value;
//   // https://an-nft-marketplace.infura-ipfs.io
//   // https://infura-ipfs.io
//   const subdomain = 'https://infura-ipfs.io';
//   console.log("Attempting to upload to IPFS.")
//   try {
//    const added = await client.add({ content: text });
//    const URL = `${subdomain}/ipfs/${added.path}`;
//    console.log(URL);
//    return URL;
//  } catch (error) {
//    console.log('Error uploading file to IPFS.');
//  }
// };

class App extends Component {

  constructor(props) {
    super(props)
    this.state = {
      publicKey: '0x78BD4d6f77A32861F54687FACF529de93910bd96',
      privateKey: '35bf11198c86d90c72009804902bab1e1c5c133098e8ebb91fbdcfe214a746a7',
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
    console.log("Set Public Key: ", publicK)
    console.log("Set Private Key: ", privateK)
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