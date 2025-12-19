from flask import render_template, request, redirect, url_for, session, flash
from . import admin_bp
from data import posts
from functools import wraps

# Credenciais (apenas para demonstração)
USUARIO_ADMIN = 'admin'
SENHA_ADMIN = '123'

# ========== AUTENTICAÇÃO ==========

def requer_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session:
            flash('Você precisa estar logado.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota: GET/POST /admin/login
    Exibe formulário e processa autenticação.
    """
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == USUARIO_ADMIN and senha == SENHA_ADMIN:
            session['usuario_logado'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'error')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """
    Rota: GET /admin/logout
    Remove usuário da sessão.
    """
    session.pop('usuario_logado', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('blog.index'))

# ========== CRUD ==========

@admin_bp.route('/dashboard')
@requer_login
def dashboard():
    """
    Rota: GET /admin/dashboard
    Exibe painel com lista de posts.
    """
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('admin.login'))

    return render_template('admin/dashboard.html', posts=posts)

@admin_bp.route('/novo', methods=['GET', 'POST'])
@requer_login
def novo_post():
    """
    Rota: GET/POST /admin/novo
    Cria nova postagem.
    """
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        # Gera novo ID
        novo_id = max([p['id'] for p in posts], default=0) + 1

        # Cria novo post
        novo = {
            'id': novo_id,
            'titulo': request.form.get('titulo'),
            'conteudo': request.form.get('conteudo'),
            'autor': session['usuario_logado']
        }

        posts.append(novo)
        flash('Postagem criada com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/new_post.html')

@admin_bp.route('/editar/<int:post_id>', methods=['GET', 'POST'])
@requer_login
def editar_post(post_id):
    """
    Rota: GET/POST /admin/editar/<id>
    Edita postagem existente.
    """
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('admin.login'))

    # Busca o post
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        flash('Postagem não encontrada.', 'error')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        post['titulo'] = request.form.get('titulo')
        post['conteudo'] = request.form.get('conteudo')
        flash('Postagem atualizada com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_post.html', post=post)

@admin_bp.route('/deletar/<int:post_id>')
@requer_login
def deletar_post(post_id):
    """
    Rota: GET /admin/deletar/<id>
    Deleta uma postagem.
    """
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('admin.login'))

    # Remove post da lista
    global posts
    posts = [p for p in posts if p['id'] != post_id]

    flash('Postagem deletada com sucesso!', 'success')
    return redirect(url_for('admin.dashboard'))