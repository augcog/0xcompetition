import requests

params = {
    "q": "SELECT * FROM transactions WHERE from_address='0x804d39f546c5164af7612c3dca3683150e55bb78' ORDER BY transaction_index DESC"
}
ip = "128.32.43.220"
r = requests.get(f"http://{ip}:8000/query", params=params)
print(r.status_code)
print(r.json()["result"]["to_address"]['0'])
