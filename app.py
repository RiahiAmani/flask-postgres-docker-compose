from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'db'),
        database=os.getenv('DATABASE_NAME', 'mydb'),
        user=os.getenv('DATABASE_USER', 'user'),
        password=os.getenv('DATABASE_PASSWORD', 'password')
    )
    return conn


@app.route('/')
def home():
    return '''
        <h2>Welcome to Flask + PostgreSQL + Docker Compose 🚀</h2>
        <p><a href="/contact">📬 Go to Contact Form</a></p>
    '''


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            return render_template_string(CONTACT_TEMPLATE, error="All fields are required!", name=name, email=email, message=message)

        # Save message to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        conn.close()

        return render_template_string(CONTACT_TEMPLATE, success="Thank you for your message!", name="", email="", message="")

    return render_template_string(CONTACT_TEMPLATE)


# Inline HTML contact page
CONTACT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
        form { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input, textarea { width: 100%; padding: 10px; margin-top: 8px; border: 1px solid #ccc; border-radius: 5px; }
        button { margin-top: 10px; padding: 10px 20px; background: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .msg { text-align: center; margin-bottom: 10px; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h2 style="text-align:center;">📬 Contact Us</h2>

    <form method="POST">
        {% if error %}
            <div class="msg error">{{ error }}</div>
        {% elif success %}
            <div class="msg success">{{ success }}</div>
        {% endif %}

        <label for="name">Name:</label>
        <input type="text" id="name" name="name" value="{{ name or '' }}">

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" value="{{ email or '' }}">

        <label for="message">Message:</label>
        <textarea id="message" name="message" rows="5">{{ message or '' }}</textarea>

        <button type="submit">Send</button>
    </form>

    <p style="text-align:center;"><a href="/">⬅ Back to Home</a></p>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
