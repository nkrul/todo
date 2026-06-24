"""Example usage of the todo_core library."""

from todo_core import TodoItem, TodoList, NaturalLanguageParser, StorageManager
from datetime import date, timedelta


def example_basic_usage():
    """Example: Basic usage of TodoItem and TodoList."""
    print("=" * 50)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 50)

    # Create a todo item
    item = TodoItem(
        title="Buy groceries",
        category="Shopping",
        priority="medium",
        due_date=date.today(),
    )
    print(f"Created item: {item.title}")
    print(f"  Category: {item.category}")
    print(f"  Priority: {item.priority}")
    print(f"  Due: {item.due_date}")

    # Create a todo list and add items
    todo_list = TodoList(name="My Shopping List")
    todo_list.add_item(item)

    # Mark as complete
    item.mark_complete()
    print(f"Marked as complete: {item.completed}")

    print()


def example_natural_language_parsing():
    """Example: Parse natural language input."""
    print("=" * 50)
    print("EXAMPLE 2: Natural Language Parsing")
    print("=" * 50)

    parser = NaturalLanguageParser()

    examples = [
        "Call mom today",
        "Buy milk tomorrow",
        "Urgent meeting next friday",
        "Important shopping list",
        "Work report due in 3 days",
        "Finance review next week",
    ]

    for text in examples:
        item = parser.parse(text)
        if item:
            print(f"\nInput: '{text}'")
            print(f"  Title: {item.title}")
            print(f"  Category: {item.category}")
            print(f"  Priority: {item.priority}")
            print(f"  Due Date: {item.due_date}")

    print()


def example_multiple_tasks():
    """Example: Parse multiple tasks from text."""
    print("=" * 50)
    print("EXAMPLE 3: Parsing Multiple Tasks")
    print("=" * 50)

    parser = NaturalLanguageParser()

    text = """
    Buy groceries tomorrow
    Call dentist today
    Finish project by friday
    Important: Review report
    """

    items = parser.parse_multiple(text)
    print(f"Parsed {len(items)} tasks:\n")

    for i, item in enumerate(items, 1):
        print(f"{i}. {item.title}")
        print(f"   Category: {item.category}, Priority: {item.priority}")
        if item.due_date:
            print(f"   Due: {item.due_date}")
        print()


def example_querying_tasks():
    """Example: Query tasks in various ways."""
    print("=" * 50)
    print("EXAMPLE 4: Querying Tasks")
    print("=" * 50)

    # Create some sample tasks
    todo_list = TodoList()

    items_data = [
        ("Buy milk", "Shopping", date.today()),
        ("Call mom", "Personal", date.today()),
        ("Finish report", "Work", date.today() + timedelta(days=1)),
        ("Dentist appointment", "Health", date.today() - timedelta(days=1)),
        ("Plan vacation", "Personal", date.today() + timedelta(days=7)),
    ]

    for title, category, due_date in items_data:
        item = TodoItem(title=title, category=category, due_date=due_date)
        todo_list.add_item(item)

    # Mark one as complete
    todo_list.items[0].mark_complete()

    # Query tasks
    print(f"Total tasks: {len(todo_list.items)}")
    print(f"Pending: {len(todo_list.get_pending_items())}")
    print(f"Today's tasks: {len(todo_list.get_today_items())}")
    print(f"Overdue: {len(todo_list.get_overdue_items())}")

    print("\nTasks by category:")
    for category in ["Shopping", "Personal", "Work", "Health"]:
        tasks = todo_list.get_items_by_category(category)
        if tasks:
            print(f"  {category}: {len(tasks)} task(s)")

    print("\nToday's tasks:")
    for item in todo_list.get_today_items():
        status = "✓" if item.completed else "☐"
        print(f"  {status} {item.title}")

    print("\nOverdue tasks:")
    for item in todo_list.get_overdue_items():
        print(f"  ⚠ {item.title} (due {item.due_date})")

    print()


def example_storage():
    """Example: Save and load tasks."""
    print("=" * 50)
    print("EXAMPLE 5: Storage and Persistence")
    print("=" * 50)

    # Create and save
    storage = StorageManager()
    todo_list = TodoList(name="My Tasks")

    items_text = [
        "Buy groceries tomorrow",
        "Call mom today",
        "Finish project next friday",
    ]

    parser = NaturalLanguageParser()
    for text in items_text:
        item = parser.parse(text)
        if item:
            todo_list.add_item(item)

    # Save to storage
    storage.save(todo_list, "demo_tasks")
    print(f"Saved {len(todo_list.items)} tasks to storage")

    # Load from storage
    loaded_list = storage.load("demo_tasks")
    print(f"Loaded {len(loaded_list.items)} tasks from storage")

    print("\nLoaded tasks:")
    for item in loaded_list.items:
        print(f"  - {item.title} ({item.category})")

    print()


def example_serialization():
    """Example: Serialize tasks to JSON format."""
    print("=" * 50)
    print("EXAMPLE 6: JSON Serialization")
    print("=" * 50)

    item = TodoItem(
        title="Buy groceries",
        category="Shopping",
        priority="high",
        due_date=date.today(),
        description="Get milk, eggs, and bread",
    )

    # Convert to dict
    item_dict = item.to_dict()
    print("Item as dictionary:")
    import json

    print(json.dumps(item_dict, indent=2))

    print("\n✓ Can be easily stored, transmitted, or displayed")

    print()


if __name__ == "__main__":
    example_basic_usage()
    example_natural_language_parsing()
    example_multiple_tasks()
    example_querying_tasks()
    example_storage()
    example_serialization()

    print("=" * 50)
    print("Examples completed!")
    print("=" * 50)
