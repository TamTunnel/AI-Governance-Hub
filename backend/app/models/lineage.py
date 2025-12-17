"""
Lineage models for dataset and model dependency tracking.
Supports traceability for audits and governance requirements.
"""
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column


class DatasetType(str, Enum):
    """Type of dataset"""
    training = "training"
    validation = "validation"
    test = "test"
    inference = "inference"


class DependencyType(str, Enum):
    """Type of model-to-model dependency"""
    fine_tuned_from = "fine_tuned_from"
    ensemble_component_of = "ensemble_component_of"
    distilled_from = "distilled_from"
    derived_from = "derived_from"


class Dataset(SQLModel, table=True):
    """
    Dataset entity for lineage tracking.
    Represents a data source used by models.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    source_system: Optional[str] = None  # e.g., "S3", "Snowflake", "BigQuery"
    location: Optional[str] = None  # URI or path
    
    # Data governance fields
    data_sensitivity: str = Field(default="internal")  # public, internal, pii, phi, pci
    data_classification: str = Field(default="internal")  # public, internal, confidential, restricted
    
    # Multi-tenancy
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    
    # Metadata
    record_count: Optional[int] = None
    schema_info: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class ModelDatasetLink(SQLModel, table=True):
    """
    Many-to-many link between models/versions and datasets.
    Enables dataset lineage tracking.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    model_id: int = Field(foreign_key="modelregistry.id")
    model_version_id: Optional[int] = Field(default=None, foreign_key="modelversion.id")
    dataset_id: int = Field(foreign_key="dataset.id")
    dataset_type: DatasetType = Field(default=DatasetType.training)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ModelDependency(SQLModel, table=True):
    """
    Model-to-model dependency tracking.
    Captures lineage like fine-tuning, ensembles, distillation.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_model_id: int = Field(foreign_key="modelregistry.id")
    parent_version_id: Optional[int] = Field(default=None, foreign_key="modelversion.id")
    child_model_id: int = Field(foreign_key="modelregistry.id")
    child_version_id: Optional[int] = Field(default=None, foreign_key="modelversion.id")
    dependency_type: DependencyType = Field(default=DependencyType.derived_from)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
