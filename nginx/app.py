import psycopg2
import logging
from flask import Flask, jsonify, render_template
from psycopg2 import Error


app = Flask(__name__)

handler = logging.FileHandler("test.log") 
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

@app.route("/")
def hello():
    return 'hello'
    
@app.route("/db")
def db():
    html = ''
    con = None
    
    try:
        conn = psycopg2.connect(
            database="pagiladb",
            user="postgres",
            password="123",
            host="localhost")

        cursor = conn.cursor()
        html += '<h1>PostgreSQL server information</h1>'

        cursor.execute("SELECT version();")
        record = cursor.fetchone()

        html += '<h1>You are connected to - ' + record[0] + '</h1>'

        cursor.close()
    except(Exception) as error:
        html += 'Error while connecting to postgreSQL'
        app.logger.error(error)
    finally:
        if conn is not None:
            conn.close()
            html += 'PostgreSQL connection is closed'

    return html
    
@app.route("/data")
def data():
    html = ''
    con = None
    result = ''

    try:
        con = psycopg2.connect(
                database="pagiladb",
                user="postgres",
                password="123",
                host="localhost")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM actor;")
        result = cursor.fetchall()
        cursor.close()
    except (Exception) as error:
        html += 'Error while connecting to PostgreSQL - '
        app.logger.error(error)
    finally:
        if con is not None:
            con.close()

    return render_template("data.html", datas=result)

@app.route("/health")
def health():
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(host='0.0.0.0')