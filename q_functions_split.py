from typing import Iterator, List
import pandas as pd
import sqlite3
import os
import pathlib

class db_query:
    def __init__(self, path: os.PathLike = None, text: str = None):
        if sum([1 for i in [path, text] if i ]) > 1:
            raise ValueError('only set path or text')
        self._path = None
        self._text = None

        if path:
            self.update_from_path(path)
        elif text:
            self.update_from_text(text)

    @property
    def query_path(self):
        return self._path
    @property
    def query_text(self):
        return self._text

    def update_from_path(self, path: os.PathLike, update_text: bool = True):
        self._path = db_query.attempt_normalize_path(path)
        if update_text:
            with open(self.query_path, 'r') as f:
                self.update_from_text(f.read())
    
    def update_from_text(self, text: str, clear_path: bool = False):
        if clear_path:
            self._path = None
        self._text = text
        
    @classmethod
    def attempt_normalize_path(cls, path: os.PathLike):
        # attempt to normalize path input to potential query paths
        if not os.path.exists(path):
            alternates = [
                f"queries/{path}.sql",
                f"queries/{path}",
                f"{path}.sql"
            ]
            exists = False
            for alt in alternates:
                if os.path.exists(alt):
                    exists = True
                    break
            if exists:
                path = alt
            else:
                raise FileNotFoundError(path)
        return path
        
class db_interface:
    def __init__(self, db_path: os.PathLike):
        if not os.path.exists(db_path):
            raise FileNotFoundError(db_path, 'must be valid path to sqlite db')
        self.db_path = db_path
        self._query: db_query = db_query()

    def set_query(self, path: os.PathLike = None, text: str = None, query: db_query = None) -> None:
        params_passed = sum([1 for i in [path, text, query] if i])
        if params_passed > 1:
            raise ValueError('only one of path, text, or query may be assigned')
        elif params_passed == 0:
            raise ValueError('must pass at least one of the parameters')

        if path:
            self._query.update_from_path(path)
        elif text:
            self._query.update_from_text(text, clear_path=True)
        elif query:
            self._query = query

    def get_df(self) -> pd.DataFrame:
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql(self._query.query_text, conn)
        except Exception as e:
            raise e
        finally:
            conn.close()
        return df
    
    def get_chunky_df(self, chunk: int) -> Iterator[pd.DataFrame]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                dfs = pd.read_sql(self._query.query_text, conn, chunksize=chunk)
            yield from dfs
        except Exception as e:
            raise e
        finally:
            conn.close()

    def export_path(self, filetype: str, filename: str = None) -> str:
        if self._query.query_path:
            return f"exports/{filetype}/{pathlib.Path(self._query.query_path).stem}.{filetype}"
        else:
            if not filename:
                raise ValueError('as query has no path, you must provide a filename')
            else:
                return f"exports/{filetype}/{filename}.{filetype}"

    def get_csv(self, filename: str = None, chunk: int = None) -> str:
        csv_path = self.export_path('csv', filename)
        os.makedirs(pathlib.Path(csv_path).parent, exist_ok=True)
        
        if chunk:
            dfs = self.get_chunky_df(chunk)
            first_iter = True
            for df in dfs:
                df: pd.DataFrame = df
                if first_iter:
                    df.to_csv(csv_path, index=False)
                    first_iter = False
                else:
                    df.to_csv(csv_path, index=False, mode="a", header=False)

        else:
            df = self.get_df()        
            df.to_csv(csv_path, index=False)
        
        return csv_path

    def get_json(self, filename: str = None) -> str:
        df = self.get_df()

        json_path = self.export_path('json', filename)
        os.makedirs(pathlib.Path(json_path).parent, exist_ok=True)
        
        df.to_json(json_path, orient='records')
        return json_path

    def csv_to_table(self, filename: str, tablename: str = None, columns: List[str] = None):
        try:
            if not tablename:
                tablename = pathlib.Path(filename).stem
            if columns:
                df = pd.read_csv(filename, names=columns, header=0)
            else:
                df = pd.read_csv(filename)

            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(tablename, conn)
        except Exception as e:
            raise e
        finally:
            conn.close()

    def exec_script(self, filename: str) -> None:
        """
            for running scripts like 'create view', 'drop table', 'alter table', etc
        """
        try:
            script_path = db_query.attempt_normalize_path(filename)
            with sqlite3.connect(self.db_path) as conn:
                with open(script_path, 'r') as f:
                    res = conn.executescript(f.read())
        except Exception as e:
            raise e
        finally:
            
            #? do something with res? return result code?
            conn.close()