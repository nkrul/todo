"""Storage management for todo items."""

import json
import os
from pathlib import Path
from typing import Optional
from .models import TodoList, TodoItem


class StorageManager:
    """Manages persistence of todo items to JSON storage."""

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the storage manager.

        Args:
            storage_path: Path to store JSON files. Defaults to ~/.todo_data
        """
        if storage_path is None:
            storage_path = os.path.expanduser("~/.todo_data")
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, list_name: str = "default") -> Path:
        """Get the file path for a todo list."""
        return self.storage_path / f"{list_name}.json"

    def save(self, todo_list: TodoList, list_name: str = "default") -> None:
        """Save a todo list to disk."""
        file_path = self._get_file_path(list_name)
        with open(file_path, "w") as f:
            json.dump(todo_list.to_dict(), f, indent=2)

    def load(self, list_name: str = "default") -> TodoList:
        """Load a todo list from disk. Returns empty list if file doesn't exist."""
        file_path = self._get_file_path(list_name)
        if file_path.exists():
            with open(file_path, "r") as f:
                data = json.load(f)
                return TodoList.from_dict(data)
        return TodoList(name=list_name)

    def delete(self, list_name: str = "default") -> bool:
        """Delete a todo list file. Returns True if successful."""
        file_path = self._get_file_path(list_name)
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def list_all(self) -> list[str]:
        """List all available todo lists."""
        if not self.storage_path.exists():
            return []
        return [
            f.stem for f in self.storage_path.glob("*.json") if f.is_file()
        ]
