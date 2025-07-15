from flask import Flask, request, render_template_string
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# الاتصال بقاعدة البيانات
db = mysql.connector.connect(
    host="localhost",
    user="noteuser",
    password="note123",
    database="notesdb"
)

cursor = db.cursor()

# HTML
html = """
<!DOCTYPE html>
<html>
<head><title>Note Taking App</title></head>
<body>
    <h1>📝 Note Taking App</h1>
    <form method="POST">
        <textarea name="note" rows="4" cols="50" placeholder="Write your note here..."></textarea><br>
        <button type="submit">Save Note</button>
    </form>
    <hr>
    {% for note in notes %}
        <p>🕒 {{ note[2] }}<br>📌 {{ note[1] }}</p><hr>
    {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form['note']
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
        db.commit()

    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()
    return render_template_string(html, notes=notes)

if __name__ == '__main__':
    app.run()

