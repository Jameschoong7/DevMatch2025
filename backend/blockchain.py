from web3 import Web3
import json
import os
from dotenv import load_dotenv


#Load environment variables from .env
load_dotenv()


#Acdess variables
provider_url = os.getenv("PROVIDER_URL")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")



#Connect to Infura
web3=Web3(Web3.HTTPProvider(provider_url))

#Load ABI form abi.json
abi_path = os.path.join(os.path.dirname(__file__),'../abi.json')

with open(abi_path) as f:
    abi = json.load(f)


#Connect to contract
contract = web3.eth.contract(address=contract_address,abi=abi)

#Get user account (needed for transactions)
account = web3.eth.account.from_key(private_key)