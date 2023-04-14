pragma solidity ^0.8.6;

// SPDX-License-Identifier: MIT

import "./Profile.sol";
import "./Community.sol";

contract Backend {
    string public name = "Backend";

    mapping(string => Community) public communities;
    uint256 private totalCommunities = 0;
    mapping(int256 => Profile) public moderators;
    mapping(address => Profile) public profiles;

    constructor() {}

    event ContractCreated(address newAddress);

    function createUser(string memory _username) public {
        // TODO:
        // if() check if user already exists
        // maybe they can just recreate their profile if they createUser

        Profile profile = new Profile(_username);
        profiles[msg.sender] = profile;
    }

    function createCommunity(string memory _communityName)
        public
        returns (address)
    {
        // Localhost should be sidechain.
        Community community = new Community("localhost");
        communities[_communityName] = community;
        totalCommunities++;
        emit ContractCreated(address(community));
        return address(community);
    }

    function fetchProfile(address _profileAddress) public returns (Profile) {
        return profiles[_profileAddress];
    }
}
