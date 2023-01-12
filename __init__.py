from flask import Flask
from flask_login import LoginManager
from .models import User, map_user_db_to_domain
import pymongo


client = pymongo.MongoClient('localhost', 27017)
db = client['Mongo']
users_collection = db['users']

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "secretsauce"

    from blog.models import User
    from blog.pages import pages
    from blog.authentication import authentication

    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(authentication, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(_id):
        user_data = users_collection.find_one({'_id': _id})
        if user_data:
            return map_user_db_to_domain(user_data)
        return None

    return app
