from flask import Flask
from flask_login import LoginManager 
import databases.models as models
from forms import *
from dotenv import load_dotenv
import os 
from databases.base import db
from routes.mainRoutes import main_bp 
from routes.vendorRoutes import vendor_bp
from routes.userRoutes import user_bp
from routes.itemRoutes import item_bp
from routes.itemCategoryRoutes import itemCategory_bp
from routes.authRoutes import auth_bp
from databases.createDatabase import createDatabase

def create_app(config=None):
    app = Flask(__name__)
    load_dotenv()
    if config:
        app.config.update(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///E-Waste-Tracker.db"
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    createDatabase(app)

    loginManager = LoginManager()
    loginManager.init_app(app)
    loginManager.login_view = "auth.login"
  

    @loginManager.user_loader
    def loadUser(userID):
        try:
            return models.User.query.filter(models.User.userID ==userID, models.User.isDeleted == False).first()
        except Exception as e:
            return None
        
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(vendor_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(itemCategory_bp)
    return app

app = create_app()
