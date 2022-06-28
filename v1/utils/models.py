from pydantic import BaseModel, validator, ValidationError

from typing import List, Optional, Union


class Table(BaseModel):
    tables: List[str] = []


class Columns(BaseModel):
    table_name: str
    columns: List[str] = []
