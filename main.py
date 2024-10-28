from src.etl.loader import DataIngestion
from src.db.metadata import MetadataReader
from src.db.classes_in import ListenHistoryIn, TracksIn, UsersIn
from src.db.writer import DataFrameManager
import requests
import os

API_BASE = "http://127.0.0.1:8000/"

schemas = {
    "tracks": TracksIn,
    "users": UsersIn,
    "listen_history": ListenHistoryIn
}

metadata_path = "data/ingestion_metadata.json"
database_path = "data/"

# Utilisation
if __name__ == "__main__":
    metadata = MetadataReader(metadata_path)
    for endpoint in schemas.keys():
        table_metadata = metadata.get_table_metadata(table_name=endpoint)
        if table_metadata is None:
            table_metadata = {}
        last_updated_at = table_metadata.get("updated_at", "2010-10-05T14:48:00")
        schema = schemas[endpoint]
        ingest = DataIngestion(base_url=API_BASE, table=endpoint, last_update=last_updated_at, schema=schema)
        try:
            new_data = ingest.execute()
            max_updated_at = max(new_data["updated_at"], default = last_updated_at)
            db_handler = DataFrameManager(csv_path=os.path.join(database_path, f"{endpoint}.csv"))
            db_handler.update_and_merge(new_df=new_data, timestamp=ingest.ingestion_time)
            metadata.update_table_metadata(endpoint, {"updated_at": max_updated_at})
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        # except Exception as err:
        #     print(f"An error occurred: {err}")