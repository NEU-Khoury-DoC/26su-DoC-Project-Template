from flask import Flask
from dotenv import load_dotenv
import os
import logging

from backend.db_connection import init_app as init_db
from backend.simple.simple_routes import simple_routes
from backend.ngos.ngo_routes import ngo_bp
from backend.farms.farm_routes import farms_bp
from backend.users.user_routes import users_bp
from backend.posts.posts_routes import posts_bp
from backend.comments.comments_routes import comments_bp
from backend.reactions.reactions_routes import reactions_bp
from backend.farm_location.farm_loc_routs import farms_loc_bp
from backend.user_growing_data.user_growing_route import user_growing_bp
from backend.prices_model_routing.prices_route import price_bp
from backend.model_routes.cropknnmd_01 import crop_routes



def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    # Load environment variables from the .env file so they are
    # accessible via os.getenv() below.
    load_dotenv()

    # Secret key used by Flask for securely signing session cookies.
    # .strip() removes accidental leading/trailing whitespace from .env values.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY").strip()

    # Database connection settings — values come from the .env file.
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME").strip()

    # Register the cleanup hook for the database connection.
    app.logger.info("create_app(): initializing database connection")
    init_db(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each.
    # simple_routes has no prefix intentionally — it serves root-level demo routes (/, /playlist, etc.)
    app.logger.info("create_app(): registering blueprints")
    app.register_blueprint(simple_routes)
    app.register_blueprint(ngo_bp, url_prefix="/ngo")
    app.register_blueprint(farms_bp, url_prefix="/farms")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(comments_bp, url_prefix="/comments")
    app.register_blueprint(reactions_bp, url_prefix="/reactions")
    app.register_blueprint(price_bp, url_prefix="/prices_model")
    app.register_blueprint(crop_routes, url_prefix="/crop")
    app.register_blueprint(farms_loc_bp, url_prefix="/farm_loc")
    app.register_blueprint(user_growing_bp, url_prefix="/user_growing")

    return app
