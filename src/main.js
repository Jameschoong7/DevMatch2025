import { ethers } from "https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.esm.min.js";

let currentWalletAddress = null;
let currentProvider = null;
let currentSigner = null;
let scannerInitialized = false;
let tokenBalance = 0;
let donationCredits = 0;

// Check if we're on a specific page
const currentPage = window.location.pathname;

// Helper function to safely get elements
function getElement(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.warn(`Element with id '${id}' not found on page: ${currentPage}`);
    }
    return element;
}

// Helper function to save wallet connection to localStorage
function saveWalletConnection(walletAddress) {
    localStorage.setItem('greenchain_wallet_address', walletAddress);
    localStorage.setItem('greenchain_connected', 'true');
    localStorage.setItem('greenchain_connection_time', Date.now().toString());
}

// Helper function to load wallet connection from localStorage
function loadWalletConnection() {
    const savedWallet = localStorage.getItem('greenchain_wallet_address');
    const isConnected = localStorage.getItem('greenchain_connected') === 'true';
    const connectionTime = localStorage.getItem('greenchain_connection_time');
    
    // Check if connection is still valid (24 hours)
    if (isConnected && savedWallet && connectionTime) {
        const timeDiff = Date.now() - parseInt(connectionTime);
        const hoursDiff = timeDiff / (1000 * 60 * 60);
        
        if (hoursDiff < 24) {
            return savedWallet;
        } else {
            // Clear expired connection
            clearWalletConnection();
        }
    }
    return null;
}

// Helper function to clear wallet connection
function clearWalletConnection() {
    localStorage.removeItem('greenchain_wallet_address');
    localStorage.removeItem('greenchain_connected');
    localStorage.removeItem('greenchain_connection_time');
}

async function connect() {
    if (typeof window.ethereum === 'undefined') {
        window.alert("Please install Metamask from https://metamask.io/");
        return;
    }

    try {
        // Request account access
        await window.ethereum.request({ method: "eth_requestAccounts" });

        currentProvider = new ethers.providers.Web3Provider(window.ethereum);
        currentSigner = currentProvider.getSigner();
        currentWalletAddress = await currentSigner.getAddress();

        // Save wallet connection to localStorage
        saveWalletConnection(currentWalletAddress);

        // Update wallet display based on page
        updateWalletDisplay();
        
        // Initialize QR scanner if on recycle page
        if (currentPage === '/recycle' && !scannerInitialized) {
            initializeQRScanner();
        }
        
        // Load initial token balance
        await checkTokenBalance();
        
    } catch (error) {
        console.error("Connection error:", error);
        window.alert("Metamask Wallet Address Not Found");
    }
}

// Function to update wallet display across all pages
function updateWalletDisplay() {
    if (currentPage === '/login') {
        const walletElement = getElement("wallet");
        const walletAddressElement = getElement("walletAddress");
        if (walletElement) walletElement.style.display = "block";
        if (walletAddressElement) walletAddressElement.innerText = currentWalletAddress;
    } else if (currentPage === '/recycle' || currentPage === '/donation') {
        const walletInfoElement = getElement("walletInfo");
        const walletAddressElement = getElement("walletAddress");
        if (walletInfoElement) walletInfoElement.style.display = "block";
        if (walletAddressElement) walletAddressElement.innerText = currentWalletAddress;
    }
}

// Function to auto-connect wallet if previously connected
async function autoConnectWallet() {
    const savedWallet = loadWalletConnection();
    if (savedWallet && typeof window.ethereum !== 'undefined') {
        try {
            // Check if the saved wallet is still connected
            const accounts = await window.ethereum.request({ method: "eth_accounts" });
            if (accounts.length > 0 && accounts[0].toLowerCase() === savedWallet.toLowerCase()) {
                currentWalletAddress = savedWallet;
                currentProvider = new ethers.providers.Web3Provider(window.ethereum);
                currentSigner = currentProvider.getSigner();
                
                updateWalletDisplay();
                
                // Initialize QR scanner if on recycle page
                if (currentPage === '/recycle' && !scannerInitialized) {
                    initializeQRScanner();
                }
                
                // Load initial token balance
                await checkTokenBalance();
                return true;
            }
        } catch (error) {
            console.error("Auto-connect error:", error);
            clearWalletConnection();
        }
    }
    return false;
}

// QR Code Scanner (only for recycle page)
let scanner = null;

async function initializeQRScanner() {
    if (currentPage !== '/recycle') return;
    
    try {
        // Clear any existing scanner
        if (scanner) {
            scanner.clear();
            scanner = null;
        }
        
        // Check if camera is available
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        
        if (videoDevices.length === 0) {
            const resultElement = getElement("result");
            if (resultElement) {
                resultElement.innerHTML = 
                `<div class="alert alert-warning">
                    <h3>⚠️ Camera Not Available</h3>
                    <p>No camera found. Please ensure your device has a camera and grant camera permissions.</p>
                    <button onclick="requestCameraPermission()" class="btn btn-primary">Grant Camera Permission</button>
                </div>`;
            }
            return;
        }
        
        // Initialize scanner with better error handling
        scanner = new Html5QrcodeScanner('reader', {
            qrbox: {
                width: 250,
                height: 250
            },
            fps: 5,
            rememberLastUsedCamera: true,
            supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
        });
        
        scanner.render(onScanSuccess, onScanError);
        scannerInitialized = true;
        
    } catch (error) {
        console.error("Scanner initialization error:", error);
        const resultElement = getElement("result");
        if (resultElement) {
            resultElement.innerHTML = 
            `<div class="alert alert-danger">
                <h3>❌ Scanner Error</h3>
                <p>Failed to initialize QR scanner: ${error.message}</p>
                <button onclick="initializeQRScanner()" class="btn btn-primary">Retry</button>
            </div>`;
        }
    }
}

async function requestCameraPermission() {
    try {
        await navigator.mediaDevices.getUserMedia({ video: true });
        const resultElement = getElement("result");
        if (resultElement) {
            resultElement.innerHTML = 
            `<div class="alert alert-success">
                <h3>✅ Camera Permission Granted</h3>
                <p>Camera access granted. Initializing scanner...</p>
            </div>`;
        }
        
        // Wait a moment then reinitialize
        setTimeout(() => {
            initializeQRScanner();
        }, 1000);
        
    } catch (error) {
        const resultElement = getElement("result");
        if (resultElement) {
            resultElement.innerHTML = 
            `<div class="alert alert-danger">
                <h3>❌ Camera Permission Denied</h3>
                <p>Camera access is required to scan QR codes. Please grant camera permission and refresh the page.</p>
                <button onclick="location.reload()" class="btn btn-primary">Refresh Page</button>
            </div>`;
        }
    }
}

function onScanSuccess(result) {
    console.log("QR Code scanned: ", result);
    
    // Stop scanning immediately
    if (scanner) {
        scanner.clear();
        scanner = null;
    }
    
    // Validate QR code format
    if (!result.startsWith('greenchain-claim-')) {
        const resultElement = getElement("result");
        if (resultElement) {
            resultElement.innerHTML = 
            `<div class="alert alert-danger">
                <h3>Invalid QR Code!</h3>
                <p>This QR code is not a valid GreenChain claim code.</p>
                <button onclick="resetScanner()" class="btn btn-primary">Scan Again</button>
            </div>`;
        }
        return;
    }
    
    // Send to backend for validation and token minting
    validateAndMintTokens(result);
}

function onScanError(error) {
    // Only log errors, don't show them to user unless they're critical
    console.error("QR Code scan error: ", error);
    
    // Don't show error messages for normal scanning attempts
    // Only show errors for critical issues
    if (error.message && error.message.includes('IndexSizeError')) {
        // This is a canvas error, try to reinitialize
        setTimeout(() => {
            if (scanner) {
                scanner.clear();
                scanner = null;
            }
            initializeQRScanner();
        }, 1000);
    }
}

function resetScanner() {
    if (currentPage !== '/recycle') return;
    
    const resultElement = getElement("result");
    const readerElement = getElement("reader");
    
    if (resultElement) resultElement.innerHTML = "";
    if (readerElement) readerElement.innerHTML = "";
    
    // Wait a moment before reinitializing
    setTimeout(() => {
        initializeQRScanner();
    }, 500);
}

function submitManualQr() {
    const manualQrInput = getElement("manualQrInput");
    if (!manualQrInput) return;
    
    const qrCode = manualQrInput.value.trim();
    
    if (!qrCode) {
        alert("Please enter a QR code");
        return;
    }
    
    // Validate QR code format
    if (!qrCode.startsWith('greenchain-claim-')) {
        alert("Invalid QR code format. Must start with 'greenchain-claim-'");
        return;
    }
    
    // Process the manual QR code
    validateAndMintTokens(qrCode);
    
    // Clear the input
    manualQrInput.value = "";
}

async function validateAndMintTokens(qrCode) {
    if (!currentWalletAddress) {
        alert("Please connect your wallet first!");
        return;
    }
    
    try {
        const resultElement = getElement("result");
        if (resultElement) {
            resultElement.innerHTML = 
            `<div class="alert alert-info">
                <h3>Processing...</h3>
                <p>Validating QR code and minting tokens...</p>
            </div>`;
        }
        
        const response = await fetch('/api/validate-qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                qr_code: qrCode,
                wallet_address: currentWalletAddress
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update token balance from server response
            tokenBalance = data.new_balance;
            updateTokenBalanceDisplay();
            
            if (resultElement) {
                resultElement.innerHTML = 
                `<div class="alert alert-success">
                    <h3>🎉 Success!</h3>
                    <p>${data.message}</p>
                    <p><strong>Tokens Minted:</strong> ${data.tokens_minted}</p>
                    <p><strong>New Balance:</strong> ${data.new_balance} tokens</p>
                    <p><strong>Transaction Hash:</strong> ${data.transaction_hash}</p>
                    <button onclick="resetScanner()" class="btn btn-primary">Scan Another QR Code</button>
                    
                    <p class="mt-2"><small class="text-success">♻️ Keep recycling! You can scan the same QR code again for more tokens.</small></p>
                </div>`;
            }
        } else {
            if (resultElement) {
                resultElement.innerHTML = 
                `<div class="alert alert-danger">
                    <h3>❌ Error</h3>
                    <p>${data.error}</p>
                    <button onclick="resetScanner()" class="btn btn-primary">Try Again</button>
                </div>`;
            }
        }
    } catch (error) {
        const resultElement = getElement("result");
        if (resultElement) {
            resultElement.innerHTML = 
            `<div class="alert alert-danger">
                <h3>❌ Network Error</h3>
                <p>Failed to connect to server: ${error.message}</p>
                <button onclick="resetScanner()" class="btn btn-primary">Try Again</button>
            </div>`;
        }
    }
}

async function checkTokenBalance() {
    if (!currentWalletAddress) {
        if (currentPage === '/recycle' || currentPage === '/donation') {
            const tokenBalanceElement = getElement("token_balance");
            if (tokenBalanceElement) {
                tokenBalanceElement.innerText = "Please connect wallet first";
            }
        }
        return;
    }
    
    try {
        if (currentPage === '/recycle' || currentPage === '/donation') {
            const tokenBalanceElement = getElement("token_balance");
            if (tokenBalanceElement) {
                tokenBalanceElement.innerText = "Loading...";
            }
        }
        
        // Fetch balance from server
        const response = await fetch(`/api/balance/${currentWalletAddress}`);
        const data = await response.json();
        
        if (data.success) {
            tokenBalance = data.token_balance;
            donationCredits = data.credits_balance;
            updateTokenBalanceDisplay();
        } else {
            throw new Error(data.error || 'Failed to fetch balance');
        }
        
    } catch (error) {
        if (currentPage === '/recycle' || currentPage === '/donation') {
            const tokenBalanceElement = getElement("token_balance");
            if (tokenBalanceElement) {
                tokenBalanceElement.innerText = `Error - ${error.message}`;
            }
        }
    }
}

function updateTokenBalanceDisplay() {
    if (currentPage === '/recycle' || currentPage === '/donation') {
        const tokenBalanceElement = getElement("token_balance");
        if (tokenBalanceElement) {
            tokenBalanceElement.innerHTML = `
                <strong>Token Balance:</strong> ${tokenBalance} tokens<br>
                <strong>Donation Credits:</strong> ${donationCredits} credits
            `;
        }
        
        // Update available tokens in donation page
        if (currentPage === '/donation') {
            const availableTokensElement = getElement("availableTokens");
            if (availableTokensElement) {
                availableTokensElement.textContent = tokenBalance;
            }
        }
    }
}

async function showDonationOptions() {
    try {
        const response = await fetch('/api/ngos');
        const data = await response.json();
        
        let ngoOptions = data.ngos.map(ngo => 
            `<option value="${ngo.address}">${ngo.name} (${ngo.address})</option>`
        ).join('');
        
        const donationOptionsElement = getElement("donation-options");
        if (donationOptionsElement) {
            donationOptionsElement.innerHTML = `
                <div class="row">
                    <div class="col-md-8">
                        <div class="form-group">
                            <label for="ngoSelect">
                                <img src="https://img.icons8.com/color/16/000000/organization.png" alt="NGO" style="margin-right: 5px;">
                                Select NGO:
                            </label>
                            <select id="ngoSelect" class="form-control">
                                ${ngoOptions}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label for="donationAmount">
                                <img src="https://img.icons8.com/color/16/000000/coins.png" alt="Amount" style="margin-right: 5px;">
                                Donation amount (credits):
                            </label>
                            <input type="number" id="donationAmount" class="form-control" value="1" min="1" max="${donationCredits}">
                            <small class="text-muted">Available credits: ${donationCredits}</small>
                        </div>
                        <button onclick="donateToNGO()" class="btn btn-donate w-100 mt-3">
                            <img src="https://img.icons8.com/color/16/000000/heart.png" alt="Donate" style="margin-right: 5px;">
                            Donate
                        </button>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error("Failed to load NGOs:", error);
    }
}

async function convertTokens() {
    const tokenAmountElement = getElement("tokenAmount");
    if (!tokenAmountElement) return;
    
    const amount = parseInt(tokenAmountElement.value);
    
    if (amount > tokenBalance) {
        alert("❌ Not enough tokens! You only have " + tokenBalance + " tokens.");
        return;
    }
    
    try {
        const response = await fetch('/api/convert-tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                wallet_address: currentWalletAddress,
                amount: amount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update balances from server response
            tokenBalance = data.new_token_balance;
            donationCredits = data.new_credits_balance;
            updateTokenBalanceDisplay();
            
            alert(`✅ ${data.message}`);
            
            // Show donation options after conversion
            showDonationOptions();
        } else {
            alert(`❌ Error: ${data.error}`);
        }
    } catch (error) {
        alert(`❌ Network Error: ${error.message}`);
    }
}

async function donateToNGO() {
    const ngoSelectElement = getElement("ngoSelect");
    const donationAmountElement = getElement("donationAmount");
    
    if (!ngoSelectElement || !donationAmountElement) return;
    
    const ngoAddress = ngoSelectElement.value;
    const amount = parseInt(donationAmountElement.value);
    
    if (amount > donationCredits) {
        alert("❌ Not enough donation credits! You only have " + donationCredits + " credits.");
        return;
    }
    
    try {
        const response = await fetch('/api/donate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                wallet_address: currentWalletAddress,
                ngo_address: ngoAddress,
                amount: amount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update donation credits from server response
            donationCredits = data.new_credits_balance;
            updateTokenBalanceDisplay();
            
            alert(`✅ ${data.message}`);
            
            // Refresh donation options to show updated balances
            showDonationOptions();
        } else {
            alert(`❌ Error: ${data.error}`);
        }
    } catch (error) {
        alert(`❌ Network Error: ${error.message}`);
    }
}

// Make functions globally accessible
window.connect = connect;
window.resetScanner = resetScanner;
window.submitManualQr = submitManualQr;
window.showDonationOptions = showDonationOptions;
window.convertTokens = convertTokens;
window.donateToNGO = donateToNGO;
window.requestCameraPermission = requestCameraPermission;
window.initializeQRScanner = initializeQRScanner;
window.checkTokenBalance = checkTokenBalance;

window.onload = async function () {
    console.log("Page loaded:", currentPage);
    
    // Try to auto-connect wallet first
    const autoConnected = await autoConnectWallet();
    
    // Add event listeners based on current page
    if (currentPage === '/login') {
        const btnConnect = getElement("btnConnect");
        if (btnConnect) {
            btnConnect.addEventListener("click", connect);
        }
    } else if (currentPage === '/recycle') {
        const btnDisplayBalance = getElement("btnDisplayBalance");
        if (btnDisplayBalance) {
            btnDisplayBalance.addEventListener("click", checkTokenBalance);
        }
        // Initialize QR scanner if wallet is already connected
        if (autoConnected || (typeof window.ethereum !== 'undefined' && window.ethereum.selectedAddress)) {
            if (!autoConnected) {
                connect();
            }
        }
    } else if (currentPage === '/donation') {
        const btnDisplayBalance = getElement("btnDisplayBalance");
        if (btnDisplayBalance) {
            btnDisplayBalance.addEventListener("click", checkTokenBalance);
        }
        // Check if wallet is already connected and auto-refresh balance
        if (autoConnected || (typeof window.ethereum !== 'undefined' && window.ethereum.selectedAddress)) {
            if (!autoConnected) {
                connect();
            }
            // Auto-refresh balance when switching to donation page
            setTimeout(() => {
                checkTokenBalance();
            }, 500);
        }
    }
}; 