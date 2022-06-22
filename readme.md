# 0x competition Server code

## Quick Start
1. clone this repo
   1. `git clone `
2. install requirements
3. get `settings.json` from administrator and put it under `config` folder
4. set environment variable:
   1. `export COMP_SETTING="YOUR_PATH_HERE"`
5. Start server by executing `python main.py`
6. test server by using `python client_example.py`


## Testing
Run `pytest -c pytest_env.ini --cov=v1`, revise the `ini` file as needed

