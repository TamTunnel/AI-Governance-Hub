"""
Tests for lineage models (Dataset, ModelDatasetLink, ModelDependency).
"""
import pytest
from app.models.lineage import Dataset, ModelDatasetLink, ModelDependency, DatasetType, DependencyType


def test_dataset_model_creation():
    """Test Dataset model can be created."""
    dataset = Dataset(
        name="Training Data v1",
        description="Customer transaction data for fraud detection",
        source_system="S3",
        location="s3://data-lake/transactions/v1",
        data_sensitivity="pii",
        data_classification="confidential"
    )
    assert dataset.name == "Training Data v1"
    assert dataset.data_sensitivity == "pii"
    assert dataset.data_classification == "confidential"


def test_dataset_type_enum():
    """Test DatasetType enum values."""
    assert DatasetType.training.value == "training"
    assert DatasetType.validation.value == "validation"
    assert DatasetType.test.value == "test"
    assert DatasetType.inference.value == "inference"


def test_dependency_type_enum():
    """Test DependencyType enum values."""
    assert DependencyType.fine_tuned_from.value == "fine_tuned_from"
    assert DependencyType.ensemble_component_of.value == "ensemble_component_of"
    assert DependencyType.distilled_from.value == "distilled_from"
    assert DependencyType.derived_from.value == "derived_from"


def test_model_dataset_link_creation():
    """Test ModelDatasetLink model can be created."""
    link = ModelDatasetLink(
        model_id=1,
        dataset_id=1,
        dataset_type=DatasetType.training,
        notes="Primary training dataset"
    )
    assert link.model_id == 1
    assert link.dataset_type == DatasetType.training


def test_model_dependency_creation():
    """Test ModelDependency model can be created."""
    dependency = ModelDependency(
        parent_model_id=1,
        child_model_id=2,
        dependency_type=DependencyType.fine_tuned_from,
        notes="Fine-tuned from base model"
    )
    assert dependency.parent_model_id == 1
    assert dependency.child_model_id == 2
    assert dependency.dependency_type == DependencyType.fine_tuned_from
