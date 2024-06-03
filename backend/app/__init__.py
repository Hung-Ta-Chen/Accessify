from flask import Flask, jsonify
from .config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from pymongo import MongoClient
import logging

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    logging.basicConfig(level=logging.INFO)

    CORS(app, resources={r"/api/*": {"origins": "*"}})  # for cross platform
    CORS(app, resources={r"/chatbot/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize MongoDB connection
    app.mongo_db = MongoClient(app.config['MONGO_URI'])['accessify_db']

    from .places.routes import place_blueprint, review_blueprint
    app.register_blueprint(place_blueprint, url_prefix='/api')
    app.register_blueprint(review_blueprint, url_prefix='/api')

    from .chatbot.routes import chatbot_blueprint
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')

    # Global error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found', 'message': str(error)}), 404

    app.logger.info('Application has started')

    return app
