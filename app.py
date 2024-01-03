from flask import Flask, render_template, request,url_for,flash
import mysql.connector

conn = mysql.connector.connect(host = 'localhost',user='root',password='2121992nasrin',database='project')
mycursor = conn.cursor()

app = Flask(__name__)
user_dict = {'admin': '1234', 'NASRI': '212'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        if username not in user_dict:
            return render_template('login.html', msg='Invalid Username!')

        elif user_dict[username] != pwd:
            return render_template('login.html', msg='Invalid Password!')

        else:
            return render_template('home.html',username=username)

   
    return render_template('login.html', msg='')


from flask import render_template, request

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        P_ID = request.form['P_ID']
        P_NAME = request.form['P_NAME']
        ABOUT = request.form['ABOUT']
        CURRENT_STATUS = request.form['CURRENT_STATUS']
        PROJECT_INCHARGE = request.form['PROJECT_INCHARGE']
        DUE_DATE = request.form['DUE_DATE']

        
        query = "INSERT INTO pro (P_ID, P_NAME, ABOUT, CURRENT_STATUS, PROJECT_INCHARGE, DUE_DATE) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(query, (P_ID, P_NAME, ABOUT, CURRENT_STATUS, PROJECT_INCHARGE, DUE_DATE))
        conn.commit()

       
        select_query = "SELECT * FROM pro"
        mycursor.execute(select_query)
        all_rows = mycursor.fetchall()

      
        return render_template('display.html', sqldata=all_rows, headers=["P_ID", "P_NAME", "ABOUT", "CURRENT_STATUS", "PROJECT_INCHARGE", "DUE_DATE"])

    return render_template('add.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        P_ID = request.form.get('P_ID')
        query = "DELETE FROM pro WHERE P_ID = %s"
        mycursor.execute(query, (P_ID,))
        conn.commit() 
        select_query = "SELECT * FROM pro"
        mycursor.execute(select_query)
        remaining_rows = mycursor.fetchall()       
        return render_template('display.html', sqldata=remaining_rows)
    return render_template('delete.html')
@app.route('/display',methods=['GET','POST'])
def display():
    query="select * from pro"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template('display.html',sqldata=data)
@app.route('/search', methods=['GET', 'POST'])
def search():
    P_ID = request.form.get('P_ID')

    if P_ID is None:
        return render_template('search.html')

    query = "SELECT * FROM pro WHERE P_ID = {}".format(P_ID)
    mycursor.execute(query)
    data = mycursor.fetchall()

    return render_template('display.html', sqldata=data)
from flask import render_template, request

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        P_ID = request.form.get('P_ID')
        new_value = request.form.get('new_value')
        column_to_update = request.form.get('column_to_update')
        update_query = "UPDATE pro SET {} = %s WHERE P_ID = %s".format(column_to_update)

        update_data = (new_value, P_ID)
        mycursor.execute(update_query, update_data)
        conn.commit()

       
        select_query = "SELECT * FROM pro WHERE P_ID = %s"
        mycursor.execute(select_query, (P_ID,))
        updated_row = mycursor.fetchone()

        
        return render_template("display.html", sqldata=[updated_row])

    return render_template('update.html')
 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       
        username = request.form.get('username')
        password = request.form.get('password')
        user_dict[username] = password
        return render_template('login.html')
    return render_template('register.html')  
@app.route('/home')
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(port=5001,debug=True)
