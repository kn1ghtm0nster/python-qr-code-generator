"""vCard QR code generator for contact information."""

from typing import Optional
from qr_generator.utils import generate_qr_code, save_qr_code


def generate_vcard_qr(name: str, phone: Optional[str] = None, email: Optional[str] = None,
                      organization: Optional[str] = None, url: Optional[str] = None,
                      output_path: Optional[str] = None, size: int = 10,
                      error_correction: str = "M") -> str:
    """
    Generate a vCard QR code for contact information sharing.
    
    Args:
        name: Full name (required)
        phone: Phone number (optional)
        email: Email address (optional)
        organization: Company/organization name (optional)
        url: Website URL (optional)
        output_path: Output file path (default: vcard_qrcode.png)
        size: Size of each box in pixels (default: 10)
        error_correction: Error correction level (default: "M")
    
    Returns:
        Path to the saved QR code file
    
    Raises:
        ValueError: If name is empty
    """
    if not name or not name.strip():
        raise ValueError("Name is required for vCard")
    
    name = name.strip()
    
    # Build vCard in version 3.0 format
    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{name}",
    ]
    
    # Split name into N field (Last;First;Middle;Prefix;Suffix)
    name_parts = name.split()
    if len(name_parts) >= 2:
        vcard_lines.append(f"N:{name_parts[-1]};{name_parts[0]};{' '.join(name_parts[1:-1])};")
    else:
        vcard_lines.append(f"N:{name};;;;")
    
    if phone:
        phone = phone.strip()
        vcard_lines.append(f"TEL:{phone}")
    
    if email:
        email = email.strip()
        vcard_lines.append(f"EMAIL:{email}")
    
    if organization:
        organization = organization.strip()
        vcard_lines.append(f"ORG:{organization}")
    
    if url:
        url = url.strip()
        vcard_lines.append(f"URL:{url}")
    
    vcard_lines.append("END:VCARD")
    vcard_string = "\n".join(vcard_lines)
    
    if output_path is None:
        output_path = "vcard_qrcode.png"
    
    qr = generate_qr_code(vcard_string, size=size, error_correction=error_correction)
    return save_qr_code(qr, output_path)
