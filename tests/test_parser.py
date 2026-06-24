"""Tests for natural language parser."""

import pytest
from datetime import date, timedelta
from todo_core.parser import NaturalLanguageParser


class TestNaturalLanguageParser:
    """Test cases for NaturalLanguageParser."""

    def test_parse_simple_task(self):
        """Test parsing a simple task."""
        item = NaturalLanguageParser.parse("Buy milk")
        assert item is not None
        assert item.title == "Buy milk"
        assert item.category == "Personal"

    def test_parse_task_with_today(self):
        """Test parsing task with 'today'."""
        item = NaturalLanguageParser.parse("Call mom today")
        assert item is not None
        assert "Call mom" in item.title
        assert item.due_date == date.today()

    def test_parse_task_with_tomorrow(self):
        """Test parsing task with 'tomorrow'."""
        item = NaturalLanguageParser.parse("Buy groceries tomorrow")
        assert item is not None
        assert "Buy groceries" in item.title
        assert item.due_date == date.today() + timedelta(days=1)

    def test_parse_task_with_yesterday(self):
        """Test parsing task with 'yesterday'."""
        item = NaturalLanguageParser.parse("Should have done this yesterday")
        assert item is not None
        assert item.due_date == date.today() - timedelta(days=1)

    def test_parse_task_with_category(self):
        """Test parsing task with category keyword."""
        item = NaturalLanguageParser.parse("Buy milk at Shopping")
        assert item is not None
        assert item.category == "Shopping"

    def test_parse_task_with_work_category(self):
        """Test parsing task with work category."""
        item = NaturalLanguageParser.parse("Finish report for Work")
        assert item is not None
        assert item.category == "Work"

    def test_parse_task_with_priority_urgent(self):
        """Test parsing task with high priority marker."""
        item = NaturalLanguageParser.parse("Fix bug !!!")
        assert item is not None
        assert item.priority == "high"

    def test_parse_task_with_priority_important(self):
        """Test parsing task with medium priority marker."""
        item = NaturalLanguageParser.parse("Important meeting tomorrow")
        assert item is not None
        assert item.priority == "medium"

    def test_parse_task_with_priority_low(self):
        """Test parsing task with low priority marker."""
        item = NaturalLanguageParser.parse("Do this later")
        assert item is not None
        assert item.priority == "low"

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        item = NaturalLanguageParser.parse("")
        assert item is None

    def test_parse_multiple_tasks(self):
        """Test parsing multiple tasks."""
        text = "Buy milk today\nCall mom tomorrow\nFinish report"
        items = NaturalLanguageParser.parse_multiple(text)
        assert len(items) >= 2

    def test_parse_task_with_date(self):
        """Test parsing task with specific date."""
        item = NaturalLanguageParser.parse("Meeting on 12/25")
        assert item is not None
        assert item.due_date is not None

    def test_extract_date_today(self):
        """Test extracting 'today' date."""
        date_obj = NaturalLanguageParser._extract_date("due today")
        assert date_obj == date.today()

    def test_extract_date_tomorrow(self):
        """Test extracting 'tomorrow' date."""
        date_obj = NaturalLanguageParser._extract_date("due tomorrow")
        assert date_obj == date.today() + timedelta(days=1)

    def test_extract_date_none(self):
        """Test extracting date when none present."""
        date_obj = NaturalLanguageParser._extract_date("just a regular task")
        assert date_obj is None

    def test_extract_category_work(self):
        """Test extracting Work category."""
        category = NaturalLanguageParser._extract_category("Work meeting tomorrow")
        assert category == "Work"

    def test_extract_category_personal(self):
        """Test extracting Personal category."""
        category = NaturalLanguageParser._extract_category("Personal task")
        assert category == "Personal"

    def test_extract_priority_high(self):
        """Test extracting high priority."""
        priority = NaturalLanguageParser._extract_priority("Urgent bug fix!!!")
        assert priority == "high"

    def test_extract_priority_low(self):
        """Test extracting low priority."""
        priority = NaturalLanguageParser._extract_priority("Do this later")
        assert priority == "low"

    def test_clean_title(self):
        """Test cleaning title."""
        title = NaturalLanguageParser._clean_title(
            "Buy milk tomorrow for Work !!! urgent"
        )
        assert "tomorrow" not in title.lower()
        assert "urgent" not in title.lower()
        assert "Buy milk" in title

    def test_parse_next_week(self):
        """Test parsing 'next week' date."""
        item = NaturalLanguageParser.parse("Vacation next week")
        assert item is not None
        assert item.due_date == date.today() + timedelta(days=7)

    def test_parse_task_no_title_after_cleaning(self):
        """Test parsing when all content is temporal/priority markers."""
        item = NaturalLanguageParser.parse("tomorrow !!!")
        # Should either return None or a minimal item
        if item is not None:
            assert item.title == "" or item.title.strip() == ""
