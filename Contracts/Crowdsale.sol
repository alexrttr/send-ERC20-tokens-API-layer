pragma solidity ^0.4.16;

import "./Whitelist.sol";
import "./ERC20Token.sol";


contract Crowdsale is Whitelist{
    address public beneficiary;
    uint public price;
    bool crowdsaleClosed = false;
    TokenERC20 public tokenReward;
    mapping(address => uint256) public balanceOf;
    address owner;
    
    event FundTransfer(address backer, uint amount, bool isContribution);

    /**
     * Constrctor function
     *
     * Setup the owner
     */
    function Crowdsale () public {
        beneficiary = 0xfDc78cab7AafB3AE0fa198ecF89CFC7907BFa9b0;
        price = 0.002437 * 1 ether;
        tokenReward = TokenERC20(0xf4350c378c8e5bf11c6d57c46165a56dab506bba);
        owner = msg.sender;
    }

    function setBeneficiary(address beneficiaryAddress) {
        require(msg.sender == owner);
        
        beneficiary = beneficiaryAddress;
    }
    
    
    function setToken(address tokenAddress) {
        require(msg.sender == owner);
        tokenReward = TokenERC20(tokenAddress);
    }
    
    /**
     * Fallback function
     *
     * The function without name is the default function that is called whenever anyone sends funds to a contract
     */
    function () onlyWhitelisted  public payable {
        require(!crowdsaleClosed);
        uint amount = msg.value;
        uint val = (amount  * 1 ether) / price;
        balanceOf[msg.sender] += amount;
        tokenReward.addsmartContractAdress(msg.sender);
        tokenReward.approve(msg.sender, val);
        tokenReward.transferFrom(owner, msg.sender, val);
        FundTransfer(msg.sender, amount, true);
    }
    
     function whoAmI() constant public returns(address me, address owner){
        return tokenReward.whoAmI();
    }
    
    function transfer(uint amount, address from) onlyWhitelisted public payable{
         
        uint val = (amount  * 1 ether) / price;
        balanceOf[from] += amount;
        tokenReward.addsmartContractAdress(msg.sender);
        tokenReward.approve(from, val);
        tokenReward.transferFrom(from, owner, val);
        FundTransfer(from, amount, true);
    } 
    
    
    function getAccount() public constant returns (address sender){
        return msg.sender;
    }
    
    function getAmount () public constant returns (uint val){
        return  (msg.value  * 1 ether) / price;
    }
    
      function getAmount (uint value) public constant returns (uint val){
        return  (val   * 1 ether) / price;
    }
    
    function changePrice(uint newprice) public {
         if (beneficiary == msg.sender) {
             price = newprice;
         }
    }

    function safeWithdrawal(uint amount) public {

        if (beneficiary == msg.sender) {
            if (beneficiary.send(amount)) {
                FundTransfer(beneficiary, amount, false);
            }
        }
    }
    
    function safeTokenWithdrawal(uint amount) public {
         if (beneficiary == msg.sender) {
             tokenReward.transfer(msg.sender, amount);
        }
    }
    
     function crowdsaleStop() public {
         if (beneficiary == msg.sender) {
            crowdsaleClosed = true;
        }
    }
    
    function crowdsaleStart() public {
         if (beneficiary == msg.sender) {
            crowdsaleClosed = false;
        }
    }
}
