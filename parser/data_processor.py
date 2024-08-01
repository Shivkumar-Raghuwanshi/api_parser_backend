
import json
import csv
import io
from typing import Dict, Any

class DataProcessor:
    @staticmethod
    def process_json(json_data: str) -> Dict[str, Any]:
        try:
            data = json.loads(json_data)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {str(e)}")

    @staticmethod
    def flatten_dict(d, parent_key='', sep='_'):
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
        if not data:
            raise ValueError("No data to save")
        
        flattened_data = DataProcessor.flatten_dict(data)
        
        csv_content = io.StringIO()
        writer = csv.writer(csv_content)
        writer.writerow(['Key', 'Value'])
        for key, value in flattened_data.items():
            writer.writerow([key, value])
        
        return csv_content.getvalue()