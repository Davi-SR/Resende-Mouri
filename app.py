import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, abort, jsonify
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

app = Flask(__name__, template_folder='.', static_folder='.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                original_filename TEXT NOT NULL,
                stored_filename TEXT NOT NULL,
                uploaded_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
            )
            """
        )


@app.before_request
def _ensure_db():
    init_db()


def allowed_file(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


@app.get('/')
def index():
    with get_db() as conn:
        docs = conn.execute(
            'SELECT id, title, uploaded_at FROM documents ORDER BY datetime(uploaded_at) DESC'
        ).fetchall()
    return render_template('index.html', documents=docs)


@app.post('/upload')
def upload():
    title = (request.form.get('title') or '').strip()
    description = (request.form.get('description') or '').strip()
    file = request.files.get('file')

    if not title:
        return redirect(url_for('index', error='Título é obrigatório.'))
    if not file or file.filename == '':
        return redirect(url_for('index', error='Selecione um arquivo.'))

    original_filename = secure_filename(file.filename)
    if not allowed_file(original_filename):
        return redirect(url_for('index', error='Formato inválido. Use PDF, JPG ou PNG.'))

    uploaded_at = datetime.utcnow().isoformat(timespec='seconds') + 'Z'

    name, ext = os.path.splitext(original_filename)
    safe_name = name[:60] if name else 'document'
    stored_filename = f"{safe_name}_{int(datetime.utcnow().timestamp())}{ext.lower()}"

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
    file.save(save_path)

    with get_db() as conn:
        cur = conn.execute(
            'INSERT INTO documents (title, description, original_filename, stored_filename, uploaded_at) VALUES (?, ?, ?, ?, ?)',
            (title, description or None, original_filename, stored_filename, uploaded_at)
        )
        doc_id = cur.lastrowid

    return redirect(url_for('document_detail', doc_id=doc_id))


@app.get('/documents/<int:doc_id>')
def document_detail(doc_id):
    with get_db() as conn:
        doc = conn.execute('SELECT * FROM documents WHERE id = ?', (doc_id,)).fetchone()
        if not doc:
            abort(404)
        comments = conn.execute(
            'SELECT * FROM comments WHERE document_id = ? ORDER BY datetime(created_at) DESC',
            (doc_id,)
        ).fetchall()

    return render_template('document.html', document=doc, comments=comments)


@app.post('/documents/<int:doc_id>/comments')
def add_comment(doc_id):
    content = (request.form.get('content') or '').strip()
    if not content:
        return redirect(url_for('document_detail', doc_id=doc_id))

    created_at = datetime.utcnow().isoformat(timespec='seconds') + 'Z'

    with get_db() as conn:
        doc = conn.execute('SELECT id FROM documents WHERE id = ?', (doc_id,)).fetchone()
        if not doc:
            abort(404)
        conn.execute(
            'INSERT INTO comments (document_id, content, created_at) VALUES (?, ?, ?)',
            (doc_id, content, created_at)
        )

    return redirect(url_for('document_detail', doc_id=doc_id))


@app.get('/files/<path:stored_filename>')
def download_file(stored_filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
    return send_file(file_path, as_attachment=True)


@app.get('/api/documents')
def api_documents():
    with get_db() as conn:
        docs = conn.execute('SELECT id, title, description, uploaded_at, original_filename, stored_filename FROM documents ORDER BY datetime(uploaded_at) DESC').fetchall()
    return jsonify([dict(r) for r in docs])


@app.get('/api/documents/<int:doc_id>/comments')
def api_comments(doc_id):
    with get_db() as conn:
        comments = conn.execute('SELECT id, document_id, content, created_at FROM comments WHERE document_id = ? ORDER BY datetime(created_at) DESC', (doc_id,)).fetchall()
    return jsonify([dict(r) for r in comments])


@app.route('/styles.css')
def serve_css():
    return send_file('styles.css', mimetype='text/css')

@app.route('/app.js')
def serve_js():
    return send_file('app.js', mimetype='application/javascript')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
