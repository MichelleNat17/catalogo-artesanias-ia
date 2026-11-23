from app import create_app, db
from app.models import Usuario

def init_database():
    app = create_app()
    
    with app.app_context():
        # Eliminar todas las tablas existentes
        db.drop_all()
        
        # Crear todas las tablas con los nuevos campos
        db.create_all()
        
        # Opcional: Crear un usuario de prueba
        try:
            usuario_prueba = Usuario(
                username='artesana_prueba',
                email='prueba@artesanas.com',
                rol='artesana'
            )
            usuario_prueba.set_password('password123')
            usuario_prueba.email_confirmado = True
            
            db.session.add(usuario_prueba)
            db.session.commit()
            print("   Base de datos creada exitosamente!")
            print("   Usuario de prueba creado:")
            print("   Usuario: artesana_prueba")
            print("   Contraseña: password123")
            print("   Rol: artesana")
            
        except Exception as e:
            print(f" Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_database()