"""Simple QR code generator for URLs and text."""

from typing import Optional
from qr_generator.utils import generate_qr_code, save_qr_code


def generate_simple_qr(data: str, output_path: Optional[str] = None,
                       size: int = 10, error_correction: str = "M") -> str:
    """
    Generate a simple QR code from text or URL.
    
    Args:
        data: The text or URL to encode
        output_path: Output file path (default: qrcode.png)
        size: Size of each box in pixels (default: 10)
        error_correction: Error correction level (default: "M")
    
    Returns:
        Path to the saved QR code file
    
    Raises:
        ValueError: If data is empty
    """
    if not data or not data.strip():
        raise ValueError("Data cannot be empty")
    
    qr = generate_qr_code(data.strip(), size=size, error_correction=error_correction)
    return save_qr_code(qr, output_path)
