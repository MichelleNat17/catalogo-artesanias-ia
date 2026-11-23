from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models import Usuario

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()], 
                          render_kw={"placeholder": "Ingresa tu usuario"})
    password = PasswordField('Contraseña', validators=[DataRequired()], 
                            render_kw={"placeholder": "Ingresa tu contraseña"})
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión', render_kw={"class": "btn btn-primary w-100"})

class RegistroForm(FlaskForm):
    username = StringField('Usuario', 
                          validators=[DataRequired(), Length(min=4, max=80)],
                          render_kw={"placeholder": "Crea un nombre de usuario"})
    email = StringField('Email', 
                       validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "tu@email.com"})
    password = PasswordField('Contraseña', 
                            validators=[DataRequired(), Length(min=6)],
                            render_kw={"placeholder": "Mínimo 6 caracteres"})
    confirm_password = PasswordField('Confirmar Contraseña', 
                                   validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')],
                                   render_kw={"placeholder": "Repite tu contraseña"})
    rol = SelectField('Tipo de Usuario', 
                     choices=[('publico', ' Público - Solo ver catálogo')],  # SOLO PÚBLICO POR DEFECTO
                     validators=[DataRequired()])
    
    # NUEVO CAMPO: Código de verificación para artesanas
    codigo_verificacion = StringField('Código de Artesana (Opcional)',
                                     validators=[Optional()],
                                     render_kw={"placeholder": "Solo si eres artesana de Loma Alta"})
    
    submit = SubmitField('Registrarse', render_kw={"class": "btn btn-success w-100"})
    
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Este usuario ya está registrado. Elige otro.')
    
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email ya está registrado.')
    
    # NUEVA VALIDACIÓN: Verificar código de artesana
    def validate_codigo_verificacion(self, codigo_verificacion):
        if codigo_verificacion.data:  # Si ingresó un código
            codigos_validos = ['ARTESANA2024', 'LOMAALTA', 'PAJATOQUILLA', 'MANOSMAESTRAS']
            if codigo_verificacion.data.upper() not in codigos_validos:
                raise ValidationError('Código de artesana inválido.')
            else:
                # Si el código es válido, cambiar el rol a artesana
                self.rol.data = 'artesana'

class EmailForm(FlaskForm):
    email = StringField('Email', 
                       validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "Ingresa tu email registrado"})
    submit = SubmitField('Enviar Instrucciones', render_kw={"class": "btn btn-primary w-100"})

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', 
                            validators=[DataRequired(), Length(min=6)],
                            render_kw={"placeholder": "Mínimo 6 caracteres"})
    confirm_password = PasswordField('Confirmar Nueva Contraseña', 
                                   validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')],
                                   render_kw={"placeholder": "Repite tu nueva contraseña"})
    submit = SubmitField('Cambiar Contraseña', render_kw={"class": "btn btn-success w-100"})


class EditarPerfilForm(FlaskForm):
    username = StringField('Usuario', 
                          validators=[DataRequired(), Length(min=4, max=80)],
                          render_kw={"placeholder": "Tu nombre de usuario"})
    email = StringField('Email', 
                       validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "tu@email.com"})
    submit = SubmitField('Actualizar Perfil', render_kw={"class": "btn btn-primary w-100"})

class CambiarPasswordForm(FlaskForm):
    password_actual = PasswordField('Contraseña Actual', 
                                   validators=[DataRequired()],
                                   render_kw={"placeholder": "Ingresa tu contraseña actual"})
    nueva_password = PasswordField('Nueva Contraseña', 
                                  validators=[DataRequired(), Length(min=6)],
                                  render_kw={"placeholder": "Mínimo 6 caracteres"})
    confirmar_password = PasswordField('Confirmar Nueva Contraseña', 
                                      validators=[DataRequired(), EqualTo('nueva_password', message='Las contraseñas deben coincidir')],
                                      render_kw={"placeholder": "Repite tu nueva contraseña"})
    submit = SubmitField('Cambiar Contraseña', render_kw={"class": "btn btn-warning w-100"})