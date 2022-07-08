from v1.utils.block_db_sql_wrapper import BlockDBSQLWrapper


def test_init():
    fp = "config/settings.json"
    try:
        block_db_sql_wrapper = BlockDBSQLWrapper(file_path=fp)
    except Exception as e:
        raise Exception(f"Error: \'{e}\'")