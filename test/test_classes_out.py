import datetime
from src.moovitamix_fastapi.classes_out import TracksOut, UsersOut, ListenHistoryOut, gender_list, genre_list

from src.api.api_client import PaginatedAPIClient
import pytest

from typing import List, Dict, Any

# Testing TracksOut
def test_tracks_out_generate_fake():
    track = TracksOut.generate_fake()
    assert isinstance(track.id, int)
    assert isinstance(track.name, str)
    assert isinstance(track.artist, str)
    assert isinstance(track.songwriters, str)
    assert isinstance(track.duration, str)
    assert isinstance(track.genres, str)
    assert isinstance(track.album, str)
    assert isinstance(track.created_at, datetime.datetime)
    assert isinstance(track.updated_at, datetime.datetime)

# Testing UsersOut
def test_users_out_generate_fake():
    user = UsersOut.generate_fake()
    assert isinstance(user.id, int)
    assert isinstance(user.first_name, str)
    assert isinstance(user.last_name, str)
    assert isinstance(user.email, str)
    assert user.gender in gender_list()
    assert user.favorite_genres in genre_list()
    assert isinstance(user.created_at, datetime.datetime)
    assert isinstance(user.updated_at, datetime.datetime)

# Testing ListenHistoryOut
def test_listen_history_out_generate_fake():
    history = ListenHistoryOut.generate_fake()
    assert history.user_id is None
    assert history.items is None
    assert isinstance(history.created_at, datetime.datetime)
    assert isinstance(history.updated_at, datetime.datetime)

import pytest
import json
import os
from tempfile import NamedTemporaryFile
from typing import Dict, Any
from src.db.metadata import MetadataReader  

@pytest.fixture
def temp_json_file():
    # Create a temporary JSON file with some initial metadata
    initial_metadata = {
        "table1": {"column1": "type1", "column2": "type2"},
        "table2": {"column3": "type3", "column4": "type4"}
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(initial_metadata, temp_file)
        temp_file_path = temp_file.name
    yield temp_file_path
    os.remove(temp_file_path)

def test_initialization(temp_json_file):
    reader = MetadataReader(temp_json_file)
    assert reader.file_path == temp_json_file
    assert reader.metadata == {
        "table1": {"column1": "type1", "column2": "type2"},
        "table2": {"column3": "type3", "column4": "type4"}
    }

def test_get_table_metadata(temp_json_file):
    reader = MetadataReader(temp_json_file)
    assert reader.get_table_metadata("table1") == {"column1": "type1", "column2": "type2"}
    assert reader.get_table_metadata("non_existent_table") is None


import os
from tempfile import NamedTemporaryFile
from src.db.writer import DataFrameManager 
import pandas as pd

@pytest.fixture
def temp_csv_file():
    # Create a temporary CSV file with some initial data
    initial_data = {
        "id": [1, 2],
        "name": ["Alice", "Bob"],
        "valid_until": [None, None]
    }
    df = pd.DataFrame(initial_data)
    with NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
    yield temp_file_path
    os.remove(temp_file_path)

def test_initialization_with_valid_csv(temp_csv_file):
    manager = DataFrameManager(temp_csv_file)
    assert not manager.df.empty
    assert list(manager.df.columns) == ["id", "name", "valid_until"]

def test_initialization_with_non_existent_csv():
    manager = DataFrameManager("non_existent_file.csv")
    assert manager.df.empty

def test_update_and_merge(temp_csv_file):
    manager = DataFrameManager(temp_csv_file)
    
    new_data = {
        "id": [1, 3],
        "name": ["Alice_updated", "Charlie"],
        "valid_until": [None, None]
    }
    new_df = pd.DataFrame(new_data)
    timestamp = "2023-01-01"

    manager.update_and_merge(new_df, timestamp)
    
    updated_df = pd.read_csv(temp_csv_file)
    
    # Check that the DataFrame has the correct number of rows
    assert len(updated_df) == 4
    
    # Check that the valid_until field was updated correctly for the existing row
    assert updated_df.loc[updated_df['id'] == 1, 'valid_until'].iloc[0] == timestamp
    
    # Check that the new row was added correctly
    assert updated_df.loc[updated_df['id'] == 3, 'name'].iloc[0] == "Charlie"
    assert pd.isna(updated_df.loc[updated_df['id'] == 3, 'valid_until']).iloc[0]

import pytest
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict, Any
from src.etl.loader import DataIngestion

# Mock implementation of PaginatedAPIClient
class MockPaginatedAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_all_pages(self, endpoint: str) -> List[Dict[str, Any]]:
        return [
            {"id": 1, "name": "Alice", "updated_at": "2023-01-01T00:00:00"},
            {"id": 2, "name": "Bob", "updated_at": "2023-01-02T00:00:00"},
        ]

class MockSchema(BaseModel):
    id: int
    name: str
    updated_at: str

@pytest.fixture
def data_ingestion():
    ingestion = DataIngestion(
        base_url="http://example.com/api",
        table="test_table",
        last_update="2023-01-01T00:00:00",
        schema=MockSchema
    )
    ingestion.api_client = MockPaginatedAPIClient(base_url="http://example.com/api")
    return ingestion

def test_initialization(data_ingestion):
    assert data_ingestion.table == "test_table"
    assert data_ingestion.last_update == "2023-01-01T00:00:00"
    assert data_ingestion.schema == MockSchema

def test_fetch_data(data_ingestion):
    data = data_ingestion.fetch_data()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"

def test_add_ingested_at(data_ingestion):
    df = pd.DataFrame([{"id": 1, "name": "Alice"}])
    enriched_df = data_ingestion.add_ingested_at(df)
    assert "ingested_at" in enriched_df.columns
    assert enriched_df["ingested_at"].iloc[0] == data_ingestion.ingestion_time

def test_filter_data(data_ingestion):
    items = [
        {"id": 1, "name": "Alice", "updated_at": "2023-01-01T00:00:00"},
        {"id": 2, "name": "Bob", "updated_at": "2023-01-02T00:00:00"},
    ]
    filtered_items = data_ingestion.filter_data(items)
    assert len(filtered_items) == 1
    assert filtered_items[0]["name"] == "Bob"


def test_validate_data(data_ingestion):
    items = [
        {"id": 1, "name": "Alice", "updated_at": "2023-01-01T00:00:00"},
        {"id": 2, "name": "Bob", "updated_at": "2023-01-02T00:00:00"},
        {"id": 3, "name": 123, "updated_at": "2023-01-02T00:00:00"},  # Invalid name type
    ]
    validated_items = data_ingestion.validate_data(items)
    assert len(validated_items) == 2
    assert validated_items[0]["name"] == "Alice"
    assert validated_items[1]["name"] == "Bob"

def test_execute(data_ingestion):
    final_df = data_ingestion.execute()
    assert len(final_df) == 1
    assert final_df["name"].iloc[0] == "Bob"
    assert "ingested_at" in final_df.columns
    assert "valid_until" in final_df.columns