# qr_utils.py
import re

QR_PATTERN = r"^greenchain-claim-[a-zA-Z0-9]+$"

def validate_qr_code(qr_string: str) -> bool:
    """
    Validate that the QR code string matches the expected format.
    Example: greenchain-claim-xyz123
    """
    return bool(re.match(QR_PATTERN, qr_string))
