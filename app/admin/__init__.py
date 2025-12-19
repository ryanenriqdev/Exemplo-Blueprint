from flask import Blueprint

# Cria o blueprint 'admin'
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Importa as rotas
from . import routes