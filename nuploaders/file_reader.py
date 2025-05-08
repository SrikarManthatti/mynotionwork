"""Module for reading files into pandas DataFrames in different formats (CSV, Excel, JSON)."""

# Standard library imports
from abc import ABC, abstractmethod
from pathlib import Path # pylint: disable=import-error

# Third-party imports
import pandas as pd # pylint: disable=import-error


class FileReader(ABC):
    """Abstract base class for reading files into DataFrames."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate_file()

    def _validate_file(self):
        """Check if file exists and is a valid file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Not a file: {self.file_path}")

    @abstractmethod
    def read(self) -> pd.DataFrame:
        """Abstract method to read file into a DataFrame."""
        pass


class ExcelReader(FileReader):
    """Reads Excel (.xlsx) files into a DataFrame."""

    def read(self) -> pd.DataFrame:
        """Read Excel file."""
        return pd.read_excel(self.file_path)


class CSVReader(FileReader):
    """Reads CSV (.csv) files into a DataFrame."""

    def read(self) -> pd.DataFrame:
        """Read CSV file."""
        return pd.read_csv(self.file_path)


class JSONReader(FileReader):
    """Reads JSON (.json) files into a DataFrame."""

    def read(self) -> pd.DataFrame:
        """Read JSON file."""
        return pd.read_json(self.file_path)


class ReadActor:
    """Factory class to select the appropriate file reader."""

    @staticmethod
    def read_file(filepath: str) -> FileReader:
        """Return a reader object based on file extension."""
        ext = Path(filepath).suffix.lower()
        if ext == '.csv':
            return CSVReader(filepath)
        if ext == '.xlsx':
            return ExcelReader(filepath)
        if ext == '.json':
            return JSONReader(filepath)
        raise ValueError(
            f"Only csv, xlsx, or json files are supported. Got: {ext}"
        )
