// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VisaContract {
    struct Visa {
        string name;
        string passportID;
        string visaType;
        uint256 timestamp;
    }

    Visa[] public visas;

    event VisaIssued(string name, string passportID, string visaType);

    constructor() {
        // Hardcoded Visa entry on deployment
        visas.push(Visa("Adi", "888888", "Study", block.timestamp));
        emit VisaIssued("Adi", "888888", "Study");
    }

    function issueVisa(string memory name, string memory passportID, string memory visaType) public {
        visas.push(Visa(name, passportID, visaType, block.timestamp));
        emit VisaIssued(name, passportID, visaType);
    }

    function getVisa(uint index) public view returns (string memory, string memory, string memory, uint256) {
        Visa memory v = visas[index];
        return (v.name, v.passportID, v.visaType, v.timestamp);
    }
}
