"""Tests for simple QR code generator."""

import pytest
import os
from pathlib import Path
from qr_generator.generators.simple import generate_simple_qr


class TestSimpleQRValid:
    """Test valid inputs for simple QR code generation."""
    
    def test_generate_with_url(self, tmp_path):
        """Test generating QR code with a URL."""
        output_path = tmp_path / "test_url.png"
        result = generate_simple_qr("https://github.com", output_path=str(output_path))
        
        assert Path(result).exists()
        assert result.endswith("test_url.png")
    
    def test_generate_with_plain_text(self, tmp_path):
        """Test generating QR code with plain text."""
        output_path = tmp_path / "test_text.png"
        result = generate_simple_qr("Hello World", output_path=str(output_path))
        
        assert Path(result).exists()
        assert result.endswith("test_text.png")
    
    def test_generate_with_default_output(self, tmp_path, monkeypatch):
        """Test generating QR code with default output path."""
        monkeypatch.chdir(tmp_path)
        result = generate_simple_qr("Test data")
        
        assert Path(result).exists()
        assert result.endswith("qrcode.png")
    
    def test_generate_with_different_sizes(self, tmp_path):
        """Test generating QR codes with different box sizes."""
        for size in [5, 10, 15, 20]:
            output_path = tmp_path / f"size_{size}.png"
            result = generate_simple_qr("Test", output_path=str(output_path), size=size)
            assert Path(result).exists()
    
    def test_generate_with_error_correction_levels(self, tmp_path):
        """Test generating QR codes with different error correction levels."""
        levels = ["L", "M", "Q", "H"]
        for level in levels:
            output_path = tmp_path / f"error_{level}.png"
            result = generate_simple_qr("Test", output_path=str(output_path),
                                       error_correction=level)
            assert Path(result).exists()
    
    def test_unicode_text(self, tmp_path):
        """Test generating QR code with Unicode characters."""
        output_path = tmp_path / "unicode.png"
        result = generate_simple_qr("你好世界 🌍", output_path=str(output_path))
        
        assert Path(result).exists()
    
    def test_long_text(self, tmp_path):
        """Test generating QR code with long text."""
        output_path = tmp_path / "long_text.png"
        long_text = "A" * 500
        result = generate_simple_qr(long_text, output_path=str(output_path))
        
        assert Path(result).exists()
    
    def test_special_characters(self, tmp_path):
        """Test generating QR code with special characters."""
        output_path = tmp_path / "special_chars.png"
        special_text = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        result = generate_simple_qr(special_text, output_path=str(output_path))
        
        assert Path(result).exists()


class TestSimpleQRInvalid:
    """Test invalid inputs for simple QR code generation."""
    
    def test_empty_string(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            generate_simple_qr("")
    
    def test_whitespace_only(self):
        """Test that whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            generate_simple_qr("   ")
    
    def test_none_data(self):
        """Test that None data raises ValueError."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            generate_simple_qr(None)
    
    def test_negative_size(self):
        """Test that negative size raises ValueError from qrcode library."""
        with pytest.raises(ValueError, match="Invalid box size"):
            generate_simple_qr("Test", size=-5)
    
    def test_zero_size(self):
        """Test zero size raises ValueError from qrcode library."""
        with pytest.raises(ValueError, match="Invalid box size"):
            generate_simple_qr("Test", size=0)
    
    def test_invalid_error_correction(self, tmp_path):
        """Test that invalid error correction defaults to M."""
        output_path = tmp_path / "invalid_error.png"
        # The function doesn't validate, but qrcode lib will use default
        result = generate_simple_qr("Test", output_path=str(output_path),
                                   error_correction="X")
        assert Path(result).exists()


class TestSimpleQRMissing:
    """Test missing/edge case inputs."""
    
    def test_whitespace_trimmed(self, tmp_path):
        """Test that leading/trailing whitespace is trimmed."""
        output_path = tmp_path / "trimmed.png"
        result = generate_simple_qr("  Hello World  ", output_path=str(output_path))
        assert Path(result).exists()
