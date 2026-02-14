from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'grademe'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'secretpass')
    )

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "backend"})

@app.route('/submissions')
def submissions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT student_name, grade FROM submissions;')
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"name": r[0], "grade": r[1]} for r in results])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
