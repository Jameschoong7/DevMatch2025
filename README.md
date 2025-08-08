# 🌱 GreenChain - Recycle & Donate Platform

A blockchain-based platform that rewards users for recycling by minting tokens, which can then be converted to donation credits and donated to approved NGOs.

## 🎯 Complete User Flow

1. **User scans a QR code** at a recycling center
2. **QR is validated** by the backend (Flask)
3. **If valid, smart contract mints a token** to the user's wallet
4. **User converts token into donation credit**
5. **User donates to a registered NGO**
6. **All steps are recorded on blockchain** for transparency

## 📋 QR Code Format

QR codes must follow the format: `greenchain-claim-{unique_id}`

Example: `greenchain-claim-abc12345`

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MetaMask browser extension
- Ethereum testnet (Sepolia/Goerli) or local blockchain

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY
   PRIVATE_KEY=your_private_key_here
   CONTRACT_ADDRESS=your_deployed_contract_address
   ```

3. **Deploy the smart contract:**
   ```bash
   # Deploy GreenChain.sol to your preferred network
   # Update CONTRACT_ADDRESS in .env with the deployed address
   ```

4. **Generate test QR codes:**
   ```bash
   cd backend
   python qr_generator.py
   ```

5. **Start the Flask backend:**
   ```bash
   cd backend
   python app.py
   ```

6. **Open the application:**
   - Navigate to `http://localhost:5000`

## 🧪 Testing the Complete Flow

### Step 1: Connect Wallet
1. Open the GreenChain application
2. Click "Connect MetaMask Wallet"
3. Approve the connection in MetaMask

### Step 2: Scan QR Code
1. Use the generated test QR codes from `backend/qr_codes/`
2. Open a QR code image on your phone
3. Scan it using the web app's QR scanner
4. The system will validate the QR format and mint tokens

### Step 3: Convert & Donate
1. After successful token minting, click "Convert to Donation Credits"
2. Select the number of tokens to convert
3. Choose an NGO from the dropdown
4. Enter donation amount and click "Donate"

## 📁 Project Structure

```
DevMatch2025/
├── backend/
│   ├── app.py              # Flask backend with API endpoints
│   ├── blockchain.py       # Web3 integration and smart contract calls
│   ├── qr_utils.py         # QR code validation utilities
│   ├── qr_generator.py     # Test QR code generator
│   ├── static/             # Static files (JS, CSS)
│   ├── templates/          # Flask templates
│   └── qr_codes/           # Generated test QR codes
├── contract/
│   └── GreenChain.sol      # Smart contract
├── abi.json               # Contract ABI
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🔧 API Endpoints

### POST `/api/validate-qr`
Validates QR code and mints tokens if valid.

**Request:**
```json
{
  "qr_code": "greenchain-claim-abc12345",
  "wallet_address": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tokens minted successfully! Keep recycling!",
  "transaction_hash": "0x...",
  "tokens_minted": 1
}
```

### POST `/api/convert-tokens`
Converts tokens to donation credits.

### POST `/api/donate`
Donates credits to an NGO.

### GET `/api/ngos`
Returns list of approved NGOs.

## 🔒 Smart Contract Functions

- `claimToken(uint256 amount)` - Mint tokens to user
- `convertToDonation(uint256 amount)` - Convert tokens to donation credits
- `donateToNGO(address ngo, uint256 amount)` - Donate to approved NGO
- `addNGO(address ngo)` - Add approved NGO (owner only)

## 🎨 Features

- ✅ QR code validation with proper format checking
- ✅ Multiple QR code scans (encourages recycling)
- ✅ Blockchain token minting
- ✅ Token to donation credit conversion
- ✅ NGO donation system
- ✅ Real-time token balance tracking
- ✅ Transaction transparency on blockchain
- ✅ Modern UI with Bootstrap
- ✅ MetaMask wallet integration
- ✅ Real-time QR code scanning
- ✅ Manual QR code input fallback

## 🐛 Troubleshooting

### Common Issues:

1. **"Invalid QR code format"**
   - Ensure QR codes follow the format: `greenchain-claim-{id}`

2. **"Failed to mint tokens"**
   - Check your `.env` configuration
   - Ensure you have sufficient gas fees
   - Verify contract address is correct

3. **MetaMask connection issues**
   - Ensure MetaMask is installed and unlocked
   - Check if you're on the correct network

4. **Camera not working**
   - Grant camera permissions
   - Use manual QR code input as fallback

## 🔮 Future Enhancements

- [ ] User authentication system
- [ ] Recycling center management portal
- [ ] Token marketplace
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-chain support

## 📄 License

This project is part of DevMatch2025 competition.

---

**🌱 Make the world greener, one recycle at a time!**
