from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass(frozen=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    occurred_on: datetime = field(default_factory=datetime.utcnow, init=False)

@dataclass(frozen=True)
class CategoryCreated(DomainEvent):
    category_id: str
    name: str
    description: str
    is_active: bool

@dataclass(frozen=True)
class CategoryUpdated(DomainEvent):
    category_id: str
    old_name: str
    new_name: str
    old_description: str
    new_description: str

@dataclass(frozen=True)
class CategoryActivated(DomainEvent):
    category_id: str

@dataclass(frozen=True)
class CategoryDeactivated(DomainEvent):
    category_id: str
