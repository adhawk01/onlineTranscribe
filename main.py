from flask import Flask

app = Flask(__name__)


@app.route("/")
def root():
    return "Hello From Flask!"


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
