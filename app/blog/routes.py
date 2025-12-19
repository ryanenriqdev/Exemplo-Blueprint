from flask import render_template
from . import blog_bp
from data import posts

@blog_bp.route('/')
def index():
    """
    Rota: GET /
    Renderiza a página inicial do blog com todos os posts.
    """
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/post/<int:post_id>')
def post(post_id):
    """
    Rota: GET /post/<id>
    Renderiza a página de um post específico.
    """
    # Busca o post com o ID especificado
    post = next((p for p in posts if p['id'] == post_id), None)
    return render_template('blog/post.html', post=post)