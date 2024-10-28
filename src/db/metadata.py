 
import json
from typing import Dict, Any, Optional

class MetadataReader:
    def __init__(self, file_path: str) -> None:
        """
        Initialize a new MetadataReader.

        :param file_path: The path to the JSON file containing the metadata.
        """
        self.file_path = file_path
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """
        Load the metadata from the JSON file.

        :return: A dictionary representing the metadata.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                metadata = json.load(file)
            print(f"Metadata successfully loaded from {self.file_path}")
            return metadata
        except FileNotFoundError:
            print(f"The file {self.file_path} does not exist.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file {self.file_path}.")
            return {}

    def get_table_metadata(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the metadata for a specific table.

        :param table_name: The name of the table.
        :return: A dictionary representing the table's metadata, or None if the table is not found.
        """
        return self.metadata.get(table_name)

    def update_table_metadata(self, table_name: str, new_metadata: Dict[str, Any]) -> None:
        """
        Update the metadata for a specific table.

        :param table_name: The name of the table.
        :param new_metadata: A dictionary containing the new metadata for the table.
        """
        self.metadata[table_name] = new_metadata
        self._save_metadata()

    def _save_metadata(self) -> None:
        """
        Save the updated metadata back to the JSON file.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.metadata, file, indent=4)
            print(f"Metadata successfully saved to {self.file_path}")
        except Exception as e:
            print(f"Failed to save metadata to {self.file_path}: {e}")
