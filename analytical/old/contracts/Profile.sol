pragma solidity ^0.8.6;

// SPDX-License-Identifier: MIT

contract Profile {
    address payable userAddress;
    string username;

    constructor(string memory _username) {
        userAddress = payable(tx.origin);
        username = _username;
    }
}
