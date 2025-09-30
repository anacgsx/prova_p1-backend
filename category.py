import uuid
from dataclasses import dataclass, field
from typing import Optional, List

from events.category_events import (
    CategoryCreated,
    CategoryUpdated,
    CategoryActivated,
    CategoryDeactivated,
)

MAX_NAME = 255

@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: Optional[str] = field(default=None)
    events: List[object] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
            self._add_event(CategoryCreated(
                category_id=self.id,
                name=self.name,
                description=self.description,
                is_active=self.is_active
            ))
        self.name = self._validate_name(self.name)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not name or not name.strip():
            raise ValueError("Nome é obrigatório")
        if len(name.strip()) > MAX_NAME:
            raise ValueError(f"Nome deve ter até {MAX_NAME} caracteres")
        return name.strip()

    def update(self, *, name: Optional[str] = None, description: Optional[str] = None):
        old_name, old_desc = self.name, self.description
        changed = False
        if name and name != self.name:
            self.name = self._validate_name(name)
            changed = True
        if description is not None and description != self.description:
            self.description = description.strip()
            changed = True
        if changed:
            self._add_event(CategoryUpdated(
                category_id=self.id,
                old_name=old_name,
                new_name=self.name,
                old_description=old_desc,
                new_description=self.description
            ))

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self._add_event(CategoryActivated(self.id))

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self._add_event(CategoryDeactivated(self.id))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "class_name": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description", ""),
            is_active=data.get("is_active", True),
        )

    def _add_event(self, event: object):
        self.events.append(event)

    def pull_events(self) -> List[object]:
        evs = self.events[:]
        self.events.clear()
        return evs
