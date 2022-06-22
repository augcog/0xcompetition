from typing import Optional, Union
from fastapi import FastAPI, Depends, Query, HTTPException
from v1.utils.competition_sql_wrapper import CompetitionSQLWrapper
from fastapi.responses import RedirectResponse
import os
from v1.utils.models import Table, Columns
import logging
import pandas as pd

logging.basicConfig(format=f'%(levelname)s - {__name__} - %(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
app = FastAPI()
fp = os.getenv("COMP_SETTING")
wrapper = CompetitionSQLWrapper(file_path=fp)


@app.get('/')
def index():
    return RedirectResponse(url="/docs/", status_code=303)


@app.get('/tables/{name}/columns/', response_model=Columns)
def list_columns(name: str):
    # TODO: @Winson, handle error
    return Columns(table_name=name, columns=wrapper.list_columns(table_name=name))


@app.get('/tables/{name}/indexes/')
def list_indexes(name: str):
    # TODO: @Winson, add response_model for validation
    # TODO: @Winson, handle error
    return {"indexes": wrapper.list_indexes(name)}


@app.get('/tables/{name}/primarykey/')
def get_primary_key_info(name: str):
    # TODO: @Winson, add response_model for validation
    # TODO: @Winson, handle error
    return {"primary key": wrapper.get_primary_key_info(name)}


@app.get('/tables/{name}/foreignkey/')
def get_foreign_keys_info(name: str):
    # TODO: @Winson, add response_model for validation
    # TODO: @Winson, handle error
    return {"primary key": wrapper.get_foreign_keys_info(name)}


@app.get('/tables')
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
        return {"result": result.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
