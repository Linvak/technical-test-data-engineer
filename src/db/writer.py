import pandas as pd

class DataFrameManager:
    def __init__(self, csv_path: str, ):
        self.csv_path = csv_path
        try:
            self.df = pd.read_csv(csv_path)
        except FileNotFoundError:
            self.df = pd.DataFrame()

    def update_and_merge(self, new_df: pd.DataFrame, timestamp: str, primary_key: str = "id"):
        existing_df = self.df
        if not existing_df.empty:
            # Update the valid_until field for matching IDs
            for idx, new_row in new_df.iterrows():
                matching_rows = existing_df[(existing_df[primary_key] == new_row[primary_key]) & (existing_df['valid_until'].isna())]
                if not matching_rows.empty:
                    existing_df.loc[matching_rows.index, 'valid_until'] = timestamp

        # Append the new DataFrame to the existing DataFrame
        new_df['valid_until'] = None
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Save the merged DataFrame back to the CSV file
        updated_df.to_csv(self.csv_path, index=False)