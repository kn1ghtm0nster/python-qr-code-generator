"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def sample_output_file(tmp_path):
    """Fixture providing a temporary output file path."""
    return tmp_path / "test_output.png"


@pytest.fixture
def sample_data():
    """Fixture providing various test data samples."""
    return {
        "url": "https://example.com",
        "text": "Hello World",
        "unicode": "你好世界 🌍",
        "special_chars": "!@#$%^&*()",
        "long_text": "A" * 500,
        "ssid": "TestNetwork",
        "password": "Password123",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
    }


@pytest.fixture(autouse=True)
def mock_save_qr_code():
    """
    Mock fixture for save_qr_code function.
    
    Automatically applied to all tests to prevent actual file creation.
    Returns a predictable path string without creating real files.
    """
    with patch("qr_generator.utils.save_qr_code") as mock:
        mock.return_value = "qr_codes/{qr_type}/qrcode.png"
        yield mock
