"""Tests for todo_core models."""

from datetime import date, timedelta

from todo_core.models import TodoItem, TodoList


class TestTodoItem:
    """Test cases for TodoItem."""

    def test_create_todo_item(self):
        """Test creating a todo item."""
        item = TodoItem(title="Test task", category="Work", priority="high")
        assert item.title == "Test task"
        assert item.category == "Work"
        assert item.priority == "high"
        assert not item.completed

    def test_mark_complete(self):
        """Test marking a todo item as complete."""
        item = TodoItem(title="Test task")
        assert not item.completed
        item.mark_complete()
        assert item.completed

    def test_mark_incomplete(self):
        """Test marking a todo item as incomplete."""
        item = TodoItem(title="Test task", completed=True)
        assert item.completed
        item.mark_incomplete()
        assert not item.completed

    def test_update_item(self):
        """Test updating a todo item."""
        item = TodoItem(title="Old title", priority="low")
        item.update(title="New title", priority="high")
        assert item.title == "New title"
        assert item.priority == "high"

    def test_to_dict(self):
        """Test converting todo item to dict."""
        item = TodoItem(title="Test", category="Work", due_date=date.today(), priority="high")
        data = item.to_dict()
        assert data["title"] == "Test"
        assert data["category"] == "Work"
        assert data["priority"] == "high"
        assert isinstance(data["due_date"], str)

    def test_from_dict(self):
        """Test creating todo item from dict."""
        data = {
            "title": "Test",
            "category": "Work",
            "due_date": date.today().isoformat(),
            "priority": "high",
        }
        item = TodoItem.from_dict(data)
        assert item.title == "Test"
        assert item.category == "Work"
        assert item.due_date == date.today()
        assert item.priority == "high"


class TestTodoList:
    """Test cases for TodoList."""

    def test_create_todo_list(self):
        """Test creating a todo list."""
        todo_list = TodoList()
        assert len(todo_list.items) == 0

    def test_add_item(self):
        """Test adding an item to the list."""
        todo_list = TodoList()
        item = TodoItem(title="Test")
        todo_list.add_item(item)
        assert len(todo_list.items) == 1

    def test_remove_item(self):
        """Test removing an item from the list."""
        todo_list = TodoList()
        item = TodoItem(title="Test")
        todo_list.add_item(item)
        assert len(todo_list.items) == 1

        removed = todo_list.remove_item(item.id)
        assert removed
        assert len(todo_list.items) == 0

    def test_get_item(self):
        """Test getting an item by ID."""
        todo_list = TodoList()
        item = TodoItem(title="Test")
        todo_list.add_item(item)

        retrieved = todo_list.get_item(item.id)
        assert retrieved is not None
        assert retrieved.title == "Test"

    def test_get_items_by_date(self):
        """Test getting items by date."""
        todo_list = TodoList()
        today = date.today()
        tomorrow = today + timedelta(days=1)

        item1 = TodoItem(title="Today task", due_date=today)
        item2 = TodoItem(title="Tomorrow task", due_date=tomorrow)

        todo_list.add_item(item1)
        todo_list.add_item(item2)

        today_items = todo_list.get_items_by_date(today)
        assert len(today_items) == 1
        assert today_items[0].title == "Today task"

    def test_get_items_by_category(self):
        """Test getting items by category."""
        todo_list = TodoList()
        item1 = TodoItem(title="Work task", category="Work")
        item2 = TodoItem(title="Personal task", category="Personal")

        todo_list.add_item(item1)
        todo_list.add_item(item2)

        work_items = todo_list.get_items_by_category("Work")
        assert len(work_items) == 1
        assert work_items[0].title == "Work task"

    def test_get_pending_items(self):
        """Test getting pending items."""
        todo_list = TodoList()
        item1 = TodoItem(title="Pending")
        item2 = TodoItem(title="Completed", completed=True)

        todo_list.add_item(item1)
        todo_list.add_item(item2)

        pending = todo_list.get_pending_items()
        assert len(pending) == 1
        assert pending[0].title == "Pending"

    def test_get_overdue_items(self):
        """Test getting overdue items."""
        todo_list = TodoList()
        yesterday = date.today() - timedelta(days=1)
        tomorrow = date.today() + timedelta(days=1)

        item1 = TodoItem(title="Overdue", due_date=yesterday)
        item2 = TodoItem(title="Future", due_date=tomorrow)

        todo_list.add_item(item1)
        todo_list.add_item(item2)

        overdue = todo_list.get_overdue_items()
        assert len(overdue) == 1
        assert overdue[0].title == "Overdue"

    def test_get_today_items(self):
        """Test getting today's items."""
        todo_list = TodoList()
        today = date.today()

        item1 = TodoItem(title="Today", due_date=today)
        item2 = TodoItem(title="Tomorrow", due_date=today + timedelta(days=1))

        todo_list.add_item(item1)
        todo_list.add_item(item2)

        today_items = todo_list.get_today_items()
        assert len(today_items) == 1
        assert today_items[0].title == "Today"

    def test_to_dict(self):
        """Test converting todo list to dict."""
        todo_list = TodoList(name="My Tasks")
        item = TodoItem(title="Test")
        todo_list.add_item(item)

        data = todo_list.to_dict()
        assert data["name"] == "My Tasks"
        assert len(data["items"]) == 1

    def test_from_dict(self):
        """Test creating todo list from dict."""
        data = {
            "name": "My Tasks",
            "items": [
                {
                    "title": "Test",
                    "category": "Work",
                    "due_date": None,
                    "description": "",
                    "priority": "medium",
                    "completed": False,
                    "id": "test-id",
                    "created_at": date.today().isoformat() + "T00:00:00",
                    "updated_at": date.today().isoformat() + "T00:00:00",
                }
            ],
        }
        todo_list = TodoList.from_dict(data)
        assert todo_list.name == "My Tasks"
        assert len(todo_list.items) == 1
