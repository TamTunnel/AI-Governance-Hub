"""
Tests for data classification and sensitivity enums.
"""
import pytest
from app.models.all_models import DataSensitivity, DataClassification


def test_data_sensitivity_enum():
    """Test DataSensitivity enum values match US governance standards."""
    assert DataSensitivity.public.value == "public"
    assert DataSensitivity.internal.value == "internal"
    assert DataSensitivity.pii.value == "pii"  # Personally Identifiable Information
    assert DataSensitivity.phi.value == "phi"  # Protected Health Information (HIPAA)
    assert DataSensitivity.pci.value == "pci"  # Payment Card Industry data


def test_data_classification_enum():
    """Test DataClassification enum values match enterprise standards."""
    assert DataClassification.public.value == "public"
    assert DataClassification.internal.value == "internal"
    assert DataClassification.confidential.value == "confidential"
    assert DataClassification.restricted.value == "restricted"


def test_data_sensitivity_pii_phi_distinction():
    """Test that PII and PHI are distinct classifications."""
    assert DataSensitivity.pii != DataSensitivity.phi
    # PHI is specifically for HIPAA-protected health information
    # PII is general personally identifiable information
