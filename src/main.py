from src.configs import IS_PRODUCTION, PORT, allowed_origins
from src.middleware import setup_request_logger
from src.routes import register_routes
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app, origins=list(allowed_origins))
setup_request_logger(app)
register_routes(app)

if __name__ == "__main__":
    app.run(port=PORT, debug=not IS_PRODUCTION)