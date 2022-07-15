from pydantic import BaseModel, validator, ValidationError

from typing import List, Optional, Union


class Table(BaseModel):
    tables: List[str] = []


class Columns(BaseModel):
    table_name: str
    columns: List[str] = []


class Indexes(BaseModel):
    table_name: str
    indexes: List[str] = []


class PrimaryKeys(BaseModel):
    table_name: str
    primary_key: List[str] = []


class ForeignKeys(BaseModel):
    table_name: str
    foreign_keys: List[str] = []

