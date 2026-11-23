from app import create_app, db

app = create_app()

# Elimina la línea con @app.before_first_request y usa esto:
with app.app_context():
    db.create_all()  # Crear tablas al iniciar

if __name__ == '__main__':
    app.run(debug=True)