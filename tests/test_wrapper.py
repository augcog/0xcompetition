from v1.utils.block_db_sql_wrapper import BlockDBSQLWrapper
import pytest
import os


def test_init_not_none():
    with pytest.raises(AssertionError):
        block_db_sql_wrapper = BlockDBSQLWrapper(file_path=None)


def test_init_exists():
    fp = "config/me.json"
    with pytest.raises(AssertionError):
        block_db_sql_wrapper = BlockDBSQLWrapper(file_path=fp)


def test_list_tables():
    fp = os.getenv("COMP_SETTING")
    bdb = BlockDBSQLWrapper(file_path=fp)
    assert bdb.list_tables() == ["transactions", "blocks"]


def test_list_columns():
    fp = os.getenv("COMP_SETTING")
    bdb = BlockDBSQLWrapper(file_path=fp)
    assert bdb.list_columns("transactions") == ["hash", "nonce", "block_hash", "block_number", "transaction_index",
                                           "from_address", "to_address", "value", "gas", "gas_price", "input",
                                           "block_timestamp", "max_fee_per_gas", "max_priority_fee_per_gas",
                                           "transaction_type", "receipt_cumulative_gas_used", "receipt_gas_used",
                                           "receipt_contract_address", "receipt_root", "receipt_status",
                                           "receipt_effective_gas_price"]


def test_list_indexes():
    fp = os.getenv("COMP_SETTING")
    bdb = BlockDBSQLWrapper(file_path=fp)
    assert bdb.list_indexes("transactions") == ["transactions_block_timestamp_index",
                                           "transactions_from_address_block_timestamp_index",
                                           "transactions_to_address_block_timestamp_index"]


def test_get_primary_key_info():
    fp = os.getenv("COMP_SETTING")
    bdb = BlockDBSQLWrapper(file_path=fp)
    assert bdb.get_primary_key_info("transactions") == ["constrained_columns", "name"]


def test_get_foreign_key_info():
    fp = os.getenv("COMP_SETTING")
    bdb = BlockDBSQLWrapper(file_path=fp)
    assert bdb.get_foreign_keys_info("transactions") == []

