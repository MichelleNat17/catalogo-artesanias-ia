from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario
from app.forms import LoginForm, RegistroForm, EmailForm, ResetPasswordForm, EditarPerfilForm, CambiarPasswordForm
from app.utils.email import enviar_email_confirmacion, enviar_email_reset

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        if current_user.es_artesana():
            return redirect(url_for('main.dashboard_artesana'))
        else:
            return redirect(url_for('main.catalogo_publico'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        try:
            # Determinar el rol basado en el código de verificación
            rol_final = 'publico'
            if form.codigo_verificacion.data:
                codigos_validos = current_app.config.get('CODIGOS_ARTESANAS', [])
                if form.codigo_verificacion.data.upper() in codigos_validos:
                    rol_final = 'artesana'
            
            nuevo_usuario = Usuario(
                username=form.username.data,
                email=form.email.data,
                rol=rol_final
            )
            nuevo_usuario.set_password(form.password.data)
            nuevo_usuario.generar_token_confirmacion()
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            # Enviar email de confirmación
            enviar_email_confirmacion(nuevo_usuario)
            
            if rol_final == 'artesana':
                flash('¡Registro exitoso como artesana! Se ha enviado un email de confirmación.', 'success')
            else:
                flash('¡Registro exitoso! Se ha enviado un email de confirmación.', 'success')
                
            return redirect(url_for('main.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el usuario. Intenta nuevamente.', 'danger')
    
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.es_artesana():
            return redirect(url_for('main.dashboard_artesana'))
        else:
            return redirect(url_for('main.catalogo_publico'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        if usuario and usuario.check_password(form.password.data):
            if not usuario.email_confirmado:
                flash('Por favor confirma tu email antes de iniciar sesión. Revisa tu bandeja de entrada.', 'warning')
                return redirect(url_for('main.login'))
            
            if usuario.activo:
                login_user(usuario, remember=form.remember_me.data)
                next_page = request.args.get('next')
                
                if usuario.es_artesana():
                    flash(f'¡Bienvenida artesana {usuario.username}!', 'success')
                    return redirect(next_page or url_for('main.dashboard_artesana'))
                else:
                    flash(f'¡Bienvenido {usuario.username}!', 'success')
                    return redirect(next_page or url_for('main.catalogo_publico'))
            else:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
        else:
            flash('Usuario o contraseña incorrectos. Intenta nuevamente.', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))

@main.route('/confirmar-email/<token>')
def confirmar_email(token):
    usuario = Usuario.query.filter_by(token_confirmacion=token).first()
    
    if not usuario:
        flash('El enlace de confirmación es inválido o ha expirado.', 'danger')
        return redirect(url_for('main.index'))
    
    usuario.email_confirmado = True
    usuario.token_confirmacion = None
    db.session.commit()
    
    flash('¡Email confirmado exitosamente! Ya puedes iniciar sesión.', 'success')
    return redirect(url_for('main.login'))

@main.route('/reenviar-confirmacion')
@login_required
def reenviar_confirmacion():
    if current_user.email_confirmado:
        flash('Tu email ya está confirmado.', 'info')
        return redirect(url_for('main.index'))
    
    current_user.generar_token_confirmacion()
    db.session.commit()
    enviar_email_confirmacion(current_user)
    
    flash('Se ha enviado un nuevo email de confirmación a tu correo.', 'success')
    return redirect(url_for('main.perfil'))

@main.route('/olvide-contrasena', methods=['GET', 'POST'])
def olvide_contrasena():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = EmailForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario:
            enviar_email_reset(usuario)
            flash('Se han enviado instrucciones para restablecer tu contraseña a tu email.', 'info')
            return redirect(url_for('main.login'))
        else:
            flash('No existe una cuenta con ese email.', 'danger')
    
    return render_template('olvide_contrasena.html', form=form)

@main.route('/reset-contrasena/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    usuario = Usuario.verificar_token_reset(token)
    if not usuario:
        flash('El enlace es inválido o ha expirado.', 'danger')
        return redirect(url_for('main.olvide_contrasena'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        usuario.set_password(form.password.data)
        db.session.commit()
        
        flash('Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('reset_contrasena.html', form=form)

@main.route('/dashboard-artesana')
@login_required
def dashboard_artesana():
    if not current_user.es_artesana():
        flash('❌ Acceso denegado. Solo las artesanas pueden acceder al dashboard.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('artesanas.html')

@main.route('/catalogo')
def catalogo_publico():
    return render_template('publico.html')

@main.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

# app/routes.py - AGREGAR ESTAS RUTAS NUEVAS

@main.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditarPerfilForm()
    
    # Precargar los datos actuales del usuario
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        try:
            # Verificar si el nuevo username ya existe (y no es el mismo usuario)
            if form.username.data != current_user.username:
                usuario_existente = Usuario.query.filter_by(username=form.username.data).first()
                if usuario_existente:
                    flash('Este usuario ya está en uso. Elige otro.', 'danger')
                    return redirect(url_for('main.editar_perfil'))
            
            # Verificar si el nuevo email ya existe (y no es el mismo usuario)
            if form.email.data != current_user.email:
                email_existente = Usuario.query.filter_by(email=form.email.data).first()
                if email_existente:
                    flash('Este email ya está registrado. Usa otro.', 'danger')
                    return redirect(url_for('main.editar_perfil'))
            
            # Actualizar los datos
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            
            flash('¡Perfil actualizado exitosamente!', 'success')
            return redirect(url_for('main.perfil'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el perfil. Intenta nuevamente.', 'danger')
    
    return render_template('editar_perfil.html', form=form)

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = CambiarPasswordForm()
    
    if form.validate_on_submit():
        try:
            # Verificar que la contraseña actual sea correcta
            if not current_user.check_password(form.password_actual.data):
                flash('La contraseña actual es incorrecta.', 'danger')
                return redirect(url_for('main.cambiar_password'))
            
            # Cambiar la contraseña
            current_user.set_password(form.nueva_password.data)
            db.session.commit()
            
            flash('¡Contraseña cambiada exitosamente!', 'success')
            return redirect(url_for('main.perfil'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al cambiar la contraseña. Intenta nuevamente.', 'danger')
    
    return render_template('cambiar_password.html', form=form)