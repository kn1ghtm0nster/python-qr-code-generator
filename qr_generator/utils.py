"""Utility functions for QR code generation and file handling."""

import os
from pathlib import Path
from typing import Optional
import qrcode


def generate_qr_code(data: str, size: int = 10, border: int = 2, 
                     error_correction: str = "M") -> qrcode.QRCode:
    """
    Generate a QR code object from data.
    
    Args:
        data: The data to encode in the QR code
        size: Size of each box in pixels (default: 10)
        border: Border size in boxes (default: 2)
        error_correction: Error correction level ("L", "M", "Q", "H") (default: "M")
    
    Returns:
        qrcode.QRCode object
    """
    error_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    
    error_level = error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_M)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_level,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def save_qr_code(qr: qrcode.QRCode, output_path: Optional[str] = None,
                 fill_color: str = "black", back_color: str = "white") -> str:
    """
    Save a QR code to a PNG file.
    
    Args:
        qr: qrcode.QRCode object to save
        output_path: Output file path (default: qrcode.png in current directory)
        fill_color: Color of QR code modules (default: black)
        back_color: Background color (default: white)
    
    Returns:
        Path to the saved file
    """
    if output_path is None:
        output_path = "qrcode.png"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output_path)
    
    return str(output_path.resolve())


def validate_output_path(output_path: str) -> None:
    """
    Validate that the output path is writable.
    
    Args:
        output_path: Path to validate
    
    Raises:
        ValueError: If path is invalid or not writable
    """
    parent = Path(output_path).parent
    if parent.exists() and not os.access(parent, os.W_OK):
        raise ValueError(f"No write permission for directory: {parent}")
    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create output directory: {parent}") from e


def get_default_output_path(qr_type: str) -> str:
    """
    Get the default output path for a given QR code type.
    
    Args:
        qr_type: Type of QR code ("simple", "wifi", or "vcard")
    
    Returns:
        Default output path for the specified QR code type
    
    Raises:
        ValueError: If qr_type is not one of the valid types
    """
    default_paths = {
        "simple": "qr_codes/simple/qrcode.png",
        "wifi": "qr_codes/wifi/wifi_qrcode.png",
        "vcard": "qr_codes/vcard/vcard_qrcode.png",
    }
    
    if qr_type not in default_paths:
        raise ValueError(
            f"Invalid QR type: {qr_type}. Must be one of {list(default_paths.keys())}"
        )
    
    return default_paths[qr_type]
