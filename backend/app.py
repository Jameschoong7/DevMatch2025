from flask import Flask, jsonify, request, render_template
from blockchain import (
    contract, mint_tokens, get_transaction_history, get_contract_stats,
    get_user_token_balance, get_user_donation_credits, convert_tokens_to_credits, donate_credits
)
from qr_utils import validate_qr_code
import json
import os

# Configure Flask to serve static files from src/ directory
app = Flask(__name__, 
           static_folder='../src',  # Point to src/ directory
           static_url_path='/static')  # Keep the same URL path

@app.route('/')
def index():
     return render_template("index.html")

@app.route('/login')
def login():
     return render_template("login.html")

@app.route('/recycle')
def recycle():
     return render_template("recycle.html")

@app.route('/donation')
def donation():
     return render_template("donation.html")

@app.route('/api/validate-qr', methods=['POST'])
def validate_qr():
    """Validate QR code and mint tokens if valid"""
    try:
        data = request.get_json()
        qr_code = data.get('qr_code')
        wallet_address = data.get('wallet_address')
        
        if not qr_code or not wallet_address:
            return jsonify({'error': 'Missing QR code or wallet address'}), 400
        
        # Validate QR code format
        if not validate_qr_code(qr_code):
            return jsonify({'error': 'Invalid QR code format'}), 400
        
        # Mint tokens to user's wallet (no usage tracking - allow multiple scans)
        try:
            tx_hash = mint_tokens(wallet_address)
            new_balance = get_user_token_balance(wallet_address)
            return jsonify({
                'success': True,
                'message': 'Tokens minted successfully! Keep recycling!',
                'transaction_hash': tx_hash,
                'tokens_minted': 1,
                'new_balance': new_balance
            })
        except Exception as e:
            return jsonify({'error': f'Failed to mint tokens: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/convert-tokens', methods=['POST'])
def convert_tokens():
    """Convert tokens to donation credits"""
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        amount = data.get('amount', 1)
        
        if not wallet_address:
            return jsonify({'error': 'Missing wallet address'}), 400
        
        # Convert tokens to donation credits
        try:
            convert_tokens_to_credits(wallet_address, amount)
            new_token_balance = get_user_token_balance(wallet_address)
            new_credits_balance = get_user_donation_credits(wallet_address)
            
            return jsonify({
                'success': True,
                'message': f'{amount} tokens converted to donation credits',
                'converted_amount': amount,
                'new_token_balance': new_token_balance,
                'new_credits_balance': new_credits_balance
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/donate', methods=['POST'])
def donate_to_ngo():
    """Donate to an NGO using donation credits"""
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        ngo_address = data.get('ngo_address')
        amount = data.get('amount', 1)
        
        if not wallet_address or not ngo_address:
            return jsonify({'error': 'Missing wallet address or NGO address'}), 400
        
        # Donate credits to NGO
        try:
            donate_credits(wallet_address, ngo_address, amount)
            new_credits_balance = get_user_donation_credits(wallet_address)
            
            return jsonify({
                'success': True,
                'message': f'Successfully donated {amount} credits to NGO',
                'donated_amount': amount,
                'ngo_address': ngo_address,
                'new_credits_balance': new_credits_balance
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/balance/<wallet_address>', methods=['GET'])
def get_balance(wallet_address):
    """Get user's token and donation credit balances"""
    try:
        token_balance = get_user_token_balance(wallet_address)
        credits_balance = get_user_donation_credits(wallet_address)
        
        return jsonify({
            'success': True,
            'wallet_address': wallet_address,
            'token_balance': token_balance,
            'credits_balance': credits_balance
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get balance: {str(e)}'}), 500

@app.route('/api/ngos', methods=['GET'])
def get_ngos():
    """Get list of approved NGOs"""
    # In production, this would come from the smart contract
    ngos = [
        {'address': '0x1234567890123456789012345678901234567890', 'name': 'Eco Warriors'},
        {'address': '0x0987654321098765432109876543210987654321', 'name': 'Green Earth'},
        {'address': '0x1111111111111111111111111111111111111111', 'name': 'Clean Oceans'}
    ]
    return jsonify({'ngos': ngos})

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get blockchain transaction history for transparency"""
    try:
        transactions = get_transaction_history()
        return jsonify({
            'success': True,
            'transactions': transactions,
            'total_count': len(transactions)
        })
    except Exception as e:
        return jsonify({'error': f'Failed to fetch transactions: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get contract statistics for transparency"""
    try:
        stats = get_contract_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500

if __name__=="__main__":
    app.run(debug=True)
