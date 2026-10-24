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

### Important: Editable Install Required

This is a Python CLI tool that must be installed in **editable mode** (`pip install -e .`). Simply running `pip install -r requirements.txt` will **NOT** make the `qr-gen` command available in your terminal. The editable install both installs dependencies and registers the CLI command in your environment.

### Setup Instructions by Operating System

#### WSL (Windows Subsystem for Linux)

1. Clone the repository:
```bash
git clone https://github.com/kn1ghtm0nster/python-qr-code-generator.git
cd python-qr-code-generator
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

4. Install dependencies and the CLI:
```bash
python -m pip install -e .
```

5. Verify installation:
```bash
qr-gen --help
```

#### Windows (PowerShell or CMD)

1. Clone the repository:
```bash
git clone https://github.com/kn1ghtm0nster/python-qr-code-generator.git
cd python-qr-code-generator
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:

**PowerShell:**
```powershell
.\.venv\Scripts\activate
```

**Command Prompt (CMD):**
```cmd
.venv\Scripts\activate.bat
```

4. Install dependencies and the CLI:
```bash
python -m pip install -e .
```

5. Verify installation:
```bash
qr-gen --help
```

#### macOS

1. Clone the repository:
```bash
git clone https://github.com/kn1ghtm0nster/python-qr-code-generator.git
cd python-qr-code-generator
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

4. Install dependencies and the CLI:
```bash
python -m pip install -e .
```

5. Verify installation:
```bash
qr-gen --help
```

## Usage

### Basic Help
```bash
qr-gen --help                 # Show main help
qr-gen simple --help          # Show simple command help
qr-gen wifi --help            # Show WiFi command help
qr-gen vcard --help           # Show vCard command help
```

### Simple QR Codes

Generate a QR code for a URL or text:

```bash
# Basic usage (outputs to qrcode.png)
qr-gen simple "https://github.com"

# Custom output file
qr-gen simple "Hello World" -o greeting.png

# Custom size (larger box size = bigger image)
qr-gen simple "https://example.com" --size 15

# High error correction (allows more damage recovery)
qr-gen simple "Data" --error-correction H
```

**Options:**
- `-o, --output TEXT` - Output file path (default: qrcode.png)
- `--size INTEGER` - Size of each box in pixels (default: 10)
- `--error-correction [L|M|Q|H]` - Error correction level (default: M)

### WiFi QR Codes

Generate a shareable WiFi QR code:

```bash
# Interactive mode (prompts for input)
qr-gen wifi

# Non-interactive mode with flags
qr-gen wifi -s "MyNetwork" -p "Password123" -t WPA -o wifi.png

# Open network (no password)
qr-gen wifi -s "FreeWiFi" -t NOPASS -o open_wifi.png

# Hidden network
qr-gen wifi -s "SecretNetwork" -p "Secret123" --hidden
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
qr-gen vcard

# Non-interactive mode
qr-gen vcard -n "John Doe" -p "+1-555-0100" -e "john@example.com" -c "Acme Corp" -o contact.png

# Minimal vCard (name only)
qr-gen vcard -n "Jane Smith"

# Full contact information
qr-gen vcard \
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

## Output Structure

By default, generated QR codes are saved to the `qr_codes/` directory organized by type:

```
qr_codes/
├── simple/
│   ├── qrcode.png
│   └── github.png
├── wifi/
│   └── home_wifi.png
└── vcard/
    ├── business_card.png
    └── alice_contact.png
```

**Custom Output Path:** You can specify a custom output location using the `-o` flag:

```bash
# Save to a specific path
qr-gen simple "https://example.com" -o /path/to/my-qr.png

# Save to current directory
qr-gen wifi -s "Network" -p "Pass" -o ./wifi.png

# Use relative paths
qr-gen vcard -n "John" -o ./contacts/john.png
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
qr-gen simple "https://github.com/username" -o github.png
```

### Share home WiFi:
```bash
qr-gen wifi -s "HomeNetwork" -p "MySecurePassword123" -o home_wifi.png
```

### Create business card QR code:
```bash
qr-gen vcard \
  -n "Robert Smith" \
  -p "+1-555-0300" \
  -e "robert@company.com" \
  -c "Company Inc" \
  -u "https://company.com" \
  -o business_card.png
```

## Troubleshooting

### "command not found: qr-gen"

**Problem:** You're getting "command not found" when trying to run `qr-gen`.

**Solution:**
1. Make sure your virtual environment is activated:
   - WSL/macOS: `source .venv/bin/activate`
   - Windows (PowerShell): `.\.venv\Scripts\activate`
   - Windows (CMD): `.venv\Scripts\activate.bat`

2. Make sure you installed in editable mode:
   ```bash
   python -m pip install -e .
   ```

3. Verify the venv is active (you should see `(.venv)` in your prompt)

### "ModuleNotFoundError: No module named 'qr_generator'"

**Problem:** You're getting a ModuleNotFoundError when trying to run the CLI.

**Solution:**
1. Ensure your virtual environment is activated
2. Reinstall the package in editable mode:
   ```bash
   python -m pip install -e .
   ```
3. Verify with: `qr-gen --help`

### Virtual Environment Not Activating

**Problem:** The activate command doesn't seem to work.

**Solution:**
- Verify you're in the project directory where `.venv` folder exists
- Check the exact activation command for your shell:
  - **Bash/Zsh (WSL/macOS):** `source .venv/bin/activate`
  - **PowerShell (Windows):** `.\.venv\Scripts\activate`
  - **Command Prompt (Windows):** `.venv\Scripts\activate.bat`
- Restart your terminal/shell if issues persist


## Dependencies

- **qrcode[pil]** (7.4.2) - QR code generation library
- **Pillow** (10.1.0) - Image processing
- **Click** (8.1.7) - CLI framework

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the project.
