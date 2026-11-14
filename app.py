import os, sqlite3
from functools import wraps
from flask import Flask, request, jsonify, Response, send_from_directory
from werkzeug.security import check_password_hash

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, "blessings.sqlite3")
app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

with db() as con:
    con.execute("""CREATE TABLE IF NOT EXISTS blessings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")

@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@app.post("/api/blessings")
def add_blessing():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    message = str(data.get("message", "")).strip()
    if not name or not message:
        return jsonify(error="Name and message are required."), 400
    if len(name) > 80:
        return jsonify(error="Name must be 80 characters or fewer."), 400
    if len(message) > 500:
        return jsonify(error="Message must be 500 characters or fewer."), 400
    with db() as con:
        cur = con.execute("INSERT INTO blessings(name,message) VALUES(?,?)", (name, message))
        blessing_id = cur.lastrowid
    return jsonify(ok=True, id=blessing_id), 201

def couple_auth(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        username = os.environ.get("COUPLE_USERNAME", "couple")
        password_hash = os.environ.get("COUPLE_PASSWORD_HASH")
        password = os.environ.get("COUPLE_PASSWORD")
        auth = request.authorization
        if not auth or auth.username != username or not (
            (password_hash and check_password_hash(password_hash, auth.password))
            or (password and auth.password == password)
        ):
            return Response("Couple access only. Sign in with your private credentials.",
                401, {"WWW-Authenticate": 'Basic realm="Priya & Souvik private blessings"'})
        return fn(*args, **kwargs)
    return wrapped

@app.get("/private")
@couple_auth
def private_page():
    return send_from_directory(ROOT, "private.html")

@app.get("/api/private/blessings")
@couple_auth
def all_blessings():
    with db() as con:
        rows = con.execute("SELECT id,name,message,created_at FROM blessings ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=False)
