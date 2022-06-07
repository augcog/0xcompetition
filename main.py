from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from competition_sql_wrapper import *

if __name__ == "__main__":
    fp = "./settings.json"
    competition_sql_wrapper = CompetitionSQLWrapper(file_path=fp)

