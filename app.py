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
        try:
            id = request.form["PrimaryId"]
            cur = conn.cursor()
            cur.execute("UPDATE SHOP_DETAILS SET NAME = ? ,SHOP_NAME = ? ,STATUS = ?,DATE = ? WHERE id = ?",(request.form["name"], request.form["shop_name"],request.form["status"], datetime.now().strftime("%m/%d/%Y %H:%M:%S"), id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except:
            cur = conn.cursor()    
            cur.execute("INSERT INTO SHOP_DETAILS(NAME,SHOP_NAME,STATUS,DATE) VALUES (?,?,?,?)",(request.form["name"],request.form["shop_name"],request.form["status"],datetime.now().strftime("%m/%d/%Y %H:%M:%S")) )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    elif request.method == 'PUT':
        database = r"storage\SqliteDB\ShopDetails.db"
        conn = create_connection(database)
        
        
    cur = conn.cursor()
    cur.execute("SELECT * FROM SHOP_DETAILS")
    items = cur.fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/button_press/<primary_key>/<action>')
def button_press(primary_key,action): 
    if action == "delete":
        database = r"storage\SqliteDB\ShopDetails.db"
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM SHOP_DETAILS WHERE ID='"+ primary_key + "';")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()