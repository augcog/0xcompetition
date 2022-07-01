from fastapi.testclient import TestClient
from v1.api import app

client = TestClient(app)


def test_list_tables():
    response = client.get("/tables")
    assert response.json() == {
        "tables": ["transactions", "blocks"]
    }


def test_list_columns():
    response = client.get("/tables/transactions/columns/")
    assert response.json() == {"table_name": "transactions",
                               "columns": ["hash", "nonce", "block_hash", "block_number", "transaction_index",
                                           "from_address", "to_address", "value", "gas", "gas_price", "input",
                                           "block_timestamp", "max_fee_per_gas", "max_priority_fee_per_gas",
                                           "transaction_type", "receipt_cumulative_gas_used", "receipt_gas_used",
                                           "receipt_contract_address", "receipt_root", "receipt_status",
                                           "receipt_effective_gas_price"]}


def test_query():
    params = {
        "q": "SELECT * FROM transaction WHERE from_address='0x804d39f546c5164af7612c3dca3683150e55bb78' ORDER BY transaction_index DESC"
    }  # wrong table name
    response = client.get("/query", params=params)
    assert response.status_code == 500

    params = {
        "q": "SELECT * FROM transactions WHERE from_address='0x804d39f546c5164af7612c3dca3683150e55bb78' ORDER BY transaction_index DESC"
    }  # wrong table name
    r = client.get("/query", params=params)
    result = r.json()["result"]
    assert len(result["hash"]) == 2

    assert result["hash"]['0'] == '0xf5a0e1a792783a8057d73b8f00c854576fb22027c7a62d14ab8d82f1e9dabd17'
    assert result["from_address"]["0"] == '0x804d39f546c5164af7612c3dca3683150e55bb78'
    assert result['to_address']['0'] == '0xf23b127ff5a6a8b60cc4cbf937e5683315894dda'

# TODO @WINSON, keep writing tests
