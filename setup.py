from setuptools import setup, find_packages

setup(
    name="qr-generator",
    version="0.1.0",
    description="CLI-based QR code generator with support for URLs, WiFi, and vCards",
    author="QR Generator Contributors",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "qrcode[pil]==7.4.2",
        "click==8.1.7",
        "Pillow==10.1.0",
    ],
    entry_points={
        "console_scripts": [
            "qr-gen=qr_generator.cli:main",
        ],
    },
)
