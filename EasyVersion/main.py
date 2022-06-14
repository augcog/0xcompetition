from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from competition_sql_wrapper import *

if __name__ == "__main__":
    fp = "./settings.json"
    wrapper = CompetitionSQLWrapper(file_path=fp)
    print(wrapper.list_tables())
    print(wrapper.list_columns("transactions"))
    print(wrapper.list_indexes("transactions"))

