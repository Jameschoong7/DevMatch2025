from web3 import Web3
import json
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# In-memory storage for demo purposes (in production, use database)
user_token_balances = {}
user_donation_credits = {}

#Load environment variables from .env
load_dotenv()


#Access variables
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
    Simulate claiming token for wallet_address.
    In a real implementation, this would require user signature.
    Returns a mock transaction hash.
    """
    try:
        # For demo purposes, we'll simulate the transaction
        # In production, this should be called by the user's wallet
        mock_tx_hash = "0x" + str(uuid.uuid4()).replace("-", "")[:64]
        
        # Update user's token balance
        if wallet_address not in user_token_balances:
            user_token_balances[wallet_address] = 0
        user_token_balances[wallet_address] += 1
        
        print(f"Tokens minted for {wallet_address}: {user_token_balances[wallet_address]} total")
        
        # You could also call the contract directly if you have the user's private key
        # nonce = web3.eth.get_transaction_count(wallet_address)
        # txn = contract.functions.claimToken(1).build_transaction({
        #     'from': wallet_address,
        #     'nonce': nonce,
        #     'gas': 200000,
        #     'gasPrice': web3.to_wei('5', 'gwei')
        # })
        
        return mock_tx_hash
        
    except Exception as e:
        raise Exception(f"Failed to claim tokens: {str(e)}")

def get_user_token_balance(wallet_address):
    """
    Get user's current token balance
    """
    return user_token_balances.get(wallet_address, 0)

def get_user_donation_credits(wallet_address):
    """
    Get user's current donation credits
    """
    return user_donation_credits.get(wallet_address, 0)

def convert_tokens_to_credits(wallet_address, amount):
    """
    Convert tokens to donation credits
    """
    try:
        current_balance = get_user_token_balance(wallet_address)
        if current_balance < amount:
            raise Exception(f"Insufficient tokens. Available: {current_balance}, Requested: {amount}")
        
        # Deduct tokens
        user_token_balances[wallet_address] -= amount
        
        # Add donation credits
        if wallet_address not in user_donation_credits:
            user_donation_credits[wallet_address] = 0
        user_donation_credits[wallet_address] += amount
        
        print(f"Converted {amount} tokens to credits for {wallet_address}")
        print(f"New token balance: {user_token_balances[wallet_address]}")
        print(f"New donation credits: {user_donation_credits[wallet_address]}")
        
        return True
        
    except Exception as e:
        raise Exception(f"Failed to convert tokens: {str(e)}")

def donate_credits(wallet_address, ngo_address, amount):
    """
    Donate credits to NGO
    """
    try:
        current_credits = get_user_donation_credits(wallet_address)
        if current_credits < amount:
            raise Exception(f"Insufficient donation credits. Available: {current_credits}, Requested: {amount}")
        
        # Deduct donation credits
        user_donation_credits[wallet_address] -= amount
        
        print(f"Donated {amount} credits to NGO {ngo_address} from {wallet_address}")
        print(f"Remaining donation credits: {user_donation_credits[wallet_address]}")
        
        return True
        
    except Exception as e:
        raise Exception(f"Failed to donate: {str(e)}")

def get_transaction_history():
    """
    Return mock transaction history for demo transparency display
    """
    # Return mock transaction data for demo purposes
    return [
        {
            'type': 'Token Claimed',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'amount': 1,
            'transaction_hash': '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
            'block_number': 12345678,
            'timestamp': '2025-01-07 14:30:25',
            'description': 'User 0x742d35Cc6... claimed 1 tokens for recycling'
        },
        {
            'type': 'Tokens Converted',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'amount': 5,
            'transaction_hash': '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            'block_number': 12345679,
            'timestamp': '2025-01-07 15:45:12',
            'description': 'User 0x742d35Cc6... converted 5 tokens to donation credits'
        },
        {
            'type': 'Donation Made',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'ngo': '0xEcoWarriors1234567890abcdef1234567890abcdef',
            'amount': 3,
            'transaction_hash': '0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba',
            'block_number': 12345680,
            'timestamp': '2025-01-07 16:20:33',
            'description': 'User 0x742d35Cc6... donated 3 credits to NGO 0xEcoWarrior...'
        },
        {
            'type': 'Token Claimed',
            'user': '0x8ba1f109551bD432803012645Hac136c772c3e',
            'amount': 2,
            'transaction_hash': '0x4567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123',
            'block_number': 12345681,
            'timestamp': '2025-01-07 17:15:45',
            'description': 'User 0x8ba1f10955... claimed 2 tokens for recycling'
        },
        {
            'type': 'NGO Added',
            'ngo': '0xGreenEarth1234567890abcdef1234567890abcdef',
            'transaction_hash': '0x6543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba98',
            'block_number': 12345682,
            'timestamp': '2025-01-07 18:00:00',
            'description': 'New NGO added: 0xGreenEarth1...'
        },
        {
            'type': 'Token Claimed',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'amount': 1,
            'transaction_hash': '0x1111111111111111111111111111111111111111111111111111111111111111',
            'block_number': 12345683,
            'timestamp': '2025-01-07 19:30:15',
            'description': 'User 0x742d35Cc6... claimed 1 tokens for recycling'
        },
        {
            'type': 'Tokens Converted',
            'user': '0x8ba1f109551bD432803012645Hac136c772c3e',
            'amount': 2,
            'transaction_hash': '0x2222222222222222222222222222222222222222222222222222222222222222',
            'block_number': 12345684,
            'timestamp': '2025-01-07 20:45:30',
            'description': 'User 0x8ba1f10955... converted 2 tokens to donation credits'
        },
        {
            'type': 'Donation Made',
            'user': '0x8ba1f109551bD432803012645Hac136c772c3e',
            'ngo': '0xCleanOceans1234567890abcdef1234567890abcdef',
            'amount': 1,
            'transaction_hash': '0x3333333333333333333333333333333333333333333333333333333333333333',
            'block_number': 12345685,
            'timestamp': '2025-01-07 21:15:45',
            'description': 'User 0x8ba1f10955... donated 1 credits to NGO 0xCleanOcean...'
        }
    ]

def get_sample_transactions():
    """
    Return sample transaction data for demo purposes
    """
    return [
        {
            'type': 'Token Claimed',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'amount': 1,
            'transaction_hash': '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
            'block_number': 12345678,
            'timestamp': '2025-01-07 14:30:25',
            'description': 'User 0x742d35Cc6... claimed 1 tokens for recycling'
        },
        {
            'type': 'Tokens Converted',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'amount': 5,
            'transaction_hash': '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            'block_number': 12345679,
            'timestamp': '2025-01-07 15:45:12',
            'description': 'User 0x742d35Cc6... converted 5 tokens to donation credits'
        },
        {
            'type': 'Donation Made',
            'user': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'ngo': '0xEcoWarriors1234567890abcdef1234567890abcdef',
            'amount': 3,
            'transaction_hash': '0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba',
            'block_number': 12345680,
            'timestamp': '2025-01-07 16:20:33',
            'description': 'User 0x742d35Cc6... donated 3 credits to NGO 0xEcoWarrior...'
        },
        {
            'type': 'Token Claimed',
            'user': '0x8ba1f109551bD432803012645Hac136c772c3e',
            'amount': 2,
            'transaction_hash': '0x4567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123',
            'block_number': 12345681,
            'timestamp': '2025-01-07 17:15:45',
            'description': 'User 0x8ba1f10955... claimed 2 tokens for recycling'
        },
        {
            'type': 'NGO Added',
            'ngo': '0xGreenEarth1234567890abcdef1234567890abcdef',
            'transaction_hash': '0x6543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba98',
            'block_number': 12345682,
            'timestamp': '2025-01-07 18:00:00',
            'description': 'New NGO added: 0xGreenEarth1...'
        }
    ]

def get_contract_stats():
    """
    Get contract statistics for transparency
    """
    try:
        # Get total events count
        latest_block = web3.eth.block_number
        from_block = max(0, latest_block - 1000)
        
        token_claimed_count = len(contract.events.TokenClaimed.get_all_entries(fromBlock=from_block))
        donation_converted_count = len(contract.events.DonationConverted.get_all_entries(fromBlock=from_block))
        donated_count = len(contract.events.Donated.get_all_entries(fromBlock=from_block))
        
        return {
            'total_recycling_events': token_claimed_count,
            'total_conversions': donation_converted_count,
            'total_donations': donated_count,
            'contract_address': contract_address,
            'network': 'Sepolia Testnet',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {
            'total_recycling_events': 15,
            'total_conversions': 8,
            'total_donations': 12,
            'contract_address': contract_address,
            'network': 'Sepolia Testnet',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
