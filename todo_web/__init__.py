"""Web interface for the todo app using Streamlit."""

import sys
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo_core import NaturalLanguageParser, StorageManager, TodoItem


def init_session_state():
    """Initialize Streamlit session state."""
    if "storage" not in st.session_state:
        st.session_state.storage = StorageManager()
    if "todo_list" not in st.session_state:
        st.session_state.todo_list = st.session_state.storage.load("default")


def save_to_storage():
    """Save current todo list to storage."""
    st.session_state.storage.save(st.session_state.todo_list, "default")


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="📝 Natural Language Todo",
        page_icon="✓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📝 Natural Language Todo App")
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()

    st.markdown(
        "Type tasks using natural language like *'call mom tomorrow'* or *'urgent meeting today'*"
    )

    # Sidebar for statistics
    with st.sidebar:
        st.header("📊 Statistics")
        pending = st.session_state.todo_list.get_pending_items()
        overdue = st.session_state.todo_list.get_overdue_items()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(st.session_state.todo_list.items))
        with col2:
            st.metric("Pending", len(pending))
        with col3:
            st.metric("Overdue", len(overdue))

        st.markdown("---")

        # Category filter
        st.subheader("🏷️ Filter by Category")
        categories = set(item.category for item in st.session_state.todo_list.items)
        categories.add("All")
        selected_category = st.radio("Category", sorted(categories), index=0)

        st.markdown("---")

        # View options
        st.subheader("👁️ View Options")
        show_completed = st.checkbox("Show Completed", value=False)

    # Main content
    tabs = st.tabs(["Add Task", "Today", "All Tasks", "By Date", "Analytics"])

    # Tab 1: Add Task
    with tabs[0]:
        st.subheader("➕ Add a New Task")

        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.text_area(
                "Enter task (natural language)",
                placeholder="e.g., 'Buy groceries tomorrow' or 'Important meeting next friday'",
                height=100,
            )
        with col2:
            st.write("")
            st.write("")
            parse_button = st.button("Parse & Add", use_container_width=True)

        if parse_button and user_input:
            parsed_items = NaturalLanguageParser.parse_multiple(user_input)
            if parsed_items:
                for item in parsed_items:
                    st.session_state.todo_list.add_item(item)
                save_to_storage()
                st.success(f"✅ Added {len(parsed_items)} task(s)!")
                st.rerun()
            else:
                st.error("❌ Could not parse the input. Please try again.")

        st.markdown("---")
        st.subheader("📋 or Add Task Manually")

        col1, col2, col3 = st.columns(3)
        with col1:
            title = st.text_input("Task Title")
        with col2:
            due_date = st.date_input("Due Date", value=date.today(), label_visibility="collapsed")
        with col3:
            category = st.selectbox(
                "Category",
                [
                    "Work",
                    "Personal",
                    "Shopping",
                    "Health",
                    "Finance",
                    "Education",
                    "Home",
                ],
                label_visibility="collapsed",
            )

        priority = st.select_slider("Priority", options=["low", "medium", "high"])
        description = st.text_area("Description (optional)", height=80)

        if st.button("Add Manual Task", use_container_width=True):
            if title:
                item = TodoItem(
                    title=title,
                    due_date=due_date,
                    category=category,
                    priority=priority,
                    description=description,
                )
                st.session_state.todo_list.add_item(item)
                save_to_storage()
                st.success("✅ Task added!")
                st.rerun()
            else:
                st.error("Please enter a task title")

    # Tab 2: Today's Tasks
    with tabs[1]:
        st.subheader("📅 Today's Tasks")
        today_tasks = st.session_state.todo_list.get_today_items()

        if today_tasks:
            for item in today_tasks:
                if not item.completed or show_completed:
                    display_task_item(item, key_prefix="today")
        else:
            st.info("No tasks for today!")

    # Tab 3: All Tasks
    with tabs[2]:
        st.subheader("📚 All Tasks")

        # Filter tasks
        tasks_to_show = st.session_state.todo_list.items
        if selected_category != "All":
            tasks_to_show = [t for t in tasks_to_show if t.category == selected_category]
        if not show_completed:
            tasks_to_show = [t for t in tasks_to_show if not t.completed]

        if tasks_to_show:
            # Sort by due date
            tasks_to_show.sort(key=lambda x: (x.completed, x.due_date or date.today()))

            for item in tasks_to_show:
                display_task_item(item, key_prefix="all")
        else:
            st.info("No tasks to display")

    # Tab 4: By Date
    with tabs[3]:
        st.subheader("📆 Tasks by Date")

        # Get date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today())
        with col2:
            end_date = st.date_input("End Date", value=date.today() + timedelta(days=7))

        # Display tasks by date
        current_date = start_date
        while current_date <= end_date:
            day_tasks = [t for t in st.session_state.todo_list.items if t.due_date == current_date]
            if day_tasks or current_date == date.today():
                st.subheader(f"📅 {current_date.strftime('%A, %B %d, %Y')}")
                if day_tasks:
                    for item in day_tasks:
                        if not item.completed or show_completed:
                            display_task_item(item, key_prefix=f"date_{current_date.isoformat()}")
                else:
                    st.caption("No tasks scheduled")
            current_date += timedelta(days=1)

    # Tab 5: Analytics
    with tabs[4]:
        st.subheader("📊 Task Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Tasks", len(st.session_state.todo_list.items))
            st.metric("Completed", sum(1 for t in st.session_state.todo_list.items if t.completed))
            st.metric("Overdue", len(st.session_state.todo_list.get_overdue_items()))

        with col2:
            categories = {}
            for item in st.session_state.todo_list.items:
                categories[item.category] = categories.get(item.category, 0) + 1

            if categories:
                st.bar_chart(categories)

        st.markdown("---")
        st.subheader("Priority Distribution")
        priorities = {}
        for item in st.session_state.todo_list.items:
            if not item.completed:
                priorities[item.priority] = priorities.get(item.priority, 0) + 1

        if priorities:
            st.bar_chart(priorities)


def display_task_item(item: TodoItem, key_prefix: str = "task"):
    """Display a single task item with controls."""
    with st.container():
        col1, col2, col3, col4 = st.columns([0.5, 3, 1, 1])

        # Checkbox for completion
        with col1:
            is_completed = st.checkbox(
                "completed",
                value=item.completed,
                key=f"{key_prefix}_check_{item.id}",
                label_visibility="collapsed",
            )
            if is_completed != item.completed:
                if is_completed:
                    item.mark_complete()
                else:
                    item.mark_incomplete()
                save_to_storage()

        # Task info
        with col2:
            text_decoration = "line-through" if item.completed else "none"
            due_date_str = f" • {item.due_date}" if item.due_date else ""
            priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(item.priority, "⚪")
            st.markdown(
                f"<span style='text-decoration:{text_decoration}'>"
                f"{item.title}</span><br/>"
                f"<small>{item.category} • {priority_emoji} {item.priority}{due_date_str}</small>",
                unsafe_allow_html=True,
            )

        edit_flag_key = f"{key_prefix}_edit_mode_{item.id}"

        # Edit button
        with col3:
            if st.button("✏️", key=f"{key_prefix}_edit_{item.id}"):
                st.session_state[edit_flag_key] = True

        # Delete button
        with col4:
            if st.button("🗑️", key=f"{key_prefix}_delete_{item.id}"):
                st.session_state.todo_list.remove_item(item.id)
                save_to_storage()
                st.rerun()

        # Edit mode
        if st.session_state.get(edit_flag_key, False):
            with st.expander("Edit Task", expanded=True):
                new_title = st.text_input(
                    "Title", value=item.title, key=f"{key_prefix}_edit_title_{item.id}"
                )
                new_category = st.selectbox(
                    "Category",
                    [
                        "Work",
                        "Personal",
                        "Shopping",
                        "Health",
                        "Finance",
                        "Education",
                        "Home",
                    ],
                    index=[
                        "Work",
                        "Personal",
                        "Shopping",
                        "Health",
                        "Finance",
                        "Education",
                        "Home",
                    ].index(item.category),
                    key=f"{key_prefix}_edit_category_{item.id}",
                )
                new_due_date = st.date_input(
                    "Due Date",
                    value=item.due_date or date.today(),
                    key=f"{key_prefix}_edit_date_{item.id}",
                )
                new_priority = st.select_slider(
                    "Priority",
                    options=["low", "medium", "high"],
                    value=item.priority,
                    key=f"{key_prefix}_edit_priority_{item.id}",
                )
                new_description = st.text_area(
                    "Description",
                    value=item.description,
                    key=f"{key_prefix}_edit_desc_{item.id}",
                    height=80,
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save", key=f"{key_prefix}_save_{item.id}"):
                        item.update(
                            title=new_title,
                            category=new_category,
                            due_date=new_due_date,
                            priority=new_priority,
                            description=new_description,
                        )
                        save_to_storage()
                        st.session_state[edit_flag_key] = False
                        st.rerun()
                with col2:
                    if st.button("Cancel", key=f"{key_prefix}_cancel_{item.id}"):
                        st.session_state[edit_flag_key] = False
                        st.rerun()

        st.divider()


if __name__ == "__main__":
    main()
