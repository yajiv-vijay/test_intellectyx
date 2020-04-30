from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from sqlite3 import Error
from datetime import datetime

app = Flask(__name__)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

@app.route('/',methods=['GET', 'POST'])
def index():
    database = r"storage\SqliteDB\ShopDetails.db"
    conn = create_connection(database)

    if request.method == 'POST':
        name = request.form["name"];shop_name = request.form["shop_name"];status = request.form["status"]
        cur1 = conn.cursor()
        strTime =datetime.now().strftime("%m/%d/%Y %H:%M:%S")     
        cur1.execute("INSERT INTO SHOP_DETAILS(NAME,SHOP_NAME,STATUS,DATE) VALUES (?,?,?,?)",(name,shop_name,status,strTime) )
        conn.commit()

        cur = conn.cursor()
        cur.execute("SELECT * FROM SHOP_DETAILS")
        items = cur.fetchall()
        conn.close()
        return render_template('index.html', items=items)
    cur = conn.cursor()
    cur.execute("SELECT * FROM SHOP_DETAILS")
    items = cur.fetchall()
    conn.close()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run()