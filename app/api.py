from flask import Flask, jsonify

from app.database import transactions

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/api/node/<node_ip>")
def get_node(node_ip):
    node = transactions.node_to_dict(node_ip)
    return jsonify(node)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
