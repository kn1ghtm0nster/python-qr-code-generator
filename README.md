# Python QR Code Generator

A modular, command-line tool for generating QR codes in Python. Supports simple text/URL QR codes, WiFi network sharing, and vCard (contact card) generation.

## Features

- **Simple QR Codes**: Convert URLs, text, or any data into QR codes
- **WiFi QR Codes**: Generate shareable WiFi network QR codes with SSID, password, and security type
- **vCard QR Codes**: Create contact card QR codes with name, phone, email, company, and website
- **Customizable Output**: Control QR code size, error correction level, and output file path
- **Error Handling**: Comprehensive validation with clear error messages
- **Extensible Design**: Modular architecture for easy addition of new QR code types

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kn1ghtm0nster/python-qr-code-generator.git
cd python-qr-code-generator
```

2. Install dependencies and the package:
```bash
pip install -e .
```

This installs the `qr` CLI command globally, along with all dependencies (qrcode, Pillow, Click).

## Usage

### Basic Help
```bash
qr --help                 # Show main help
qr simple --help          # Show simple command help
qr wifi --help            # Show WiFi command help
qr vcard --help           # Show vCard command help
```

### Simple QR Codes

Generate a QR code for a URL or text:

```bash
# Basic usage (outputs to qrcode.png)
qr simple "https://github.com"

# Custom output file
qr simple "Hello World" -o greeting.png

# Custom size (larger box size = bigger image)
qr simple "https://example.com" --size 15

# High error correction (allows more damage recovery)
qr simple "Data" --error-correction H
```

**Options:**
- `-o, --output TEXT` - Output file path (default: qrcode.png)
- `--size INTEGER` - Size of each box in pixels (default: 10)
- `--error-correction [L|M|Q|H]` - Error correction level (default: M)

### WiFi QR Codes

Generate a shareable WiFi QR code:

```bash
# Interactive mode (prompts for input)
qr wifi

# Non-interactive mode with flags
qr wifi -s "MyNetwork" -p "Password123" -t WPA -o wifi.png

# Open network (no password)
qr wifi -s "FreeWiFi" -t NOPASS -o open_wifi.png

# Hidden network
qr wifi -s "SecretNetwork" -p "Secret123" --hidden
```

**Options:**
- `-s, --ssid TEXT` - WiFi network name (SSID)
- `-p, --password TEXT` - WiFi password (leave empty for open networks)
- `-t, --security [WPA|WEP|NOPASS]` - Security type (default: WPA)
- `--hidden` - Mark network as hidden
- `-o, --output TEXT` - Output file path (default: wifi_qrcode.png)
- `--size INTEGER` - Size of each box in pixels (default: 10)
- `--error-correction [L|M|Q|H]` - Error correction level (default: M)

### vCard QR Codes

Generate a contact card QR code:

```bash
# Interactive mode
qr vcard

# Non-interactive mode
qr vcard -n "John Doe" -p "+1-555-0100" -e "john@example.com" -c "Acme Corp" -o contact.png

# Minimal vCard (name only)
qr vcard -n "Jane Smith"

# Full contact information
qr vcard \
  -n "Alice Johnson" \
  -p "+1-555-0200" \
  -e "alice@example.com" \
  -c "Tech Company" \
  -u "https://alice.example.com" \
  -o alice_contact.png
```

**Options:**
- `-n, --name TEXT` - Full name (required)
- `-p, --phone TEXT` - Phone number (optional)
- `-e, --email TEXT` - Email address (optional)
- `-c, --company TEXT` - Company/organization name (optional)
- `-u, --url TEXT` - Website URL (optional)
- `-o, --output TEXT` - Output file path (default: vcard_qrcode.png)
- `--size INTEGER` - Size of each box in pixels (default: 10)
- `--error-correction [L|M|Q|H]` - Error correction level (default: M)

## Project Structure

```
.
├── requirements.txt          # Project dependencies
├── setup.py                  # Package configuration
├── qr_generator/             # Main package
│   ├── __init__.py
│   ├── cli.py               # CLI entry point and commands
│   ├── utils.py             # Shared QR code utilities
│   └── generators/          # Generator modules
│       ├── __init__.py
│       ├── simple.py        # Simple QR generation
│       ├── wifi.py          # WiFi QR generation
│       └── vcard.py         # vCard QR generation
└── README.md                # This file
```

## Error Correction Levels

QR codes support four error correction levels:
- **L** (Low) - ~7% error correction, smallest QR code
- **M** (Medium) - ~15% error correction, default
- **Q** (Quartile) - ~25% error correction
- **H** (High) - ~30% error correction, largest QR code

Higher correction levels create larger QR codes but allow them to remain readable even if partially damaged or obscured.

## Examples

### Generate GitHub profile QR code:
```bash
qr simple "https://github.com/username" -o github.png
```

### Share home WiFi:
```bash
qr wifi -s "HomeNetwork" -p "MySecurePassword123" -o home_wifi.png
```

### Create business card QR code:
```bash
qr vcard \
  -n "Robert Smith" \
  -p "+1-555-0300" \
  -e "robert@company.com" \
  -c "Company Inc" \
  -u "https://company.com" \
  -o business_card.png
```

## Dependencies

- **qrcode[pil]** (7.4.2) - QR code generation library
- **Pillow** (10.1.0) - Image processing
- **Click** (8.1.7) - CLI framework

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the project.
