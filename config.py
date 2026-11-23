import os

class Config:
    SECRET_KEY = 'clave123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///catalogo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de email (USAR TUS DATOS REALES)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'natalyiot34@gmail.com'  # TU EMAIL
    MAIL_PASSWORD = 'yrbe cpjr eqdi aemp'  #  CONTRASEÑA DE APLICACIÓN
    MAIL_DEFAULT_SENDER = 'natalyiot34@gmail.com'

    # Códigos de verificación para artesanas
    CODIGOS_ARTESANAS = ['ARTESANA2025', 'LOMAALTA', 'PAJATOQUILLA', 'MANOSMAESTRAS']