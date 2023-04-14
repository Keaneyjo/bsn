pragma solidity ^0.8.13;

// SPDX-License-Identifier: MIT

contract Backend {

    address[] public moderators;
    address public founder;

    mapping(string => address) public communityAddresses;
    mapping(address => uint16) public communityPorts;
    mapping(uint16 => address) public communityPortToAddress;
    string [] public communitiesNames;
    int public communitiesNumber = 0;


    constructor() {
        founder = tx.origin;
        moderators.push(tx.origin);
    }

    function createCommunity(string memory _communityName, address _communityAddress, uint16 _communityPort) public {
        communityAddresses[_communityName] = _communityAddress;
        communityPorts[_communityAddress] = _communityPort;
        communityPortToAddress[_communityPort] = _communityAddress;
        communitiesNames.push(_communityName);
        communitiesNumber++;
    }

}
