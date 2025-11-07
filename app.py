import os
import sqlite3
from flask import Flask, request, g, render_template, redirect, url_for, session

# Configuration
DB_PATH = "challenge.db"
SECRET_KEY = os.environ.get("FLASK_SECRET", "dev_secret_for_local_only")
VULNERABLE = os.environ.get("VULNERABLE", "1").lower() in ("1", "true", "yes")

app = Flask(__name__, static_folder="static")
app.secret_key = SECRET_KEY

# Connexion à la base SQLite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g._database = conn
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Page d'accueil (template)
@app.route("/")
def index():
    mode = "VULNÉRABLE" if VULNERABLE else "SÉCURISÉE"
    return render_template("index.html", mode=mode)

# Indique le mode (utile pour le script de test)
@app.route("/mode")
def mode():
    return ("vulnerable" if VULNERABLE else "safe"), 200, {"Content-Type": "text/plain; charset=utf-8"}

# Page /login (GET: formulaire, POST: traitement)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # POST : traiter login
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    db = get_db()
    cursor = db.cursor()

    if VULNERABLE:
        # ---------- VERSION VULNÉRABLE ----------
        # Ici, la requête est construite par concaténation de la chaîne.
        # C'EST DANGEREUX : si `username` contient des fragments SQL, ils seront exécutés.
        # Exemple d'attaque : username = "' OR '1'='1' -- " permettra de contourner l'authentification.
        sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
        except Exception as e:
            # En cas d'erreur SQL, afficher une page d'erreur simple
            return render_template("result.html", status="error",
                                   message=f"Erreur SQL (mode vulnérable) : {e}")
    else:
        # ---------- VERSION SÉCURISÉE ----------
        # Utilisation de requêtes paramétrées (placeholders), qui séparent le code SQL des données.
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        row = cursor.fetchone()

    if row:
        # Authentification réussie : on stocke l'utilisateur en session
        session['user'] = row["username"]
        return render_template("result.html", status="ok",
                               message=f"Authentification réussie. Vous êtes connecté en tant que <strong>{row['username']}</strong>.")
    else:
        return render_template("result.html", status="fail",
                               message="Échec de la connexion. Nom d'utilisateur ou mot de passe incorrect.")

# Route /flag : ne renvoie le flag que si l'utilisateur est 'admin' (connecté)
@app.route("/flag")
def flag():
    user = session.get("user")
    if not user:
        return render_template("flag.html", ok=False, message="Accès refusé : vous devez être connecté.")
    if user != "admin":
        return render_template("flag.html", ok=False, message="Accès refusé : compte non autorisé pour voir le flag.")
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT flag FROM flags LIMIT 1")
    row = cur.fetchone()
    if row:
        return render_template("flag.html", ok=True, flag=row['flag'])
    else:
        return render_template("flag.html", ok=False, message="Aucun flag trouvé.")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
