let GameItems = artifacts.require("GameItems");

module.exports = function(deployer) {
  // deployment steps
  deployer.deploy(GameItems, "0x2B99251eC9650e507936fa9530D11dE4d6C9C05c");
};