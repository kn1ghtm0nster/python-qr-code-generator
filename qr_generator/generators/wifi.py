"""WiFi QR code generator for network sharing."""

from typing import Optional, Literal
from qr_generator.utils import generate_qr_code, save_qr_code


def generate_wifi_qr(ssid: str, password: str, security: str = "WPA",
                     hidden: bool = False, output_path: Optional[str] = None,
                     size: int = 10, error_correction: str = "M") -> str:
    """
    Generate a WiFi QR code for network sharing.
    
    Args:
        ssid: Network SSID (name)
        password: Network password
        security: Security type - "WPA" (default), "WEP", or "nopass"
        hidden: Whether the network is hidden (default: False)
        output_path: Output file path (default: wifi_qrcode.png)
        size: Size of each box in pixels (default: 10)
        error_correction: Error correction level (default: "M")
    
    Returns:
        Path to the saved QR code file
    
    Raises:
        ValueError: If required parameters are invalid
    """
    if not ssid or not ssid.strip():
        raise ValueError("SSID cannot be empty")
    
    security = security.upper()
    if security not in ["WPA", "WEP", "NOPASS"]:
        raise ValueError(f"Invalid security type: {security}. Must be WPA, WEP, or NOPASS")
    
    if security != "NOPASS" and (not password or not password.strip()):
        raise ValueError(f"Password required for {security} security")
    
    ssid = ssid.strip()
    password = password.strip() if password else ""
    
    # WiFi QR code format: WIFI:T:security;S:ssid;P:password;H:hidden;;
    hidden_str = "true" if hidden else "false"
    wifi_string = f'WIFI:T:{security};S:{ssid};P:{password};H:{hidden_str};;'
    
    if output_path is None:
        output_path = "wifi_qrcode.png"
    
    qr = generate_qr_code(wifi_string, size=size, error_correction=error_correction)
    return save_qr_code(qr, output_path)
