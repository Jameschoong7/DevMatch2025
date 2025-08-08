import qrcode
import os
import uuid

def generate_test_qr_codes(count=5):
    """Generate test QR codes with the greenchain-claim- format"""
    
    # Create qr_codes directory if it doesn't exist
    if not os.path.exists('qr_codes'):
        os.makedirs('qr_codes')
    
    qr_codes = []
    
    for i in range(count):
        # Generate unique identifier
        unique_id = str(uuid.uuid4())[:8]
        qr_text = f"greenchain-claim-{unique_id}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        filename = f"qr_codes/test_qr_{i+1}_{unique_id}.png"
        img.save(filename)
        
        qr_codes.append({
            'text': qr_text,
            'filename': filename
        })
        
        print(f"Generated QR Code {i+1}: {qr_text}")
        print(f"Saved as: {filename}")
        print("-" * 50)
    
    return qr_codes

if __name__ == "__main__":
    print("🌱 Generating GreenChain Test QR Codes...")
    print("=" * 50)
    
    qr_codes = generate_test_qr_codes(5)
    
    print("\n✅ QR Code Generation Complete!")
    print(f"Generated {len(qr_codes)} test QR codes in the 'qr_codes' directory.")
    print("\nYou can now:")
    print("1. Open these QR code images on your phone")
    print("2. Scan them with the GreenChain app")
    print("3. Test the complete user flow")
    
    print("\n📋 QR Code Texts (for manual testing):")
    for qr in qr_codes:
        print(f"  - {qr['text']}") 