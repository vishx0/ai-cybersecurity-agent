// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecurityLog {

    string[] public logHashes;

    function addLogHash(string memory hash) public {
        logHashes.push(hash);
    }

    function getLogHash(uint index) public view returns(string memory) {
        return logHashes[index];
    }

    function getLogCount() public view returns(uint) {
        return logHashes.length;
    }
}