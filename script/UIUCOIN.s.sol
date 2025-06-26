// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {UIUCOIN} from "../src/UIUCOIN.sol";
contract UIUCOINScript is Script {

    function setUp() public {}

    function run() public {
        address initialOwner = vm.envAddress("OWNER");
        
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        
        vm.startBroadcast(deployerPrivateKey);

        UIUCOIN uiucoin = new UIUCOIN(initialOwner);
        console.log(address(uiucoin));
        vm.stopBroadcast();

    }
}
