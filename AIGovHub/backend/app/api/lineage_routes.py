"""
Lineage API routes.
CRUD for datasets and model dependencies/lineage tracking.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from ..core.database import get_session
from ..models import (
    Dataset, ModelDatasetLink, ModelDependency,
    DatasetType, DependencyType, ModelRegistry
)


router = APIRouter(tags=["Lineage"])


# --- Schemas ---
class DatasetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source_system: Optional[str] = None
    location: Optional[str] = None
    data_sensitivity: str = "internal"
    data_classification: str = "internal"
    organization_id: Optional[int] = None
    record_count: Optional[int] = None


class DatasetRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    source_system: Optional[str]
    location: Optional[str]
    data_sensitivity: str
    data_classification: str
    organization_id: Optional[int]
    record_count: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class DatasetLinkCreate(BaseModel):
    dataset_id: int
    dataset_type: DatasetType = DatasetType.training
    model_version_id: Optional[int] = None
    notes: Optional[str] = None


class DatasetLinkRead(BaseModel):
    id: int
    model_id: int
    model_version_id: Optional[int]
    dataset_id: int
    dataset_type: DatasetType
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DependencyCreate(BaseModel):
    parent_model_id: int
    parent_version_id: Optional[int] = None
    dependency_type: DependencyType = DependencyType.derived_from
    notes: Optional[str] = None


class DependencyRead(BaseModel):
    id: int
    parent_model_id: int
    parent_version_id: Optional[int]
    child_model_id: int
    child_version_id: Optional[int]
    dependency_type: DependencyType
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LineageResponse(BaseModel):
    datasets: List[DatasetLinkRead]
    parent_models: List[DependencyRead]
    child_models: List[DependencyRead]


# --- Dataset CRUD ---
@router.post("/datasets/", response_model=DatasetRead)
def create_dataset(payload: DatasetCreate, session: Session = Depends(get_session)):
    """Create a new dataset for lineage tracking"""
    dataset = Dataset(**payload.model_dump())
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    return dataset


@router.get("/datasets/", response_model=List[DatasetRead])
def list_datasets(
    session: Session = Depends(get_session),
    organization_id: Optional[int] = Query(None),
    data_sensitivity: Optional[str] = Query(None)
):
    """List all datasets with optional filters"""
    query = select(Dataset)
    if organization_id:
        query = query.where(Dataset.organization_id == organization_id)
    if data_sensitivity:
        query = query.where(Dataset.data_sensitivity == data_sensitivity)
    return session.exec(query.order_by(Dataset.created_at.desc())).all()


@router.get("/datasets/{dataset_id}", response_model=DatasetRead)
def get_dataset(dataset_id: int, session: Session = Depends(get_session)):
    """Get a specific dataset"""
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


# --- Model-Dataset Links ---
@router.post("/models/{model_id}/datasets/", response_model=DatasetLinkRead)
def link_dataset_to_model(
    model_id: int,
    payload: DatasetLinkCreate,
    session: Session = Depends(get_session)
):
    """Link a dataset to a model"""
    model = session.get(ModelRegistry, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    dataset = session.get(Dataset, payload.dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    link = ModelDatasetLink(
        model_id=model_id,
        dataset_id=payload.dataset_id,
        dataset_type=payload.dataset_type,
        model_version_id=payload.model_version_id,
        notes=payload.notes
    )
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@router.get("/models/{model_id}/datasets/", response_model=List[DatasetLinkRead])
def get_model_datasets(model_id: int, session: Session = Depends(get_session)):
    """Get all datasets linked to a model"""
    return session.exec(
        select(ModelDatasetLink).where(ModelDatasetLink.model_id == model_id)
    ).all()


# --- Model Dependencies ---
@router.post("/models/{model_id}/dependencies/", response_model=DependencyRead)
def create_dependency(
    model_id: int,
    payload: DependencyCreate,
    session: Session = Depends(get_session)
):
    """Declare a model dependency (this model depends on parent_model)"""
    model = session.get(ModelRegistry, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    parent = session.get(ModelRegistry, payload.parent_model_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent model not found")
    
    dependency = ModelDependency(
        parent_model_id=payload.parent_model_id,
        parent_version_id=payload.parent_version_id,
        child_model_id=model_id,
        dependency_type=payload.dependency_type,
        notes=payload.notes
    )
    session.add(dependency)
    session.commit()
    session.refresh(dependency)
    return dependency


# --- Full Lineage ---
@router.get("/models/{model_id}/lineage", response_model=LineageResponse)
def get_model_lineage(model_id: int, session: Session = Depends(get_session)):
    """Get full lineage for a model (datasets + parent/child models)"""
    model = session.get(ModelRegistry, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Get linked datasets
    datasets = session.exec(
        select(ModelDatasetLink).where(ModelDatasetLink.model_id == model_id)
    ).all()
    
    # Get parent models (this model depends on)
    parents = session.exec(
        select(ModelDependency).where(ModelDependency.child_model_id == model_id)
    ).all()
    
    # Get child models (depend on this model)
    children = session.exec(
        select(ModelDependency).where(ModelDependency.parent_model_id == model_id)
    ).all()
    
    return LineageResponse(
        datasets=list(datasets),
        parent_models=list(parents),
        child_models=list(children)
    )
