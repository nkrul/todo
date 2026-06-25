"""Tests for todo_cli package."""

import tempfile
from pathlib import Path

from todo_cli import TodoCLI, main
from todo_core.models import TodoItem


class TestTodoCLI:
    def test_add_parses_and_stores(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = TodoCLI(storage_path=tmpdir)
            added = cli.add("Buy milk tomorrow")

            assert len(added) == 1
            assert added[0].title.lower().startswith("buy milk")
            assert added[0].due_date is not None
            assert len(cli.todo_list.items) == 1
            assert Path(tmpdir).joinpath("default.json").exists()

    def test_list_filters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = TodoCLI(storage_path=tmpdir)
            cli.todo_list.add_item(TodoItem(title="Pending task"))
            completed = TodoItem(title="Done task", completed=True)
            cli.todo_list.add_item(completed)
            cli.save()

            pending_items = cli.list(filter_by="pending", show_completed=False)
            assert len(pending_items) == 1
            assert pending_items[0].title == "Pending task"

            all_items = cli.list(filter_by="all", show_completed=True)
            assert len(all_items) == 2

    def test_complete_updates_item(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = TodoCLI(storage_path=tmpdir)
            item = TodoItem(title="Finish report")
            cli.todo_list.add_item(item)
            cli.save()

            updated = cli.complete([item.id])
            assert len(updated) == 1
            assert updated[0].completed

    def test_remove_item(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = TodoCLI(storage_path=tmpdir)
            item = TodoItem(title="Trash this")
            cli.todo_list.add_item(item)
            cli.save()

            removed = cli.remove([item.id])
            assert removed == [item.id]
            assert len(cli.todo_list.items) == 0

    def test_clear_deletes_storage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = TodoCLI(storage_path=tmpdir)
            cli.todo_list.add_item(TodoItem(title="Temp"))
            cli.save()

            assert Path(tmpdir).joinpath("default.json").exists()
            cleared = cli.clear()
            assert cleared
            assert len(cli.todo_list.items) == 0
            assert not Path(tmpdir).joinpath("default.json").exists()

    def test_stats_returns_counts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = TodoCLI(storage_path=tmpdir)
            cli.todo_list.add_item(TodoItem(title="Pending"))
            cli.todo_list.add_item(TodoItem(title="Done", completed=True))
            cli.save()

            stats = cli.stats()
            assert stats["total"] == 2
            assert stats["pending"] == 1
            assert stats["completed"] == 1

    def test_help_command_shows_usage(self, capsys):
        exit_code = main(["help"])
        captured = capsys.readouterr()

        assert exit_code == 0
        assert "usage:" in captured.out.lower()

    def test_help_command_shows_subcommand_help(self, capsys):
        exit_code = main(["help", "add"])
        captured = capsys.readouterr()

        assert exit_code == 0
        assert "add" in captured.out.lower()
        assert "task text to parse and add" in captured.out.lower()
