from flask import Flask
from flask_cors import CORS
from app.routes import register_routes

def create_app():
    app = Flask(__name__)

    CORS(app)

    # 라우트 등록
    register_routes(app)

    return app