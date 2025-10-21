"""
Setup script for Airflow Teams Notifier package.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory.parent / "README.md").read_text(encoding='utf-8')

setup(
    name="airflow-teams-notifier",
    version="1.0.0",
    author="Naval Hatode, Akshay Prabhu",
    author_email="navalhatode@gmail.com",
    description="A Python-based notification system for Airflow DAG failures with Microsoft Teams integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/navalhatode/airflow_teams_notifier",
    packages=find_packages(where="."),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.6.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "pylint>=2.12.0",
            "mypy>=0.930",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
