from flask import Flask
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)


@app.route("/")
def root():
    return "Hello From Flask!"


asgi_app = WsgiToAsgi(app)

# if __name__ == "__main__":
#     app.run(
#         debug=True,
#         port=5001,
#         host="0.0.0.0",
#         ssl_context=(
#             r"C:\ssl\quicktranslate.online-chain.pem",   # certificate (or fullchain)
#             r"C:\ssl\quicktranslate.online-key.pem"    # private key
#         )
#     )
