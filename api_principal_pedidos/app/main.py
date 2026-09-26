from flask import Flask
from flasgger import Swagger
from app.database.db_config import init_db
from app.routes.pedido_routes import pedido_bp

def create_app():
    app = Flask(__name__)
    
    # Inicializa o Swagger com configurações básicas
    app.config['SWAGGER'] = {
        'title': 'API Principal - Pedidos',
        'uiversion': 3
    }
    Swagger(app)
    
    init_db()
    app.register_blueprint(pedido_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)