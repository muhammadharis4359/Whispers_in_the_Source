from flask import Flask, request, render_template, redirect, session, jsonify
import sqlite3
import os
import secrets
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DB = "blackpearl.db"
FLAG = "SAVVY{br0w53r_15_n0t_l0y4l}"

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crew (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'sailor',
            access_code TEXT
        )
    """)
    
    # Notes table (crew logs)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            is_private INTEGER DEFAULT 0
        )
    """)
    
    # Clear existing data
    cur.execute("DELETE FROM crew")
    cur.execute("DELETE FROM notes")
    
    # Add crew members with various roles
    cur.execute("INSERT INTO crew VALUES (1, 'jack_sparrow', 'rumrunner', 'captain', 'PEARL')")
    cur.execute("INSERT INTO crew VALUES (2, 'will_turner', 'elizabeth', 'officer', 'COMP')")
    cur.execute("INSERT INTO crew VALUES (3, 'joshamee', 'cotton_parrot', 'quartermaster', 'PASS')")
    # cur.execute("INSERT INTO crew VALUES (4, 'deckhand_tom', 'anchor123', 'sailor', None)")
    
    # Add notes with clues
    cur.execute("""INSERT INTO notes VALUES 
        (1, 1, 'Captain''s Log - Entry 47', 
        'The old authentication system was flawed. We moved everything to the client for speed. The crew doesn''t need to know this.', 0)""")
    
    cur.execute("""INSERT INTO notes VALUES 
        (2, 2, 'Officer Report', 
        'Found something odd: access decisions happen in the browser, not the server. Fragment 1 of access code: PEARL__', 1)""")
    
    cur.execute("""INSERT INTO notes VALUES 
        (3, 3, 'Quartermaster Notes', 
        'The vault system checks roles locally. I suspect anyone can pretend. Fragment 2: COMP__@SS', 1)""")
    
    cur.execute("""INSERT INTO notes VALUES 
        (4, 4, 'Sailor''s Diary', 
        'Overheard the officers talking about a master phrase Fragment 3: C0d3', 0)""")
    
    cur.execute("""INSERT INTO notes VALUES 
        (5, 1, 'Hidden Navigation Chart', 
        'The final chamber requires the phrase. Only those who read between them find /vault/final', 1)""")
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query, args).fetchall()
    conn.commit()
    conn.close()
    return (result[0] if result else None) if one else result

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """
    Fake login - server doesn't actually validate
    This is intentional! Client-side JS does the real work
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    
    # Server just returns success for ANY input
    # The real validation happens in JavaScript (vulnerability!)
    return jsonify({"success": True, "message": "Credentials accepted"})

@app.route("/dashboard")
def dashboard():
    # No real session check!
    # Client-side JS controls access
    return render_template("dashboard.html")

@app.route("/admin")
def admin():
    # No server-side role verification!
    # This page is "protected" only by client-side JavaScript
    return render_template("admin.html")

@app.route("/notes")
def notes():
    # Returns ALL notes without proper access control
    # Client is supposed to filter, but that's insecure!
    all_notes = query_db("SELECT * FROM notes")
    return render_template("notes.html", notes=all_notes)

@app.route("/api/notes/<int:user_id>")
def api_notes(user_id):
    """
    API endpoint that returns notes for a specific user
    No authentication check! Client-side vulnerability
    """
    notes = query_db("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    return jsonify([dict(note) for note in notes])

@app.route("/vault")
def vault():
    # Another fake protected page
    return render_template("vault.html")

@app.route("/vault/final")
def vault_final():
    """
    The final chamber - requires discovering the hidden endpoint
    """
    # Check if they figured out the access code
    code = request.args.get("code", "")
    
    if code.upper() == "PEARLCOMPASSCODE":
        return render_template("success.html", flag=FLAG)
    else:
        return render_template("vault_locked.html")

@app.route("/api/validate")
def api_validate():
    """
    Fake validation endpoint that always returns true
    Shows that server doesn't actually validate anything
    """
    return jsonify({"valid": True, "role": "admin", "message": "Client decides everything"})

@app.route("/static/auth.js")
def auth_js():
    """
    Serve the vulnerable authentication JavaScript
    This is where players will find the client-side logic
    """
    return render_template("auth.js"), 200, {'Content-Type': 'application/javascript'}

# ---------------- ERROR HANDLERS ----------------
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)