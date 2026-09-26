from flask import Flask
from flasgger import Swagger
from app.database.db_config import init_db
from app.routes.frete_routes import frete_bp

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'API Secundária - Logística e Frete',
        'uiversion': 3
    }
    Swagger(app)
    
    init_db()
    app.register_blueprint(frete_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)