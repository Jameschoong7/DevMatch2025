from flask import Flask, jsonify, request
from blockchain import contract


app = Flask(__name__)


@app.route('/')
def index():
    return "GreenChain Flask backend is running" 

#Other endpoint (claim_token, etc..)


if __name__=="__main__":
    app.run(debug=True)
