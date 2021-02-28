// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@opengsn/gsn/contracts/BaseRelayRecipient.sol";


contract GameItems is ERC1155, Ownable, BaseRelayRecipient {
    uint public constant GToken = 0;
    uint public totalTokenTypes = 1;

    mapping(address => uint[]) public userMonsters;

    event MonsterCreated(address indexed recipient, uint MonsterId, string MonsterName);

    constructor(address _trustedForwarder) public ERC1155("https://dmon-api.herokuapp.com/item/{id}") {
        trustedForwarder = _trustedForwarder;
        _mint(_msgSender(), GToken, 10 ** 18, "");
    }

    function createMonster(address recipient, string memory MonsterName) public onlyOwner {
        _mint(recipient, totalTokenTypes, 1, "");
        userMonsters[recipient].push(totalTokenTypes);
        emit MonsterCreated(recipient, totalTokenTypes, MonsterName);
        totalTokenTypes++;
    }

    function getUserMonsters(address user) public returns (uint[] memory) {
        return userMonsters[user];
    }

    function _msgSender() internal override(Context, BaseRelayRecipient)
    view returns (address payable) {
        return BaseRelayRecipient._msgSender();
    }

    function _msgData() internal override(Context, BaseRelayRecipient)
    view returns (bytes memory ret) {
        return BaseRelayRecipient._msgData();
    }


    function setForwarder(address forwarder) public onlyOwner {
        trustedForwarder = forwarder;
    }

    function versionRecipient() external virtual override view returns (string memory){return "1";}

    receive() external payable {}
}
