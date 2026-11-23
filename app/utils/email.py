from flask_mail import Message
from flask import render_template, current_app
from app import mail

def enviar_email(destinatario, asunto, template, **kwargs):
    msg = Message(
        asunto,
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[destinatario]
    )
    msg.body = render_template(f'emails/{template}.txt', **kwargs)
    msg.html = render_template(f'emails/{template}.html', **kwargs)
    mail.send(msg)

def enviar_email_confirmacion(usuario):
    token = usuario.generar_token_confirmacion()
    enviar_email(
        usuario.email,
        'Confirma tu cuenta - Catálogo Artesanías',
        'confirmar_cuenta',
        usuario=usuario,
        token=token
    )

def enviar_email_reset(usuario):
    token = usuario.generar_token_reset()
    enviar_email(
        usuario.email,
        'Restablecer tu contraseña - Catálogo Artesanías',
        'reset_password',
        usuario=usuario,
        token=token
    )