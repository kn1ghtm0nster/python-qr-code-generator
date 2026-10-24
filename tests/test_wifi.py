"""Tests for WiFi QR code generator."""

import pytest
from pathlib import Path
from qr_generator.generators.wifi import generate_wifi_qr


class TestWiFiQRValid:
    """Test valid inputs for WiFi QR code generation."""
    
    def test_generate_wpa_with_password(self, tmp_path):
        """Test generating WiFi QR code with WPA security."""
        output_path = tmp_path / "wifi_wpa.png"
        result = generate_wifi_qr("MyNetwork", "Password123", security="WPA",
                                output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith(".png")
    
    def test_generate_wep_with_password(self, tmp_path):
        """Test generating WiFi QR code with WEP security."""
        output_path = tmp_path / "wifi_wep.png"
        result = generate_wifi_qr("MyNetwork", "Password123", security="WEP",
                                output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_open_network(self, tmp_path):
        """Test generating WiFi QR code for open network."""
        output_path = tmp_path / "wifi_open.png"
        result = generate_wifi_qr("PublicNetwork", "", security="NOPASS",
                                output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_hidden_network(self, tmp_path):
        """Test generating WiFi QR code for hidden network."""
        output_path = tmp_path / "wifi_hidden.png"
        result = generate_wifi_qr("HiddenNetwork", "SecurePass", security="WPA",
                                hidden=True, output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_default_output_path(self, tmp_path, monkeypatch):
        """Test generating WiFi QR code with default output path."""
        monkeypatch.chdir(tmp_path)
        result = generate_wifi_qr("Network", "Password", security="WPA")
        
        assert result is not None
        assert isinstance(result, str)
        assert result.endswith(".png")
    
    def test_different_error_correction_levels(self, tmp_path):
        """Test generating WiFi QR codes with different error correction levels."""
        levels = ["L", "M", "Q", "H"]
        for level in levels:
            output_path = tmp_path / f"wifi_error_{level}.png"
            result = generate_wifi_qr("Network", "Pass", security="WPA",
                                    output_path=str(output_path),
                                    error_correction=level)
            assert result is not None
            assert isinstance(result, str)
    
    def test_different_sizes(self, tmp_path):
        """Test generating WiFi QR codes with different box sizes."""
        for size in [5, 10, 20]:
            output_path = tmp_path / f"wifi_size_{size}.png"
            result = generate_wifi_qr("Network", "Pass", security="WPA",
                                    output_path=str(output_path), size=size)
            assert result is not None
            assert isinstance(result, str)
    
    def test_unicode_ssid(self, tmp_path):
        """Test WiFi QR code with Unicode SSID."""
        output_path = tmp_path / "wifi_unicode.png"
        result = generate_wifi_qr("网络🌐", "Password", security="WPA",
                                output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_special_characters_in_ssid(self, tmp_path):
        """Test WiFi QR code with special characters in SSID."""
        output_path = tmp_path / "wifi_special.png"
        result = generate_wifi_qr("Net-Work_2.4GHz!", "Pass@123", security="WPA",
                                output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_long_password(self, tmp_path):
        """Test WiFi QR code with long password."""
        output_path = tmp_path / "wifi_long_pass.png"
        long_password = "A" * 63  # Max WPA2 password length
        result = generate_wifi_qr("Network", long_password, security="WPA",
                                output_path=str(output_path))
        
        assert result is not None
        assert isinstance(result, str)


class TestWiFiQRInvalid:
    """Test invalid inputs for WiFi QR code generation."""
    
    def test_empty_ssid(self):
        """Test that empty SSID raises ValueError."""
        with pytest.raises(ValueError, match="SSID cannot be empty"):
            generate_wifi_qr("", "Password", security="WPA")
    
    def test_whitespace_ssid(self):
        """Test that whitespace-only SSID raises ValueError."""
        with pytest.raises(ValueError, match="SSID cannot be empty"):
            generate_wifi_qr("   ", "Password", security="WPA")
    
    def test_invalid_security_type(self):
        """Test that invalid security type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid security type"):
            generate_wifi_qr("Network", "Password", security="INVALID")
    
    def test_wpa_without_password(self):
        """Test that WPA security without password raises ValueError."""
        with pytest.raises(ValueError, match="Password required"):
            generate_wifi_qr("Network", "", security="WPA")
    
    def test_wpa_with_empty_password(self):
        """Test that WPA security with empty password raises ValueError."""
        with pytest.raises(ValueError, match="Password required"):
            generate_wifi_qr("Network", "   ", security="WPA")
    
    def test_wep_without_password(self):
        """Test that WEP security without password raises ValueError."""
        with pytest.raises(ValueError, match="Password required"):
            generate_wifi_qr("Network", "", security="WEP")
    
    def test_none_ssid(self):
        """Test that None SSID raises ValueError."""
        with pytest.raises(ValueError, match="SSID cannot be empty"):
            generate_wifi_qr(None, "Password", security="WPA")


class TestWiFiQRMissing:
    """Test edge cases for WiFi QR code generation."""
    
    def test_nopass_with_empty_password(self, tmp_path):
        """Test NOPASS security with empty password."""
        output_path = tmp_path / "nopass_empty.png"
        result = generate_wifi_qr("OpenNet", "", security="NOPASS",
                                output_path=str(output_path))
        
        assert Path(result).exists()
    
    def test_security_case_insensitive(self, tmp_path):
        """Test that security types are case-insensitive."""
        output_path = tmp_path / "security_case.png"
        result = generate_wifi_qr("Network", "Pass", security="wpa",
                                output_path=str(output_path))
        
        assert Path(result).exists()
    
    def test_ssid_whitespace_trimmed(self, tmp_path):
        """Test that SSID whitespace is trimmed."""
        output_path = tmp_path / "ssid_trimmed.png"
        result = generate_wifi_qr("  MyNetwork  ", "Password",
                                output_path=str(output_path))
        
        assert Path(result).exists()
