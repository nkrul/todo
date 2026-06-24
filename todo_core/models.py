"""Domain models for todo items and lists."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import List, Optional
import uuid


@dataclass
class TodoItem:
    """Represents a single todo item with temporal and category information."""

    title: str
    due_date: Optional[date] = None
    category: str = "Personal"
    description: str = ""
    priority: str = "medium"  # low, medium, high
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        data = asdict(self)
        if self.due_date:
            data["due_date"] = self.due_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create TodoItem from dictionary representation."""
        data = data.copy()
        if isinstance(data.get("due_date"), str):
            data["due_date"] = datetime.fromisoformat(data["due_date"]).date()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)

    def mark_complete(self) -> None:
        """Mark the item as completed."""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark the item as incomplete."""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, **kwargs) -> None:
        """Update item fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()


@dataclass
class TodoList:
    """Represents a collection of todo items."""

    items: List[TodoItem] = field(default_factory=list)
    name: str = "My Tasks"

    def add_item(self, item: TodoItem) -> None:
        """Add a todo item to the list."""
        self.items.append(item)

    def remove_item(self, item_id: str) -> bool:
        """Remove a todo item by ID. Returns True if item was found and removed."""
        original_length = len(self.items)
        self.items = [item for item in self.items if item.id != item_id]
        return len(self.items) < original_length

    def get_item(self, item_id: str) -> Optional[TodoItem]:
        """Get a todo item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_items_by_date(self, target_date: date) -> List[TodoItem]:
        """Get all items due on a specific date."""
        return [item for item in self.items if item.due_date == target_date]

    def get_items_by_category(self, category: str) -> List[TodoItem]:
        """Get all items in a specific category."""
        return [item for item in self.items if item.category == category]

    def get_pending_items(self) -> List[TodoItem]:
        """Get all incomplete items."""
        return [item for item in self.items if not item.completed]

    def get_overdue_items(self) -> List[TodoItem]:
        """Get all incomplete items with due dates in the past."""
        today = date.today()
        return [
            item
            for item in self.items
            if not item.completed and item.due_date and item.due_date < today
        ]

    def get_today_items(self) -> List[TodoItem]:
        """Get all items due today."""
        return self.get_items_by_date(date.today())

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoList":
        """Create TodoList from dictionary representation."""
        todo_list = cls(name=data.get("name", "My Tasks"))
        for item_data in data.get("items", []):
            todo_list.add_item(TodoItem.from_dict(item_data))
        return todo_list
