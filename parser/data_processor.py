import json
import csv
import io
from typing import Dict, Any

class DataProcessor:
    @staticmethod
    def process_json(json_data: str) -> Dict[str, Any]:
        """
        Converts a JSON string to a Python dictionary.
        
        Args:
            json_data (str): A string containing JSON data.
        
        Returns:
            Dict[str, Any]: The parsed JSON data as a dictionary.
        
        Raises:
            ValueError: If the JSON data is invalid.
        """
        try:
            data = json.loads(json_data)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {str(e)}")

    @staticmethod
    def flatten_dict(d, parent_key='', sep='_'):
        """
        Recursively flattens a nested dictionary.
        
        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The parent key for nested dictionaries.
            sep (str): The separator to use between keys.
        
        Returns:
            dict: A flattened version of the input dictionary.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataProcessor.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(DataProcessor.flatten_dict({f"{new_key}{sep}{i}": item}, sep=sep).items())
                    else:
                        items.append((f"{new_key}{sep}{i}", str(item)))
            else:
                items.append((new_key, str(v)))
        return dict(items)

    @staticmethod
    def save_to_csv_flattened(data: Dict[str, Any]) -> str:
        """
        Saves a flattened dictionary to a CSV string.
        
        Args:
            data (Dict[str, Any]): The dictionary to save.
        
        Returns:
            str: The CSV content as a string.
        
        Raises:
            ValueError: If there's no data to save.
        """
        if not data:
            raise ValueError("No data to save")
        
        # Flatten the input dictionary
        flattened_data = DataProcessor.flatten_dict(data)
        
        # Create a CSV string using a StringIO object
        csv_content = io.StringIO()
        writer = csv.writer(csv_content)
        writer.writerow(['Key', 'Value'])  # Write header
        for key, value in flattened_data.items():
            writer.writerow([key, value])
        
        return csv_content.getvalue()