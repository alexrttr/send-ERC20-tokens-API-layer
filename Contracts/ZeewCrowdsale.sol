pragma solidity ^0.4.16;

import "./Crowdsale.sol";

contract ZeewCrowdsale {
    
    address public beneficiary;
    uint public price;
    bool crowdsaleClosed = false;
    Crowdsale public crowdsaleContract;
    mapping(address => uint256) public balanceOf;
    address owner;
    
    event FundTransfer(address backer, uint amount, bool isContribution);

    /**
     * Constrctor function
     *
     * Setup the owner
     */
    function ZeewCrowdsale () public {
        crowdsaleContract = Crowdsale( 0xfDc78cab7AafB3AE0fa198ecF89CFC7907BFa9b0);
    }

    function setCrowdsaleAddress(address crowdsaleAddr) {
        require(msg.sender == owner);
        
        crowdsaleContract = Crowdsale( crowdsaleAddr);
    }
    
      function ()  public payable {
     crowdsaleContract.transfer(msg.value, msg.sender);
    }
   
}