pragma solidity ^0.8.5;

contract SimpleTest {
    int256 public count = 0;
    string public name = "John";
    address payable creator;

    constructor() {
        creator = payable(msg.sender);
    }

    function payCreator() public payable {
        creator.transfer(msg.value);
        count++;
    }
}
