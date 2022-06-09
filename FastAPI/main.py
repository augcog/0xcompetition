from fastapi import FastAPI
from EasyVersion import competition_sql_wrapper
import json


app = FastAPI()


@app.get('/')
def index():
    return {"message": "Hello World"}

@app.get('/tables/')
def greet_name(name: str):
    fp = "./settings.json"
    wrapper = competition_sql_wrapper.CompetitionSQLWrapper(file_path=fp)
    tables = json.dumps(wrapper.list_tables())
    return {"tables": tables}
