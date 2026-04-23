from flask import Flask
from extensions import db, login_manager, mail
from models import Usuario
from routes.auth import auth
from routes.finanzas import finanzas
from routes.usuario import usuario
from routes.extras import extras

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave_secreta_123'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'martinezmestrajuanpablo7@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wxpf lxqu slti jidv'
    app.config['VAPID_PUBLIC_KEY'] = '0x000001D2308BF450'
    app.config['VAPID_PRIVATE_KEY'] = '0x000001D2302E5C50'
    app.config['VAPID_CLAIM_EMAIL'] = 'martinezmestrajuanpablo7@gmail.com'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.context_processor
    def inject_moneda():
        from flask_login import current_user
        if current_user and current_user.is_authenticated:
            return dict(moneda=current_user.moneda)
        return dict(moneda='$')

    app.register_blueprint(auth)
    app.register_blueprint(finanzas)
    app.register_blueprint(usuario)
    app.register_blueprint(extras)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

@app.route('/landing')
def landing():
    from flask import render_template
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(debug=True)