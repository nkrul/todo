"""Mobile app for todo using Kivy for iOS/Android."""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.garden.datepicker import DatePicker
from datetime import date
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo_core import TodoItem, TodoList, NaturalLanguageParser, StorageManager


class TodoApp(App):
    """Kivy-based mobile todo application."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.todo_list = self.storage.load("default")
        self.current_item_id = None

    def build(self):
        """Build the Kivy app."""
        Window.size = (400, 600)

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title
        title_label = Label(
            text="📝 Todo App",
            size_hint_y=0.1,
            font_size="24sp",
            bold=True,
        )
        main_layout.add_widget(title_label)

        # Input section
        input_layout = BoxLayout(orientation="horizontal", size_hint_y=0.15, spacing=5)
        self.input_field = TextInput(
            multiline=False,
            hint_text="Type task (e.g., 'Buy milk tomorrow')",
            font_size="12sp",
        )
        input_layout.add_widget(self.input_field)

        add_button = Button(text="Add", size_hint_x=0.2, font_size="12sp")
        add_button.bind(on_press=self.add_task)
        input_layout.add_widget(add_button)

        main_layout.add_widget(input_layout)

        # Stats
        self.stats_label = Label(size_hint_y=0.1, font_size="12sp")
        self.update_stats()
        main_layout.add_widget(self.stats_label)

        # Tasks list
        scroll_view = ScrollView(size_hint=(1, 0.65))
        self.tasks_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.tasks_grid.bind(minimum_height=self.tasks_grid.setter("height"))
        scroll_view.add_widget(self.tasks_grid)
        main_layout.add_widget(scroll_view)

        self.refresh_tasks()

        return main_layout

    def update_stats(self):
        """Update statistics label."""
        pending = len(self.todo_list.get_pending_items())
        total = len(self.todo_list.items)
        self.stats_label.text = f"Total: {total} | Pending: {pending}"

    def add_task(self, instance):
        """Add a new task from input."""
        text = self.input_field.text.strip()
        if text:
            items = NaturalLanguageParser.parse_multiple(text)
            for item in items:
                self.todo_list.add_item(item)
            self.storage.save(self.todo_list, "default")
            self.input_field.text = ""
            self.refresh_tasks()

    def refresh_tasks(self):
        """Refresh the task list display."""
        self.tasks_grid.clear_widgets()

        for item in sorted(
            self.todo_list.items,
            key=lambda x: (x.completed, x.due_date or date.today()),
        ):
            self.add_task_widget(item)

        self.update_stats()

    def add_task_widget(self, item: TodoItem):
        """Add a task widget to the grid."""
        task_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=5)

        # Checkbox
        check_btn = Button(text="✓" if item.completed else "☐", size_hint_x=0.1)

        def toggle_complete(btn):
            if item.completed:
                item.mark_incomplete()
            else:
                item.mark_complete()
            self.storage.save(self.todo_list, "default")
            self.refresh_tasks()

        check_btn.bind(on_press=toggle_complete)
        task_layout.add_widget(check_btn)

        # Task info
        due_date_str = f" ({item.due_date})" if item.due_date else ""
        task_text = f"{item.title}{due_date_str}"
        if item.completed:
            task_text = f"[s]{task_text}[/s]"

        info_label = Label(
            text=task_text,
            markup=True,
            size_hint_x=0.6,
            font_size="12sp",
        )
        task_layout.add_widget(info_label)

        # Edit button
        edit_btn = Button(text="✎", size_hint_x=0.15, font_size="12sp")

        def edit_task(btn):
            self.show_edit_popup(item)

        edit_btn.bind(on_press=edit_task)
        task_layout.add_widget(edit_btn)

        # Delete button
        delete_btn = Button(text="✕", size_hint_x=0.15, font_size="12sp")

        def delete_task(btn):
            self.todo_list.remove_item(item.id)
            self.storage.save(self.todo_list, "default")
            self.refresh_tasks()

        delete_btn.bind(on_press=delete_task)
        task_layout.add_widget(delete_btn)

        self.tasks_grid.add_widget(task_layout)

    def show_edit_popup(self, item: TodoItem):
        """Show edit popup for a task."""
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title input
        title_input = TextInput(text=item.title, multiline=False, size_hint_y=0.15)
        content.add_widget(title_input)

        # Category spinner
        category_spinner = Spinner(
            text=item.category,
            values=[
                "Work",
                "Personal",
                "Shopping",
                "Health",
                "Finance",
                "Education",
                "Home",
            ],
            size_hint_y=0.15,
        )
        content.add_widget(category_spinner)

        # Priority spinner
        priority_spinner = Spinner(
            text=item.priority, values=["low", "medium", "high"], size_hint_y=0.15
        )
        content.add_widget(priority_spinner)

        # Buttons
        button_layout = BoxLayout(size_hint_y=0.2, spacing=5)

        def save_changes(btn):
            item.update(
                title=title_input.text,
                category=category_spinner.text,
                priority=priority_spinner.text,
            )
            self.storage.save(self.todo_list, "default")
            popup.dismiss()
            self.refresh_tasks()

        save_btn = Button(text="Save")
        save_btn.bind(on_press=save_changes)
        button_layout.add_widget(save_btn)

        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(cancel_btn)

        content.add_widget(button_layout)

        popup = Popup(title="Edit Task", content=content, size_hint=(0.9, 0.6))
        popup.open()


if __name__ == "__main__":
    app = TodoApp()
    app.run()

