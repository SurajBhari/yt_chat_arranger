from flask import Flask, request
from json import dump, dumps

app = Flask(__name__)


@app.get("/")
def testing():
    print("\n\n\n")
    print(request.headers)
    print("\n\n\n")
    print(request.headers["Nightbot-User"])
    print("\n\n\n")
    print(request.headers["Nightbot-Channel"])
    print(type(request.headers))
    return "hello world suprise"


app.run(port=5000, debug=True, host="0.0.0.0")
