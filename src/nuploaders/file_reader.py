#standard library imports
from abc import ABC, abstractmethod
from pathlib import Path

#third party 
import pandas as pd 


class FileReader(ABC):
    """This is the base class for reading of any files"""
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate_file()
    
    def _validate_file(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"File is not found {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Not a file {self.file_path}")

    @abstractmethod
    def read(self) -> pd.DataFrame:
        #will be implemented in baseclass
        pass

class ExcelReader(FileReader):
    """This class extends FileReader and read excel file (.xlsx)"""
    
    def read(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)
    
class CSVReader(FileReader):
    """This class extends FileReader and read csv file (.csv)"""

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

class JSONReader(FileReader):
    """This class extends FileReader and read json file (.json)"""
    #TOOD can add some exception handling to read JSON Serde format also

    def read(self) -> pd.DataFrame:
        return pd.read_json(self.file_path)

class ReadActor():
    """This is the actor class which will help read different types of files"""

    @staticmethod
    def read_file(filepath) -> FileReader:
        ext = Path(file_path).suffix.lower()
        if ext == '.csv':
            return CSVReader(filepath)
        elif ext == '.xlsx':
            return ExcelReader(filepath)
        elif ext == '.json':
            return JSONReader(filepath)
        else:
            raise ValueError(f"Only expecting to have csv, xlsx, or json file. Current format is {ext}")

        






