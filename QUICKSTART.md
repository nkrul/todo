# Quick Start Guide

Get up and running with the Natural Language Todo App in minutes!

## 30-Second Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/todo-app.git
cd todo-app

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Run the web app
streamlit run todo_web/app.py
```

Visit `http://localhost:8501` in your browser!

## Use Cases

### Add a task with natural language
```
Type in the input box: "Buy milk tomorrow"
Click "Parse & Add"
✓ Task added with automatic date and category!
```

### Use different date formats
- "today" → today
- "tomorrow" → tomorrow
- "next friday" → next Friday
- "12/25" → December 25th
- "next week" → one week from today

### Indicate priority
- "urgent", "asap", "!!!" → high priority
- "important" → medium priority  
- "later" → low priority

### Specify category
- "Work" → Work category
- "Shopping" → Shopping category
- "Personal" → Personal category
- And more (Finance, Health, Education, Home)

## As a Library

Use the core module in your own Python projects:

```python
from todo_core import NaturalLanguageParser

parser = NaturalLanguageParser()
item = parser.parse("Buy milk tomorrow")

print(item.title)      # "Buy milk"
print(item.due_date)   # 2024-01-10
print(item.category)   # "Personal"
```

## Commands

```bash
# Run tests
pytest tests/ -v

# Format code
make format

# Run linter
make lint

# Run web app
make run-web

# Run mobile app  
make run-mobile

# See all commands
make help
```

## Project Layout

```
todo/
├── todo_core/       ← Reusable library
├── todo_web/        ← Web interface
├── todo_mobile/     ← Mobile interface
├── tests/           ← Tests
└── examples.py      ← Example usage
```

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🧪 Run examples: `python examples.py`
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- 📚 Check tests in `tests/` for usage examples

## Troubleshooting

### "Module not found" errors
```bash
python -m pip install -r requirements.txt
```

### Streamlit not starting
```bash
python -m pip install streamlit --upgrade
```

### Tests failing
```bash
# Make sure you're in the project root
cd /path/to/todo-app
pytest tests/ -v
```

## Tips & Tricks

1. **Combine multiple items**: Enter them on separate lines or separated by commas
2. **Quick dates**: "today", "tomorrow", "next monday" are fastest
3. **Edit inline**: Click the pencil icon to edit any task
4. **Filter by category**: Use the sidebar to focus on specific categories
5. **Batch operations**: Check multiple tasks to mark them complete together

## Getting Help

- 📋 Open an issue on GitHub
- 💬 Check existing issues for answers
- 📧 Email the maintainers

---

**Ready to be productive? Start using the app now! 🚀**
