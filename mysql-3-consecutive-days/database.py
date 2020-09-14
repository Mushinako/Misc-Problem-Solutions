#!/usr/bin/env python3
import sqlite3
from dataclasses import dataclass
from contextlib import contextmanager
from typing import List, Optional, Any

DATA = [
    ["a", "2020-09-11"],
    ["b", "2020-09-12"],
    ["c", "2020-09-13"],
    ["c", "2020-09-12"],
    ["c", "2020-09-11"],
    ["d", "2020-09-10"],
    ["e", "2020-09-11"],
    ["d", "2020-09-11"],
    ["b", "2020-09-11"],
    ["b", "2020-09-10"],
]


@dataclass
class Field:
    name: str
    type: str
    primary_key: bool = False
    not_null: bool = False
    unique: bool = False
    default: Any = None
    check: Optional[str] = None

    @property
    def field(self) -> str:
        base_str = f"{self.name} {self.type}"
        if self.primary_key:
            base_str += " PRIMARY KEY"
            return base_str
        if self.not_null:
            base_str += " NOT NULL"
        if self.unique:
            base_str += " UNIQUE"
        if self.default is not None:
            base_str += f" DEFAULT {self.default!r}"
        if self.check is not None:
            base_str += f" CHECK({self.check})"
        return base_str


DB_PATH = "database.sqlite"
TABLE_NAME = "logins"
PRIMARY_KEY = Field("id", "INTEGER", primary_key=True)
FIELDS = [
    Field("name", "TEXT", not_null=True),
    Field("last_login_date", "TEXT", not_null=True),
]


@contextmanager
def connect_to_db():
    """Context manager wrapper for sqlite database connection

    Yields:
        conn (sqlite3.Connection): The connection to sqlite database
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    finally:
        if conn:
            conn.close()


def create_table(conn: sqlite3.Connection, table_name: str, primary_key: Field, fields: List[Field], overwrite: bool = True) -> None:
    """Create table of given name

    Args:
        conn       (sqlite3.Connection): Database connection
        table_name (str)               : Table name
        fields     (list[Field])       : Fields to be added
    """

    if overwrite:
        drop_command_tempate = f"DROP TABLE IF EXISTS {table_name}"
        with conn:
            cursor = conn.execute(drop_command_tempate)

    field_properties = (", ").join(field.field for field in fields)
    create_command_template = f"""CREATE TABLE IF NOT EXISTS {table_name} ({primary_key.field}, {field_properties})"""
    with conn:
        cursor = conn.execute(create_command_template)


def insert_data(conn: sqlite3.Connection, table_name: str, headers: List[str], data: List[List]) -> None:
    """Insert data import table

    Args:
        conn       (sqlite3.Connection): Database connection
        table_name (str)               : Table name
        headers    (list[str])         : Column headers
        data       (list[list])        : Table data
    """

    col_count = len(headers)
    col_counts = tuple(set((len(datum) for datum in data)))
    if len(col_counts) > 1:
        raise ValueError("Different argument lengths detected!")
    col_count_args = col_counts[0]
    if col_count != col_count_args:
        raise ValueError("Header length does not match argument lengths!")
    if (col_count) < 1:
        raise ValueError("Invalid argument lengths detected!")
    xtra_col_count = col_counts[0] - 1
    args_placeholder = f"(?{', ?' * xtra_col_count})"
    command_template = f"""INSERT INTO {table_name} ({", ".join(headers)}) VALUES {args_placeholder}"""
    with conn:
        cursor = conn.executemany(command_template, data)


def prepare_database(conn: sqlite3.Connection) -> None:
    """Prepare database for testing

    Args:
        conn (sqlite3.Connection): Database connection
    """

    create_table(conn, TABLE_NAME, PRIMARY_KEY, FIELDS)

    field_names = [field.name for field in FIELDS]
    insert_data(conn, TABLE_NAME, field_names, DATA)


def execute_date_search(conn: sqlite3.Connection) -> None:
    """Do the date search

    Args:
        conn (sqlite3.Connection): Database connection
    """

    date_field = "last_login_date"
    command = f"""SELECT name FROM {TABLE_NAME} n WHERE EXISTS(SELECT 1 FROM {TABLE_NAME} WHERE name=n.name AND date({date_field})=date(n.{date_field}, "+1 day")) AND EXISTS(SELECT 1 FROM {TABLE_NAME} WHERE name=n.name AND date({date_field})=date(n.{date_field}, "+2 day"))"""
    with conn:
        cursor = conn.execute(command)
    print([record[0] for record in cursor.fetchall()])


def main() -> None:
    with connect_to_db() as conn:
        prepare_database(conn)
        execute_date_search(conn)


if __name__ == "__main__":
    main()
