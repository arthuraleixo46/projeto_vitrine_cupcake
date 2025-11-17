import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from mongo_manager import MongoManager
from bson import ObjectId

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('FLASK_SECRET', 'dev-secret-change-me')

md = MongoManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    cupcakes = md.get_cupcakes()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/product/<id>')
def product_detail(id):
    cupcake = md.get_cupcake(id)
    if not cupcake:
        return redirect(url_for('index'))
    return render_template('product.html', cupcake=cupcake)

# ------------ AUTENTICAÇÃO -------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = md.find_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['admin_id'] = str(user['_id'])
            session['admin_email'] = user['email']
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('admin_login'))

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Faça login como administrador.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper

# ------------ DASHBOARD DA ÁREA ADMIN -------------
@app.route('/admin')
@admin_required
def admin_dashboard():
    cupcakes = md.get_cupcakes()
    return render_template('admin_dashboard.html', cupcakes=cupcakes)

@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def admin_add():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sabor = request.form.get('sabor')
        price = request.form.get('price')
        image_url = request.form.get('image_url', '').strip()
        image_file = request.files.get('image_file')

        stored_path = ''
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(save_path)
            stored_path = '/static/uploads/' + filename
        elif image_url:
            stored_path = image_url
        else:
            stored_path = '/static/uploads/placeholder.png'

        if nome and sabor and price:
            md.add_cupcake({
                'nome': nome,
                'sabor': sabor,
                'price': float(price),
                'image': stored_path
            })
            flash('Cupcake adicionado.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Preencha todos os campos obrigatórios.', 'warning')
    return render_template('admin_add.html')

@app.route('/admin/edit/<id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(id):
    cupcake = md.get_cupcake(id)
    if not cupcake:
        flash('Cupcake não encontrado.', 'danger')
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        sabor = request.form.get('sabor')
        price = request.form.get('price')
        image_url = request.form.get('image_url', '').strip()
        image_file = request.files.get('image_file')

        stored_path = cupcake.get('image', '/static/uploads/placeholder.png')
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(save_path)
            stored_path = '/static/uploads/' + filename
        elif image_url:
            stored_path = image_url

        md.update_cupcake(id, {
            'nome': nome,
            'sabor': sabor,
            'price': float(price),
            'image': stored_path
        })
        flash('Cupcake atualizado.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', cupcake=cupcake)

@app.route('/admin/delete/<id>', methods=['POST'])
@admin_required
def admin_delete(id):
    md.delete_cupcake(id)
    flash('Cupcake removido.', 'info')
    return redirect(url_for('admin_dashboard'))

# ------------ ROTA DE UPLOADS -------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) # Força a existência da pasta uploads
    app.run(debug=True)
