"""Main Streamlit app entry point."""

import sys
from pathlib import Path

# Add the project root to sys.path so this script can be run directly.
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from todo_web import main

if __name__ == "__main__":
    main()

