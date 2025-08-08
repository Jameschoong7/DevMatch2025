
import { ethers } from "https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.esm.min.js";

async function connect() {
    if (typeof window.ethereum === 'undefined') {
        window.alert("Please install Metamask from https://metamask.io/");
        return;
    }

    try {
        // Request account access
        await window.ethereum.request({ method: "eth_requestAccounts" });

        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        const walletAddress = await signer.getAddress();

      //   console.log(walletAddress);
        document.getElementById("wallet").innerText = `Wallet: ${walletAddress}`;
    } catch (error) {
        window.alert("Metamask Wallet Address Not Found");
    }
}

window.onload = function () {
    document.getElementById("btnConnect").addEventListener("click", connect);
};

//Qr Code Scanner
const scanner = new Html5QrcodeScanner('reader',{
      qrbox: {
          width: 250, //qrcode box width
          height: 250 // qrcode box height
      },
      fps: 20,
});

//using qr scanner
scanner.render(onScanSuccess, onScanError);

function onScanSuccess(result) {
      console.log("QR Code scanned: ", result);
      // document.getElementById("result").innerHTML = `QR Code Result: ${result}`;
      document.getElementById("result").innerHTML = 
      `<h2>Success!</h2>
      <p><a href="${result}">${result}</a></p>`;
      //end the scanning process
      scanner.clear();
      //remove reader element
      document.getElementById("reader").remove(); 
}

function onScanError(error) {
      console.error("QR Code scan error: ", error);
      // document.getElementById("result").innerHTML = `<p>Error scanning QR Code: ${error}</p>`;
}