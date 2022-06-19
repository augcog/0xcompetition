from fastapi import FastAPI, Query
from EasyVersion import competition_sql_wrapper


app = FastAPI()
fp = "./settings.json"
wrapper = competition_sql_wrapper.CompetitionSQLWrapper(file_path=fp)


@app.get('/')
def index():
    return {"message": "Hello World"}


@app.get('/tables/')
def list_tables():
    return {"tables": wrapper.list_tables()}


@app.get('/tables/{name}/columns/')
def list_columns(name: str):
    return {"columns": wrapper.list_columns(name)}


@app.get('/tables/{name}/indexes/')
def list_indexes(name: str):
    return {"indexes": wrapper.list_indexes(name)}


@app.get('/tables/{name}/primarykey/')
def get_primary_key_info(name: str):
    return {"primary key": wrapper.get_primary_key_info(name)}


@app.get('/tables/{name}/foreignkey/')
def get_foreign_keys_info(name: str):
    return {"primary key": wrapper.get_foreign_keys_info(name)}


@app.get('/tables/{name}/items/')
def query(name: str, skip: int = 0, limit: int = Query(default=10, lte=100), order_by: str | None = None, select: str = "*", from_address: str | None = None):
    query_str = "SELECT " + select + " SKIP " + str(skip*limit) + " FROM " + name
    if from_address is not None:
        query_str += (" WHERE from_address = \'" + from_address + "\'")
    if order_by is not None:
        query_str += (" ORDER BY " + order_by)
    query_str += " LIMIT " + str(limit) + ";"
    return {"items": wrapper.query(query_str)}

#Skip, limit, sort (asc/desc), txn_hash?, start/end date, etc


