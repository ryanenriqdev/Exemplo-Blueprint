from flask import Flask

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configuração da chave secreta para sessões
app.secret_key = 'chave-secreta-super-segura-123'

# Importa os blueprints
from app.blog import blog_bp
from app.admin import admin_bp

# Registra os blueprints na aplicação
app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)