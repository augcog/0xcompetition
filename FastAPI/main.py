from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return {"message": "Hello World"}

@app.get('/greet/{name}')
def greet_name(name: str):
    return {"greeting": f"Hello {name}"}