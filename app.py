

from flask_migrate import Migrate
from models.User import User
from config import app, db
from flask_login import LoginManager
# Flask-Migrate for database migrations
migrate = Migrate(app, db)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

login_manager=LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

import routes
