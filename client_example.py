import requests

params = {
    "q": "SELECT * FROM transactions WHERE from_address='0x804d39f546c5164af7612c3dca3683150e55bb78' ORDER BY transaction_index DESC"
}
r = requests.get(f"http://127.0.0.1:8000/query", params=params)
print(r.status_code)
print(r.json()["result"]["to_address"]['0'])
