
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Union

from pydantic import BaseModel, ValidationError


from src.api.api_client import PaginatedAPIClient




class DataIngestion:
    def __init__(self, base_url: str, table:str, last_update: str, schema:BaseModel):
        self.api_client = PaginatedAPIClient(base_url=base_url)
        self.last_update = last_update
        self.table = table
        self.schema = schema
        self.ingestion_time = datetime.now()
    
    def fetch_data(self):
        return self.api_client.fetch_all_pages(endpoint=self.table)

    def add_ingested_at(self, df: pd.DataFrame) -> pd.DataFrame:
        df['ingested_at'] = self.ingestion_time
        return df

    def filter_data(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        date_limit = datetime.fromisoformat(self.last_update)
        return [item for item in items if datetime.fromisoformat(item['updated_at']) > date_limit]

    def add_valid_until(self, df: pd.DataFrame) -> pd.DataFrame:
        df["valid_until"]  = None
        return df
    
    def validate_data(self, data: List[dict]) -> List[BaseModel]:
        validated_data = []
        for item in data:
            try:
                validated_item = self.schema(**item)
                validated_data.append(item)
            except ValidationError as e:
                print(f"Validation error for item {item}: {e}")
        return validated_data

    def execute(self) -> pd.DataFrame:
        # Fetch data from API
        data = self.fetch_data()

        # Filter data based on last_update
        filtered_data = self.filter_data(data)

        validated_data = self.validate_data(filtered_data)

        # Convert to pandas df for ease of use once data is filtered
        columns = self.schema.model_fields.keys()
        df = pd.DataFrame(validated_data, columns=columns)

        # Add ingested_at & valid_until timestamp
        enriched_data = self.add_ingested_at(df)
        final_data = self.add_valid_until(enriched_data)

        return final_data