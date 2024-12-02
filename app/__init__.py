from flask import Flask
from app.config import Config
from app.services.llm_handler import LLMHandler
from app.services.solution_runner import SolutionRunner
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = LLMHandler()
runner = SolutionRunner()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    logger.info("🌟 AoC 2024 Solution Generator initialized")
    return app 