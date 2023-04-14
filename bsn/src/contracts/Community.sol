pragma solidity ^0.8.6;

// SPDX-License-Identifier: MIT

import "./Post.sol";
import "./Profile.sol";
import "./Backend.sol";

interface IBackend {
    function count() external view returns (uint256);

    function fetchProfile(address _profileAddress) external returns (Profile);
}

// contract Counter {
//     uint public count;

//     function increment() external {
//         count += 1;
//     }
// }

// contract Interaction {
//     address counterAddr;

//     function setCounterAddr(address _counter) public payable {
//        counterAddr = _counter;
//     }

//     function getCount() external view returns (uint) {
//         return ICounter(counterAddr).count();
//     }
// }

contract Community {
    string public name = "Community";
    Profile public founder;
    string public hosting; // Network the community is being hosted on, e.g. localhost:7545, etc.

    uint256 postCount = 0;

    mapping(address => Profile) subscribers;
    mapping(uint256 => Post) public posts;

    address public BACKEND_CONTRACT_ADDRESS;

    address private backend;

    function fetchProfile(address _profile) external returns (Profile) {
        return IBackend(backend).fetchProfile(_profile);
    }

    function makePost(string memory _content) public {
        posts[postCount] = new Post(_content);
        postCount++;
    }

    constructor(string memory _hosting) payable {
        backend = msg.sender;
        founder = IBackend(backend).fetchProfile(tx.origin);
        hosting = _hosting;
    }
}
