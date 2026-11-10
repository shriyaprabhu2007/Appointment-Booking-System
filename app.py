from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        service TEXT,
        date TEXT,
        time TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Appointment Form
@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

# Save Appointment
@app.route('/book', methods=['POST'])
def book():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    service = request.form['service']
    date = request.form['date']
    time = request.form['time']
    message = request.form['message']

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO appointments
    (name,email,phone,service,date,time,message)
    VALUES (?,?,?,?,?,?,?)
    """,(name,email,phone,service,date,time,message))

    conn.commit()
    conn.close()

    return redirect(url_for('appointments'))

# Display Appointments
@app.route('/appointments')
def appointments():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointments")
    data = cur.fetchall()

    conn.close()

    return render_template("appointments.html", appointments=data)

# Delete Appointment
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM appointments WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('appointments'))


# Edit Appointment
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']

        cur.execute("""
        UPDATE appointments
        SET name=?, email=?, phone=?, service=?,
        date=?, time=?, message=?
        WHERE id=?
        """, (name, email, phone, service, date, time, message, id))

        conn.commit()
        conn.close()
        return redirect(url_for('appointments'))

    cur.execute("SELECT * FROM appointments WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()

    if data is None:
        return "Appointment not found", 404

    return render_template("edit.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
