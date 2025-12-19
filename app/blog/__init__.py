from flask import Blueprint

# Cria o blueprint 'blog'
blog_bp = Blueprint('blog', __name__, template_folder='templates')

# Importa as rotas
from . import routes