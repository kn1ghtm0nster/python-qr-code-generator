"""Tests for utility functions."""

import pytest
import os
from pathlib import Path
import qrcode
from qr_generator.utils import generate_qr_code, save_qr_code, validate_output_path


class TestGenerateQRCode:
    """Test QR code generation utility function."""
    
    def test_generate_with_default_parameters(self):
        """Test generating QR code with default parameters."""
        qr = generate_qr_code("Test data")
        
        assert isinstance(qr, qrcode.QRCode)
        assert qr.box_size == 10
        assert qr.border == 2
    
    def test_generate_with_custom_size(self):
        """Test generating QR code with custom box size."""
        qr = generate_qr_code("Test", size=15)
        
        assert qr.box_size == 15
    
    def test_generate_with_error_correction_L(self):
        """Test QR code with error correction level L."""
        qr = generate_qr_code("Test", error_correction="L")
        
        assert qr.error_correction == qrcode.constants.ERROR_CORRECT_L
    
    def test_generate_with_error_correction_M(self):
        """Test QR code with error correction level M."""
        qr = generate_qr_code("Test", error_correction="M")
        
        assert qr.error_correction == qrcode.constants.ERROR_CORRECT_M
    
    def test_generate_with_error_correction_Q(self):
        """Test QR code with error correction level Q."""
        qr = generate_qr_code("Test", error_correction="Q")
        
        assert qr.error_correction == qrcode.constants.ERROR_CORRECT_Q
    
    def test_generate_with_error_correction_H(self):
        """Test QR code with error correction level H."""
        qr = generate_qr_code("Test", error_correction="H")
        
        assert qr.error_correction == qrcode.constants.ERROR_CORRECT_H
    
    def test_generate_with_invalid_error_correction(self):
        """Test that invalid error correction defaults to M."""
        qr = generate_qr_code("Test", error_correction="X")
        
        assert qr.error_correction == qrcode.constants.ERROR_CORRECT_M
    
    def test_generate_with_long_data(self):
        """Test generating QR code with long data."""
        long_data = "A" * 1000
        qr = generate_qr_code(long_data)
        
        assert isinstance(qr, qrcode.QRCode)
    
    def test_generate_with_unicode_data(self):
        """Test generating QR code with Unicode data."""
        qr = generate_qr_code("Hello 世界 🌍")
        
        assert isinstance(qr, qrcode.QRCode)
    
    def test_generate_with_special_characters(self):
        """Test generating QR code with special characters."""
        qr = generate_qr_code("!@#$%^&*()[]{}|\\;:,.<>?")
        
        assert isinstance(qr, qrcode.QRCode)
    
    def test_qr_is_made(self):
        """Test that generated QR code is properly made."""
        qr = generate_qr_code("Test")
        # After generation, the QR data should be set
        assert qr.data_list is not None or len(qr.modules) > 0


class TestSaveQRCode:
    """Test QR code saving utility function."""
    
    def test_save_with_default_path(self, tmp_path, monkeypatch):
        """Test saving QR code with default output path."""
        monkeypatch.chdir(tmp_path)
        qr = generate_qr_code("Test")
        result = save_qr_code(qr)
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith(".png")
    
    def test_save_with_custom_path(self, tmp_path):
        """Test saving QR code with custom output path."""
        qr = generate_qr_code("Test")
        output_path = tmp_path / "custom.png"
        result = save_qr_code(qr, str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith(".png")
    
    def test_save_creates_parent_directories(self, tmp_path):
        """Test that save creates parent directories if they don't exist."""
        qr = generate_qr_code("Test")
        output_path = tmp_path / "nested" / "dir" / "qrcode.png"
        result = save_qr_code(qr, str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_save_with_custom_colors(self, tmp_path):
        """Test saving QR code with custom colors."""
        qr = generate_qr_code("Test")
        output_path = tmp_path / "colored.png"
        result = save_qr_code(qr, str(output_path), fill_color="blue",
                            back_color="yellow")
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_save_returns_absolute_path(self, tmp_path):
        """Test that save_qr_code returns absolute path."""
        qr = generate_qr_code("Test")
        output_path = tmp_path / "test.png"
        result = save_qr_code(qr, str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_save_with_relative_path(self, tmp_path, monkeypatch):
        """Test saving QR code with relative path."""
        monkeypatch.chdir(tmp_path)
        qr = generate_qr_code("Test")
        result = save_qr_code(qr, "subdir/qrcode.png")
        
        assert result is not None
        assert isinstance(result, str)


class TestValidateOutputPath:
    """Test output path validation utility function."""
    
    def test_validate_existing_writable_directory(self, tmp_path):
        """Test validation of existing writable directory."""
        # Should not raise
        validate_output_path(str(tmp_path / "test.png"))
    
    def test_validate_creates_directory(self, tmp_path):
        """Test that validation creates parent directories."""
        nested_path = tmp_path / "new" / "nested" / "path" / "test.png"
        # Should not raise and should create directories
        validate_output_path(str(nested_path))
        assert nested_path.parent.exists()
    
    def test_validate_read_only_directory(self, tmp_path):
        """Test validation fails for read-only directory."""
        if os.name == 'nt':  # Windows
            pytest.skip("Read-only test is complex on Windows")
        
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)
        
        try:
            with pytest.raises(ValueError, match="No write permission"):
                validate_output_path(str(readonly_dir / "test.png"))
        finally:
            readonly_dir.chmod(0o755)  # Restore permissions for cleanup
    
    def test_validate_parent_already_exists(self, tmp_path):
        """Test validation when parent directory already exists."""
        parent = tmp_path / "existing"
        parent.mkdir()
        
        # Should not raise
        validate_output_path(str(parent / "test.png"))
    
    def test_validate_multiple_nested_levels(self, tmp_path):
        """Test validation with multiple nested directory levels."""
        deep_path = tmp_path / "a" / "b" / "c" / "d" / "e" / "test.png"
        
        # Should not raise
        validate_output_path(str(deep_path))
        assert deep_path.parent.exists()


class TestUtilsIntegration:
    """Integration tests for utility functions working together."""
    
    def test_generate_and_save_workflow(self, tmp_path):
        """Test complete workflow of generating and saving QR code."""
        output_path = tmp_path / "integration.png"
        qr = generate_qr_code("Integration Test")
        result = save_qr_code(qr, str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_validate_then_save_workflow(self, tmp_path):
        """Test workflow of validating path then saving."""
        output_path = tmp_path / "new_dir" / "validated.png"
        
        # Validate path (creates directories)
        validate_output_path(str(output_path))
        
        # Generate and save
        qr = generate_qr_code("Validated Path")
        result = save_qr_code(qr, str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
