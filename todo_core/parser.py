"""Natural language parsing for todo items."""

import re
from datetime import date, datetime, timedelta
from typing import Callable, Dict, List, Optional, Union

from .models import TodoItem


class NaturalLanguageParser:
    """Parse natural language input to extract todo items with due dates."""

    # Relative date patterns
    RELATIVE_PATTERNS: Dict[str, Union[int, Callable[[], int]]] = {
        r"\btoday\b": 0,
        r"\btomorrow\b": 1,
        r"\byesterday\b": -1,
        r"\bnext\s+week\b": 7,
        r"\bnext\s+monday\b": lambda: NaturalLanguageParser._days_until(0),
        r"\bnext\s+tuesday\b": lambda: NaturalLanguageParser._days_until(1),
        r"\bnext\s+wednesday\b": lambda: NaturalLanguageParser._days_until(2),
        r"\bnext\s+thursday\b": lambda: NaturalLanguageParser._days_until(3),
        r"\bnext\s+friday\b": lambda: NaturalLanguageParser._days_until(4),
        r"\bnext\s+saturday\b": lambda: NaturalLanguageParser._days_until(5),
        r"\bnext\s+sunday\b": lambda: NaturalLanguageParser._days_until(6),
    }

    CATEGORIES = [
        "Work",
        "Personal",
        "Shopping",
        "Health",
        "Finance",
        "Education",
        "Home",
    ]

    PRIORITY_KEYWORDS = {
        r"\b(urgent|asap|critical|immediately|priority)\b|!{2,}": "high",
        r"\b(important|soon)\b": "medium",
        r"\b(later|whenever)\b": "low",
    }

    @staticmethod
    def _days_until(day_of_week: int) -> int:
        """Calculate days until next occurrence of day_of_week (0=Monday, 6=Sunday)."""
        today = date.today()
        current_day = today.weekday()
        days_ahead = day_of_week - current_day
        if days_ahead <= 0:
            days_ahead += 7
        return days_ahead

    @staticmethod
    def _extract_date(text: str) -> Optional[date]:
        """Extract a due date from text using relative and absolute patterns."""
        text_lower = text.lower()

        # Check relative patterns
        for pattern, offset in NaturalLanguageParser.RELATIVE_PATTERNS.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                offset_days: int = offset() if callable(offset) else offset
                return date.today() + timedelta(days=offset_days)

        # Check for absolute date patterns (MM/DD or MM-DD or MM.DD)
        date_matches = re.findall(r"\b(\d{1,2})[/\-\.](\d{1,2})(?:[/\-\.](\d{2,4}))?\b", text)
        if date_matches:
            month, day, year = date_matches[0]
            try:
                if year:
                    parsed_date = datetime.strptime(f"{month}/{day}/{year}", "%m/%d/%Y").date()
                else:
                    # Assume current or next year
                    try:
                        parsed_date = datetime.strptime(
                            f"{month}/{day}/{date.today().year}", "%m/%d/%Y"
                        ).date()
                        if parsed_date < date.today():
                            parsed_date = datetime.strptime(
                                f"{month}/{day}/{date.today().year + 1}", "%m/%d/%Y"
                            ).date()
                    except ValueError:
                        return None
                return parsed_date
            except ValueError:
                pass

        return None

    @staticmethod
    def _extract_category(text: str) -> str:
        """Extract category from text."""
        text_lower = text.lower()
        for category in NaturalLanguageParser.CATEGORIES:
            if category.lower() in text_lower:
                return category
        return "Personal"

    @staticmethod
    def _extract_priority(text: str) -> str:
        """Extract priority level from text."""
        text_lower = text.lower()
        for pattern, priority in NaturalLanguageParser.PRIORITY_KEYWORDS.items():
            if re.search(pattern, text_lower):
                return priority
        return "medium"

    @staticmethod
    def _clean_title(text: str) -> str:
        """Clean the title by removing date and priority keywords."""
        # Remove relative date keywords
        for pattern in NaturalLanguageParser.RELATIVE_PATTERNS.keys():
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Remove priority keywords
        for pattern in NaturalLanguageParser.PRIORITY_KEYWORDS.keys():
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Remove dates
        text = re.sub(r"\d{1,2}[/\-\.]\d{1,2}(?:[/\-\.]\d{2,4})?", "", text)

        # Clean up extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    @staticmethod
    def parse(text: str) -> Optional[TodoItem]:
        """Parse a natural language string into a TodoItem."""
        if not text or not text.strip():
            return None

        title = NaturalLanguageParser._clean_title(text)
        if not title:
            return None

        due_date = NaturalLanguageParser._extract_date(text)
        category = NaturalLanguageParser._extract_category(text)
        priority = NaturalLanguageParser._extract_priority(text)

        return TodoItem(title=title, due_date=due_date, category=category, priority=priority)

    @staticmethod
    def parse_multiple(text: str) -> List[TodoItem]:
        """
        Parse multiple todo items from text.
        Items can be separated by newlines, commas, or 'and'.
        """
        # Split by common separators
        items_text = re.split(r"[\n;]|(?:^|\s)and(?:\s|$)", text)

        items = []
        for item_text in items_text:
            item = NaturalLanguageParser.parse(item_text.strip())
            if item:
                items.append(item)

        return items
