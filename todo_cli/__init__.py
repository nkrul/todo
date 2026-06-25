"""Command-line interface for the todo app."""

from __future__ import annotations

import argparse
from datetime import date
from typing import Iterable, List, Optional

from todo_core import NaturalLanguageParser, StorageManager, TodoList
from todo_core.models import TodoItem

__all__ = ["TodoCLI", "main"]


class TodoCLI:
    """Command-line interface implementation for todo management."""

    def __init__(self, storage_path: Optional[str] = None) -> None:
        self.storage = StorageManager(storage_path)
        self.todo_list = self.storage.load("default")

    def save(self) -> None:
        """Persist the current todo list."""
        self.storage.save(self.todo_list, "default")

    def add(self, text: str) -> List[TodoItem]:
        """Parse natural language text and add resulting todo items."""
        items = NaturalLanguageParser.parse_multiple(text)
        if not items:
            raise ValueError("Could not parse any todo items from input")

        for item in items:
            self.todo_list.add_item(item)
        self.save()
        return items

    def list(
        self,
        filter_by: str = "pending",
        show_completed: bool = False,
    ) -> List[TodoItem]:
        """List items in the todo list with optional filters."""
        if filter_by == "all":
            items = self.todo_list.items
        elif filter_by == "today":
            items = self.todo_list.get_today_items()
        elif filter_by == "overdue":
            items = self.todo_list.get_overdue_items()
        else:
            items = self.todo_list.get_pending_items()

        if not show_completed:
            items = [item for item in items if not item.completed]

        return sorted(
            items,
            key=lambda item: (item.completed, item.due_date or date.today()),
        )

    def complete(self, item_ids: Iterable[str]) -> List[TodoItem]:
        """Mark items complete by ID."""
        updated = []
        for item_id in item_ids:
            item = self.todo_list.get_item(item_id)
            if item and not item.completed:
                item.mark_complete()
                updated.append(item)
        self.save()
        return updated

    def remove(self, item_ids: Iterable[str]) -> List[str]:
        """Remove items by ID."""
        removed_ids = []
        for item_id in item_ids:
            if self.todo_list.remove_item(item_id):
                removed_ids.append(item_id)
        self.save()
        return removed_ids

    def clear(self) -> bool:
        """Delete the default todo list from storage."""
        cleared = self.storage.delete("default")
        self.todo_list = TodoList(name="default")
        return cleared

    def stats(self) -> dict[str, int]:
        """Return high-level statistics for the current todo list."""
        return {
            "total": len(self.todo_list.items),
            "pending": len(self.todo_list.get_pending_items()),
            "completed": sum(1 for item in self.todo_list.items if item.completed),
            "overdue": len(self.todo_list.get_overdue_items()),
        }

    @staticmethod
    def format_item(item: TodoItem) -> str:
        """Format a TodoItem for console output."""
        due = item.due_date.isoformat() if item.due_date else "No due date"
        status = "✓" if item.completed else " "
        return (
            f"[{status}] {item.id} | {item.title} | {item.category} | " f"{item.priority} | {due}"
        )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo_cli",
        description="Todo command-line interface using todo_core for storage and parsing.",
    )
    parser.add_argument(
        "--storage-path",
        help="Directory used for storing todo data.",
        default=None,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new todo item using natural language.")
    add_parser.add_argument("text", nargs="+", help="Task text to parse and add.")

    list_parser = subparsers.add_parser("list", help="List todo items.")
    list_parser.add_argument(
        "--filter",
        choices=["all", "pending", "today", "overdue"],
        default="pending",
        help="Filter tasks by status or due date.",
    )
    list_parser.add_argument(
        "--show-completed",
        action="store_true",
        help="Include completed tasks in the output.",
    )

    complete_parser = subparsers.add_parser(
        "complete",
        help="Mark todo items complete by ID.",
    )
    complete_parser.add_argument("item_ids", nargs="+", help="IDs of items to complete.")

    remove_parser = subparsers.add_parser("remove", help="Remove todo items by ID.")
    remove_parser.add_argument("item_ids", nargs="+", help="IDs of items to remove.")

    subparsers.add_parser("clear", help="Delete the default todo list.")
    subparsers.add_parser("stats", help="Print todo list statistics.")
    help_parser = subparsers.add_parser("help", help="Show help for todo_cli commands.")
    help_parser.add_argument(
        "topic",
        nargs="?",
        help="Command to show help for.",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    cli = TodoCLI(storage_path=args.storage_path)

    if args.command == "add":
        added = cli.add(" ".join(args.text))
        for item in added:
            print(f"Added: {cli.format_item(item)}")
        return 0

    if args.command == "list":
        items = cli.list(filter_by=args.filter, show_completed=args.show_completed)
        if not items:
            print("No tasks found.")
            return 0
        for item in items:
            print(cli.format_item(item))
        return 0

    if args.command == "complete":
        updated = cli.complete(args.item_ids)
        if not updated:
            print("No matching incomplete tasks were found.")
            return 1
        for item in updated:
            print(f"Completed: {cli.format_item(item)}")
        return 0

    if args.command == "remove":
        removed_ids = cli.remove(args.item_ids)
        if not removed_ids:
            print("No matching tasks were removed.")
            return 1
        for item_id in removed_ids:
            print(f"Removed: {item_id}")
        return 0

    if args.command == "clear":
        cleared = cli.clear()
        print("Cleared todo list." if cleared else "No todo list found to clear.")
        return 0

    if args.command == "help":
        if args.topic:
            subparsers = parser._subparsers._group_actions[0].choices
            if args.topic in subparsers:
                subparsers[args.topic].print_help()
            else:
                print(f"No help available for '{args.topic}'.\n")
                parser.print_help()
        else:
            parser.print_help()
        return 0

    if args.command == "stats":
        stats = cli.stats()
        print(
            f"Total: {stats['total']} | Pending: {stats['pending']} | "
            f"Completed: {stats['completed']} | Overdue: {stats['overdue']}"
        )
        return 0

    parser.print_help()
    return 1
