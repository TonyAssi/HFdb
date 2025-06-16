import pandas as pd
from huggingface_hub import HfApi, HfFileSystem, upload_file, hf_hub_download

class HFdbClient:
    def __init__(self, repo_id, token):
        self.repo_id = repo_id
        self.token = token
        self.api = HfApi(token=token)
        self.fs = HfFileSystem(token=token)
        self.filepath = "db.csv"
        self._download()

    def _download(self):
        hf_hub_download(
            repo_id=self.repo_id,
            filename=self.filepath,
            token=self.token,
            repo_type="dataset",
            local_dir="."
        )

    def _upload(self):
        upload_file(
            path_or_fileobj=self.filepath,
            path_in_repo=self.filepath,
            repo_id=self.repo_id,
            repo_type="dataset",
            token=self.token
        )

    def _save_df(self, df):
        df.to_csv(self.filepath, index=False)
        self._upload()

    def add_row(self, row: dict):
        df = pd.read_csv(self.filepath)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        self._save_df(df)

    def get_df(self):
        return pd.read_csv(self.filepath)

    def get_row(self, column, value):
        df = pd.read_csv(self.filepath)
        match = df[df[column] == value]
        return match.iloc[0].to_dict() if not match.empty else None

    def delete_row(self, column, value):
        df = pd.read_csv(self.filepath)
        df = df[df[column] != value]
        self._save_df(df)

    def replace_element(self, find_column, find_value, update_column, new_value):
        df = pd.read_csv(self.filepath)
        mask = df[find_column] == find_value
        df.loc[mask, update_column] = new_value
        self._save_df(df)

    def replace_row(self, find_column, find_value, new_row: dict):
        df = pd.read_csv(self.filepath)
        df = df[df[find_column] != find_value]  # remove old row
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)  # add new one
        self._save_df(df)

    def row_exists(self, column, value):
        df = pd.read_csv(self.filepath)
        return not df[df[column] == value].empty

    def get_columns(self):
        df = pd.read_csv(self.filepath)
        return df.columns.tolist()

def create(repo_name, columns, token):
    api = HfApi(token=token)
    api.create_repo(
        repo_id=repo_name,
        repo_type="dataset",
        exist_ok=True,
        private=True
    )

    df = pd.DataFrame(columns=columns)
    filepath = "db.csv"
    df.to_csv(filepath, index=False)

    upload_file(
        path_or_fileobj=filepath,
        path_in_repo=filepath,
        repo_id=repo_name,
        repo_type="dataset",
        token=token
    )

    return HFdbClient(repo_id=repo_name, token=token)

def db(repo_name, token):
    return HFdbClient(repo_id=repo_name, token=token)
