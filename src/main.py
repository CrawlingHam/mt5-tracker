from src.configs import IS_PRODUCTION, PORT, allowed_origins
from src.middleware import setup_request_logger
from src.routes import register_routes
from flask_cors import CORS
from waitress import serve
from flask import Flask

app = Flask(__name__)
CORS(app, origins=list(allowed_origins), supports_credentials=True)
setup_request_logger(app)
register_routes(app)

if __name__ == "__main__":
    if IS_PRODUCTION:
        serve(app, listen=f"127.0.0.1:{PORT}")
    else:
        app.run(port=PORT, debug=True)