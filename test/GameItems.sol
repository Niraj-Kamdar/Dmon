// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/GameItems.sol";

contract TestGameItems {
    function testInitialBalanceUsingDeployedContract() public {
        GameItems gameItems = GameItems(DeployedAddresses.GameItems());
        uint expected = 10**18;
        Assert.equal(gameItems.balanceOf(tx.origin, 0), expected, "Owner should have 10**18 GToken initially");
    }
}