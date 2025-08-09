# GreenChain - Recycle & Donate Platform

A blockchain-based platform that rewards users for recycling by minting tokens, which can then be converted to donation credits and donated to approved NGOs.

## User Flow

1. **User scans a QR code** at a recycling center
2. **QR is validated** by the backend (Flask)
3. **If valid, smart contract mints a token** to the user's wallet
4. **User converts token into donation credit**
5. **User donates to a registered NGO**
6. **All steps are recorded on blockchain** for transparency

## QR Code Format

QR codes must follow the format: `greenchain-claim-{unique_id}`

Example: `greenchain-claim-abc12345`

## Quick Start

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
├── abi.json
├── backend/
│ ├── app.py               # Flask app; serves static from ../src
│ ├── blockchain.py        # Web3/contract integration
│ ├── qr_utils.py          # QR code validation
│ ├── qr_generator.py      # Test QR generator
│ ├── qr_codes/            # Generated test QR images
│ │ ├── test_qr_1_531ffe6b.png
│ │ ├── test_qr_2_8bfa09bc.png
│ │ ├── test_qr_3_766934fc.png
│ │ ├── test_qr_4_f7ca1262.png
│ │ └── test_qr_5_61b47c80.png
│ └── templates/           # Flask templates
│ ├── index.html
│ ├── login.html
│ ├── recycle.html
│ ├── donation.html
│ └── ngo_transparency.html
├── contract/
│ └── GreenChain.sol       # Smart contract
├── src/                   # Static assets served by Flask
│ ├── main.js
│ ├── donation.png
│ ├── greenchain.png
│ ├── logout.png
│ ├── transparency.png
│ ├── triangular-arrows-sign-for-recycle.png
│ └── user.png
├── BUSINESS_MODEL_ANALYSIS.md
├── SYSTEM_ANALYSIS_SUMMARY.md
├── deployment.md
├── requirements.txt
└── README.md
```



## 🎨 Features

- ✅ QR code validation with proper format checking
- ✅ Multiple QR code scans (encourages recycling)
- ✅ Blockchain token minting
- ✅ Token to donation credit conversion
- ✅ NGO donation system
- ✅ Real-time token balance tracking
- ✅ Transaction transparency on blockchain
- ✅ MetaMask wallet integration
- ✅ Real-time QR code scanning
- ✅ Manual QR code input fallback

## 🐛 Troubleshooting

### Common Issues:

1. **"Invalid QR code format"**
   - Ensure QR codes follow the format: `greenchain-claim-{id}`

2. **"Failed to mint tokens"**
   - Check your `.env` configuration
   - Ensure sufficient gas fees
   - Verify contract address is correct

3. **MetaMask connection issues**
   - Ensure MetaMask is installed and unlocked
   - Check network

4. **Camera not working**
   - Grant camera permissions
   - Use manual QR code input as fallback

