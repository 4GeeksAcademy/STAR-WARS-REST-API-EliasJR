import os
from flask_admin import Admin
from models import db, User, Character, Planet, Starship, FavoriteItem
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    # Configurar la clave secreta para la aplicación
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    # Configurar Flask-Admin
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Añadir las vistas de los modelos al panel de administración
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Starship, db.session))
    admin.add_view(ModelView(FavoriteItem, db.session))

