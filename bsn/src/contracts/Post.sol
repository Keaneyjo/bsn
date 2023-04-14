pragma solidity ^0.8.6;

// SPDX-License-Identifier: MIT

contract Post {
    string public content;
    address payable public author;
    uint256 public postTime;

    constructor(string memory _content) {
        author = payable(tx.origin);
        content = _content;
        postTime = block.timestamp;
    }
}
