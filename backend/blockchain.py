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


def mint_tokens(wallet_address):
    """
    Mint token to wallet_address.
    Returns the transaction hash.
    """
    nonce = web3.eth.get_transaction_count(account.address)
    txn = contract.functions.mint(wallet_address, 1).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)
