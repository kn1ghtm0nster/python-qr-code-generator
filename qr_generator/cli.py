"""Main CLI interface for QR code generation."""

import click
from pathlib import Path
from qr_generator.generators.simple import generate_simple_qr
from qr_generator.generators.wifi import generate_wifi_qr
from qr_generator.generators.vcard import generate_vcard_qr
from qr_generator.utils import validate_output_path


@click.group()
@click.version_option(version="0.1.0")
def main():
    """QR Code Generator - Create QR codes for URLs, WiFi networks, and contact cards."""
    pass


@main.command()
@click.argument("data")
@click.option("-o", "--output", default=None, help="Output file path (default: qrcode.png)")
@click.option("--size", default=10, type=int, help="Size of each box in pixels (default: 10)")
@click.option("--error-correction", default="M", type=click.Choice(["L", "M", "Q", "H"]),
              help="Error correction level (default: M)")
def simple(data: str, output: str, size: int, error_correction: str):
    """Generate a simple QR code for text or URL.
    
    Example:
        qr simple "https://github.com"
        qr simple "Hello World" -o greeting.png
    """
    try:
        if output:
            validate_output_path(output)
        
        result_path = generate_simple_qr(data, output_path=output, size=size,
                                        error_correction=error_correction)
        click.echo(f"[OK] QR code saved to: {result_path}")
    except ValueError as e:
        click.echo(f"[ERROR] {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("-s", "--ssid", prompt="Network SSID (name)", help="WiFi network name")
@click.option("-p", "--password", prompt="Password", hide_input=True, default="",
              help="WiFi password (leave empty for open networks)")
@click.option("-t", "--security", type=click.Choice(["WPA", "WEP", "NOPASS"]),
              default="WPA", help="Security type (default: WPA)")
@click.option("--hidden", is_flag=True, help="Network is hidden")
@click.option("-o", "--output", default=None, help="Output file path (default: wifi_qrcode.png)")
@click.option("--size", default=10, type=int, help="Size of each box in pixels (default: 10)")
@click.option("--error-correction", default="M", type=click.Choice(["L", "M", "Q", "H"]),
              help="Error correction level (default: M)")
def wifi(ssid: str, password: str, security: str, hidden: bool, output: str,
         size: int, error_correction: str):
    """Generate a WiFi QR code for network sharing.
    
    Example:
        qr wifi
        qr wifi -s "MyNetwork" -p "Password123" -t WPA
    """
    try:
        if output:
            validate_output_path(output)
        
        # Adjust security for open networks
        if not password or password.strip() == "":
            security = "NOPASS"
            password = ""
        
        result_path = generate_wifi_qr(ssid, password, security=security, hidden=hidden,
                                      output_path=output, size=size,
                                      error_correction=error_correction)
        click.echo(f"[OK] WiFi QR code saved to: {result_path}")
    except ValueError as e:
        click.echo(f"[ERROR] {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("-n", "--name", prompt="Full name", help="Contact full name (required)")
@click.option("-p", "--phone", default=None, help="Phone number (optional)")
@click.option("-e", "--email", default=None, help="Email address (optional)")
@click.option("-c", "--company", default=None, help="Company/organization (optional)")
@click.option("-u", "--url", default=None, help="Website URL (optional)")
@click.option("-o", "--output", default=None, help="Output file path (default: vcard_qrcode.png)")
@click.option("--size", default=10, type=int, help="Size of each box in pixels (default: 10)")
@click.option("--error-correction", default="M", type=click.Choice(["L", "M", "Q", "H"]),
              help="Error correction level (default: M)")
def vcard(name: str, phone: str, email: str, company: str, url: str, output: str,
          size: int, error_correction: str):
    """Generate a vCard QR code for contact information sharing.
    
    Example:
        qr vcard
        qr vcard -n "John Doe" -p "+1234567890" -e "john@example.com" -c "Acme Corp"
    """
    try:
        if output:
            validate_output_path(output)
        
        result_path = generate_vcard_qr(name, phone=phone, email=email,
                                       organization=company, url=url,
                                       output_path=output, size=size,
                                       error_correction=error_correction)
        click.echo(f"[OK] vCard QR code saved to: {result_path}")
    except ValueError as e:
        click.echo(f"[ERROR] {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
