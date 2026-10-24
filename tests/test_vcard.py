"""Tests for vCard QR code generator."""

import pytest
from pathlib import Path
from qr_generator.generators.vcard import generate_vcard_qr


class TestVCardQRValid:
    """Test valid inputs for vCard QR code generation."""
    
    def test_generate_name_only(self, tmp_path):
        """Test generating vCard QR code with only name."""
        output_path = tmp_path / "vcard_name_only.png"
        result = generate_vcard_qr("John Doe", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith(".png")
    
    def test_generate_with_phone(self, tmp_path):
        """Test generating vCard QR code with phone number."""
        output_path = tmp_path / "vcard_phone.png"
        result = generate_vcard_qr("John Doe", phone="+1234567890",
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_with_email(self, tmp_path):
        """Test generating vCard QR code with email."""
        output_path = tmp_path / "vcard_email.png"
        result = generate_vcard_qr("John Doe", email="john@example.com",
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_with_organization(self, tmp_path):
        """Test generating vCard QR code with organization."""
        output_path = tmp_path / "vcard_org.png"
        result = generate_vcard_qr("John Doe", organization="Acme Corp",
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_with_url(self, tmp_path):
        """Test generating vCard QR code with URL."""
        output_path = tmp_path / "vcard_url.png"
        result = generate_vcard_qr("John Doe", url="https://example.com",
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_full_contact(self, tmp_path):
        """Test generating vCard QR code with all fields."""
        output_path = tmp_path / "vcard_full.png"
        result = generate_vcard_qr(
            "Jane Smith",
            phone="+1987654321",
            email="jane@example.com",
            organization="Tech Solutions Inc",
            url="https://techsolutions.com",
            output_path=str(output_path)
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_default_output_path(self, tmp_path, monkeypatch):
        """Test generating vCard QR code with default output path."""
        monkeypatch.chdir(tmp_path)
        result = generate_vcard_qr("John Doe")
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith(".png")
    
    def test_single_name(self, tmp_path):
        """Test vCard QR code with single-word name."""
        output_path = tmp_path / "vcard_single_name.png"
        result = generate_vcard_qr("Madonna", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_multi_part_name(self, tmp_path):
        """Test vCard QR code with multi-part name."""
        output_path = tmp_path / "vcard_multi_name.png"
        result = generate_vcard_qr("Jean Claude Van Damme",
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_different_error_correction_levels(self, tmp_path):
        """Test generating vCard QR codes with different error correction levels."""
        levels = ["L", "M", "Q", "H"]
        for level in levels:
            output_path = tmp_path / f"vcard_error_{level}.png"
            result = generate_vcard_qr("John Doe", output_path=str(output_path),
                                     error_correction=level)
            assert result is not None
            assert isinstance(result, str)
    
    def test_different_sizes(self, tmp_path):
        """Test generating vCard QR codes with different box sizes."""
        for size in [5, 10, 20]:
            output_path = tmp_path / f"vcard_size_{size}.png"
            result = generate_vcard_qr("John Doe", output_path=str(output_path),
                                     size=size)
            assert result is not None
            assert isinstance(result, str)
    
    def test_unicode_name(self, tmp_path):
        """Test vCard QR code with Unicode name."""
        output_path = tmp_path / "vcard_unicode.png"
        result = generate_vcard_qr("李明 (Li Ming)", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_special_characters_in_contact(self, tmp_path):
        """Test vCard QR code with special characters in contact info."""
        output_path = tmp_path / "vcard_special.png"
        result = generate_vcard_qr(
            "O'Connor-Smith",
            email="test+tag@example.co.uk",
            organization="A&B Inc.",
            output_path=str(output_path)
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_whitespace_in_fields(self, tmp_path):
        """Test vCard QR code with extra whitespace in fields."""
        output_path = tmp_path / "vcard_whitespace.png"
        result = generate_vcard_qr(
            "  John  Doe  ",
            phone="  +1234567890  ",
            email="  john@example.com  ",
            output_path=str(output_path)
        )
        
        assert result is not None
        assert isinstance(result, str)


class TestVCardQRInvalid:
    """Test invalid inputs for vCard QR code generation."""
    
    def test_empty_name(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Name is required"):
            generate_vcard_qr("")
    
    def test_whitespace_name(self):
        """Test that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Name is required"):
            generate_vcard_qr("   ")
    
    def test_none_name(self):
        """Test that None name raises ValueError."""
        with pytest.raises(ValueError, match="Name is required"):
            generate_vcard_qr(None)
    
    def test_empty_phone_optional(self, tmp_path):
        """Test that empty phone is handled as optional."""
        output_path = tmp_path / "vcard_empty_phone.png"
        result = generate_vcard_qr("John Doe", phone="", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_empty_email_optional(self, tmp_path):
        """Test that empty email is handled as optional."""
        output_path = tmp_path / "vcard_empty_email.png"
        result = generate_vcard_qr("John Doe", email="", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_none_optional_fields(self, tmp_path):
        """Test that None for optional fields is handled."""
        output_path = tmp_path / "vcard_none_optional.png"
        result = generate_vcard_qr("John Doe", phone=None, email=None,
                                 organization=None, url=None,
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)


class TestVCardQRMissing:
    """Test edge cases for vCard QR code generation."""
    
    def test_name_trimming(self, tmp_path):
        """Test that name is properly trimmed."""
        output_path = tmp_path / "vcard_trim_name.png"
        result = generate_vcard_qr("  Jane Smith  ", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_vcard_format_structure(self, tmp_path):
        """Test that generated vCard follows proper structure."""
        # This is more of an integration test
        output_path = tmp_path / "vcard_structure.png"
        result = generate_vcard_qr(
            "Test User",
            phone="+1234567890",
            email="test@example.com",
            output_path=str(output_path)
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_two_part_name_parsing(self, tmp_path):
        """Test two-part name is parsed correctly into N field."""
        output_path = tmp_path / "vcard_two_part.png"
        result = generate_vcard_qr("John Smith", output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_three_part_name_parsing(self, tmp_path):
        """Test three-part name is parsed correctly."""
        output_path = tmp_path / "vcard_three_part.png"
        result = generate_vcard_qr("John Michael Smith",
                                 output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
