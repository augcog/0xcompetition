from typing import Optional, Union
from fastapi import FastAPI, Depends, Query, HTTPException
from v1.utils.block_db_sql_wrapper import BlockDBSQLWrapper
from fastapi.responses import RedirectResponse
import os
from v1.utils.models import *
import logging
import pandas as pd

logging.basicConfig(format=f'%(levelname)s - {__name__} - %(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
app = FastAPI()
fp = os.getenv("COMP_SETTING")
wrapper = BlockDBSQLWrapper(file_path=fp)


@app.get('/')
def index():
    #entering the url with no path will redirect you to the OpenAPI documentation
    return RedirectResponse(url="/docs/", status_code=303)


@app.get('/tables/{name}/columns/', response_model=Columns)
def list_columns(name: str):
    try:
        return Columns(table_name=name, columns=wrapper.list_columns(table_name=name))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Table name \'{e}\' not found!")


@app.get('/tables/{name}/indexes/', response_model=Indexes)
def list_indexes(name: str):
    try:
        return Indexes(table_name=name, indexes=wrapper.list_indexes(name))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Table name \'{e}\' not found!")


@app.get('/tables/{name}/primarykey/', response_model=PrimaryKeys)
def get_primary_key_info(name: str):
    try:
        return PrimaryKeys(table_name=name, primary_key=wrapper.get_primary_key_info(name))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Table name \'{e}\' not found!")


@app.get('/tables/{name}/foreignkeys/', response_model=ForeignKeys)
def get_foreign_keys_info(name: str):
    try:
        return ForeignKeys(table_name=name, foreign_keys=wrapper.get_foreign_keys_info(name))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Table name \'{e}\' not found!")


@app.get('/tables', response_model=Table)
def list_tables():
    tables = wrapper.list_tables()
    return Table(tables=tables)


@app.get("/query")
def query(q: str):
    """
     return query if query q is correct SQL format.

     Example: SELECT * FROM transactions WHERE from_address='0x804d39f546c5164af7612c3dca3683150e55bb78' ORDER BY transaction_index DESC
    NOTE:
        this is definitely a security breach, to allow foreign users to submit queries that are unfiltered.
    :param q: query to perform
    :return:
        A dictionary of {"result": ACTUAL result} or HTTP error if failure happened
    """
    try:
        result: pd.DataFrame = wrapper.query(q)
        return {"result": pd.DataFrame.to_json(result.to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
