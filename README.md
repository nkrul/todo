# 📝 Natural Language Todo App

A modern, multi-platform todo application with natural language parsing and temporal awareness. Write tasks the way you think about them: "call mom tomorrow" or "urgent meeting next friday".

## Features

### 🗣️ Natural Language Parsing
- Parse tasks using natural language like "buy milk tomorrow" or "call dentist next monday"
- Automatic date extraction from relative time words (today, tomorrow, yesterday, next week, etc.)
- Category and priority inference from keywords
- Support for multiple tasks in a single input

### ⏰ Temporal Awareness
- Understand relative dates: today, tomorrow, yesterday, next week, etc.
- Day of week references: "next monday", "next friday"
- Automatic due date calculation
- Overdue task tracking
- Today's tasks dashboard

### 💻 Multi-Platform
- **Web Interface**: Streamlit-based responsive web app
- **Mobile Interface**: Kivy-based native mobile app (iOS/Android)
- **Core Library**: Reusable domain logic shared across all platforms

### 📊 Features
- Task categorization (Work, Personal, Shopping, Health, Finance, Education, Home)
- Priority levels (low, medium, high)
- Task completion tracking
- Task statistics and analytics
- Persistent storage (JSON-based)
- Edit and delete tasks
- Filter by category, date, or status

## Project Structure

```
todo/
├── todo_core/               # Core domain logic (reusable)
│   ├── __init__.py
│   ├── models.py           # TodoItem and TodoList models
│   ├── parser.py           # Natural language parser
│   └── storage.py          # Storage management
├── todo_web/               # Web interface (Streamlit)
│   ├── __init__.py
│   └── app.py              # Main Streamlit app
├── todo_mobile/            # Mobile interface (Kivy)
│   ├── __init__.py
│   └── app.py              # Main Kivy app
├── tests/                  # Comprehensive test suite
│   ├── test_models.py
│   ├── test_parser.py
│   ├── test_storage.py
│   ├── __init__.py
│   └── conftest.py
├── setup.py               # Package setup
├── pyproject.toml         # Project metadata
├── requirements.txt       # All dependencies
├── requirements-core.txt  # Core dependencies only
├── requirements-web.txt   # Web interface dependencies
├── requirements-mobile.txt # Mobile interface dependencies
├── requirements-dev.txt   # Development dependencies
└── .github/workflows/     # CI/CD pipelines
```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip or poetry

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. **Install dependencies**

   For all features:
   ```bash
   python -m pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   # Core only
   python -m pip install -r requirements-core.txt
   
   # Web interface
   python -m pip install -r requirements-web.txt
   
   # Mobile interface
   python -m pip install -r requirements-mobile.txt
   
   # Development
   pip install -r requirements-dev.txt
   ```

3. **From source (development)**
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

## Usage

### Web Interface (Streamlit)

```bash
streamlit run todo_web/app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Add tasks with natural language
- View today's tasks, all tasks, or tasks by date range
- Edit and delete tasks
- View analytics and statistics
- Filter by category

### Mobile Interface (Kivy)

```bash
python -m todo_mobile
```

**Features:**
- Add tasks on the go
- Manage tasks with a mobile-friendly interface
- Same natural language parsing as web
- Local storage for offline access

### Core Library (Python API)

```python
from todo_core import TodoItem, TodoList, NaturalLanguageParser, StorageManager
from datetime import date

# Parse natural language
parser = NaturalLanguageParser()
item = parser.parse("Buy milk tomorrow")
print(item.title)        # "Buy milk"
print(item.due_date)     # 2024-01-10 (if today is 2024-01-09)
print(item.category)     # "Personal"
print(item.priority)     # "medium"

# Parse multiple items
items = parser.parse_multiple("""
    Buy groceries tomorrow
    Call mom today
    Finish report by friday
""")

# Manage tasks
todo_list = TodoList()
todo_list.add_item(item)

# Query tasks
today_tasks = todo_list.get_today_items()
overdue = todo_list.get_overdue_items()
work_tasks = todo_list.get_items_by_category("Work")

# Persist to disk
storage = StorageManager()
storage.save(todo_list, "my_tasks")
loaded = storage.load("my_tasks")
```

## Natural Language Examples

Here are some examples of what the parser understands:

### Dates
- "today" → today's date
- "tomorrow" → tomorrow's date  
- "yesterday" → yesterday's date
- "next week" → 7 days from today
- "next monday" → next occurrence of Monday
- "12/25" or "12-25" → December 25th of current/next year

### Priorities
- "urgent", "asap", "critical", "!!!", "priority" → high priority
- "important", "soon" → medium priority
- "later", "whenever" → low priority

### Categories
- "Work" → Work category
- "Personal" → Personal category
- "Shopping" → Shopping category
- "Health" → Health category
- "Finance" → Finance category
- "Education" → Education category
- "Home" → Home category

### Combined Examples
- "Buy milk tomorrow" → Personal, medium priority, tomorrow
- "urgent meeting next friday" → Personal, high priority, next Friday
- "Work report due today" → Work, medium priority, today
- "Important shopping list" → Shopping, medium priority, no specific date

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=todo_core --cov-report=html

# Run specific test file
pytest tests/test_parser.py -v

# Run specific test
pytest tests/test_parser.py::TestNaturalLanguageParser::test_parse_simple_task -v
```

### Test Coverage
- **test_models.py**: TodoItem and TodoList model tests
- **test_parser.py**: Natural language parser tests
- **test_storage.py**: Storage and persistence tests

Current test coverage includes:
- ✓ Basic task creation and management
- ✓ Date parsing for all temporal patterns
- ✓ Category and priority extraction
- ✓ Multiple task parsing
- ✓ Storage persistence
- ✓ JSON serialization/deserialization

## CI/CD

The project includes GitHub Actions workflows:

- **tests.yml**: Runs tests on Python 3.9-3.12, reports coverage
- **code-quality.yml**: Runs black, isort, flake8, and mypy checks

## Development

### Code Style

Format code with black:
```bash
black todo_core todo_web todo_mobile tests
```

Sort imports with isort:
```bash
isort todo_core todo_web todo_mobile tests
```

Lint with flake8:
```bash
flake8 todo_core todo_web todo_mobile tests
```

Type check with mypy:
```bash
mypy todo_core --ignore-missing-imports
```

### Adding New Features

1. Create a test for the feature in the appropriate test file
2. Implement the feature in the core module
3. Update the web/mobile interfaces if needed
4. Run the full test suite
5. Ensure code style compliance

## Architecture

### Core Module (Reusable)
- **models.py**: TodoItem and TodoList classes with business logic
- **parser.py**: NaturalLanguageParser for text → TodoItem conversion
- **storage.py**: StorageManager for persistence

### Web Module (Streamlit)
- Responsive UI with multiple views
- Real-time updates
- Analytics dashboard
- Task filtering and search

### Mobile Module (Kivy)
- Touch-friendly interface
- Cross-platform (iOS/Android)
- Local storage
- Minimalist design for mobile

## Performance Considerations

- Tasks are stored locally in JSON for quick access
- Parser uses regex for efficient date/category/priority extraction
- Streamlit caches session state for responsiveness
- Kivy provides native performance on mobile

## Future Enhancements

- [ ] Cloud synchronization across devices
- [ ] Recurring tasks
- [ ] Task attachments
- [ ] Collaboration features
- [ ] Advanced filtering and search
- [ ] Task templates
- [ ] Export to calendar apps
- [ ] Voice input
- [ ] Dark mode
- [ ] Offline-first architecture with sync

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for productive people everywhere**
