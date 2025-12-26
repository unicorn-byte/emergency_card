"""
QR Code generation utilities
"""
import qrcode
from io import BytesIO
import base64
from typing import Tuple


def generate_qr_code(data: str, size: int = 10) -> Tuple[str, bytes]:
    """
    Generate QR code for given data
    
    Args:
        data: URL or text to encode in QR code
        size: Size of QR code (default: 10)
    
    Returns:
        Tuple of (base64_encoded_image, raw_bytes)
    """
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    
    # Convert to base64 for easy transfer
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64, img_bytes


def save_qr_code(data: str, filepath: str, size: int = 10) -> bool:
    """
    Generate and save QR code to file
    
    Args:
        data: URL or text to encode
        filepath: Path to save the QR code image
        size: Size of QR code
    
    Returns:
        True if successful, False otherwise
    """
    try:
        _, img_bytes = generate_qr_code(data, size)
        
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        
        return True
    except Exception as e:
        print(f"Error saving QR code: {e}")
        return False
