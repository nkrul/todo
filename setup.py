"""Setup configuration for todo app."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="todo-app",
    version="0.1.0",
    author="Todo App Team",
    description="A natural language todo app with temporal awareness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/todo-app",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.28.0",
        "kivy>=2.2.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "web": [
            "streamlit>=1.28.0",
        ],
        "mobile": [
            "kivy>=2.2.1",
            "kivy-garden>=0.1.5",
        ],
    },
)
