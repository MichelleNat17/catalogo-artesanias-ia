from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(20), nullable=False, default='publico')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # CAMPOS PARA VERIFICACIÓN DE EMAIL
    email_confirmado = db.Column(db.Boolean, default=False)
    token_confirmacion = db.Column(db.String(100), unique=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def es_artesana(self):
        return self.rol == 'artesana'
    
    def generar_token_confirmacion(self):
        self.token_confirmacion = secrets.token_urlsafe(32)
        return self.token_confirmacion
    
    def generar_token_reset(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verificar_token_reset(token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
            user_id = data.get('user_id')
            return Usuario.query.get(user_id)
        except:
            return None
    
    def __repr__(self):
        return f'<Usuario {self.username} - {self.rol}>'

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))