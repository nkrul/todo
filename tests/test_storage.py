"""Tests for storage manager."""

import pytest
import tempfile
import json
from pathlib import Path
from todo_core.storage import StorageManager
from todo_core.models import TodoItem, TodoList


class TestStorageManager:
    """Test cases for StorageManager."""

    @pytest.fixture
    def temp_storage_path(self):
        """Create a temporary directory for storage tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_create_storage_manager(self, temp_storage_path):
        """Test creating a storage manager."""
        storage = StorageManager(temp_storage_path)
        assert storage.storage_path == Path(temp_storage_path)
        assert storage.storage_path.exists()

    def test_save_and_load(self, temp_storage_path):
        """Test saving and loading a todo list."""
        storage = StorageManager(temp_storage_path)

        # Create and save
        todo_list = TodoList()
        item = TodoItem(title="Test task", category="Work")
        todo_list.add_item(item)
        storage.save(todo_list, "test_list")

        # Load and verify
        loaded = storage.load("test_list")
        assert len(loaded.items) == 1
        assert loaded.items[0].title == "Test task"

    def test_load_nonexistent(self, temp_storage_path):
        """Test loading a nonexistent list returns empty list."""
        storage = StorageManager(temp_storage_path)
        loaded = storage.load("nonexistent")
        assert len(loaded.items) == 0

    def test_delete_list(self, temp_storage_path):
        """Test deleting a todo list."""
        storage = StorageManager(temp_storage_path)

        # Create and save
        todo_list = TodoList()
        item = TodoItem(title="Test")
        todo_list.add_item(item)
        storage.save(todo_list, "to_delete")

        # Verify it exists
        assert storage.load("to_delete") is not None

        # Delete
        deleted = storage.delete("to_delete")
        assert deleted

        # Verify it's gone
        loaded = storage.load("to_delete")
        assert len(loaded.items) == 0

    def test_list_all(self, temp_storage_path):
        """Test listing all saved lists."""
        storage = StorageManager(temp_storage_path)

        # Save multiple lists
        for i in range(3):
            todo_list = TodoList(name=f"List {i}")
            storage.save(todo_list, f"list_{i}")

        # List all
        all_lists = storage.list_all()
        assert len(all_lists) >= 3
        assert "list_0" in all_lists
        assert "list_1" in all_lists
        assert "list_2" in all_lists

    def test_storage_persistence(self, temp_storage_path):
        """Test that storage persists across instances."""
        # First instance
        storage1 = StorageManager(temp_storage_path)
        todo_list = TodoList()
        item = TodoItem(title="Persistent task", category="Work")
        todo_list.add_item(item)
        storage1.save(todo_list, "persistent")

        # Second instance
        storage2 = StorageManager(temp_storage_path)
        loaded = storage2.load("persistent")

        assert len(loaded.items) == 1
        assert loaded.items[0].title == "Persistent task"

    def test_file_format(self, temp_storage_path):
        """Test that storage files are valid JSON."""
        storage = StorageManager(temp_storage_path)
        todo_list = TodoList(name="JSON Test")
        item = TodoItem(title="Test", category="Work", priority="high")
        todo_list.add_item(item)
        storage.save(todo_list, "json_test")

        # Read file directly
        file_path = storage._get_file_path("json_test")
        with open(file_path, "r") as f:
            data = json.load(f)

        assert data["name"] == "JSON Test"
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Test"
