//SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;

contract GreenChain{

    //Mapping to track user token balances
    mapping(address=>uint256) public tokenBalances;

    //Mapping to track user donation totals
    mapping(address=>uint256)public totalDonated;

    //Mapping to check valid NGO address
    mapping(address=>bool)public approvedNGOs;

    //Owner of the contract
    address public owner;

    
    //Event for frontend to listen to
    event TokenClaimed(address indexed user, uint256 amount);
    event DonationConverted(address indexed user, uint256 amount);
    event Donated(address indexed user, address indexed ngo, uint256 amount);
    event NGOAdded(address ngo);


    //Constructor runs only once when contracted is deployed
    constructor(){
        owner = msg.sender;
    }

    //Modifier: Only owner can call certain functions
    modifier onlyOwner(){
        require(msg.sender == owner,"Not Contract Owner");
        _;
    }

    //Function to add a valid NGO (can be called only by owner)
    function addNGO(address ngo) public onlyOwner{
        approvedNGOs[ngo] = true;
        emit NGOAdded(ngo);

    }

    //User claims token after recycling
    function claimToken(uint256 amount) public{
        require(amount>0,"Invalid amount");
        tokenBalances[msg.sender]+= amount;
        emit TokenClaimed(msg.sender, amount);

    }


    //Convert tokens to donation credit (token burned)
    function convertToDonation(uint256 amount) public{
        require(tokenBalances[msg.sender]>amount,"Insufficient Balance");
        tokenBalances[msg.sender]-=amount;
        totalDonated[msg.sender] +=amount;
        emit DonationConverted(msg.sender, amount);
    }

    //Donate to NGO using converted donation credits
    function donateToNGO(address ngo,uint256 amount)public{
        require(approvedNGOs[ngo],"NGO not supported");
        require(totalDonated[msg.sender]>=amount,"Not enough donation credits");

        totalDonated[msg.sender]-=amount;

        emit Donated(msg.sender,ngo,amount);
    }

}