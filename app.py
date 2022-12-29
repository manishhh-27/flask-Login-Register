from flask import Flask, render_template, url_for, request, redirect,session
from flask_pymongo import PyMongo

from pymongo import MongoClient

app = Flask(__name__)
app.secret_key='hello'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'

mongo = PyMongo(app)



@app.route("/")
def main():
    return render_template('index.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        register_user = users.find_one({'username': request.form['username']})
        if register_user:
            return render_template('register.html',msg="This username already exist,Try another")


        
    

        
        users.insert_one({'username': request.form['username'], 'password': request.form['password'], 'email': request.form['email']})
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/index')
def index():


    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if request.form['password']==login_user['password'] :
                session['username'] = request.form['username']
                return render_template('welcome.html',name=request.form['username'])
        
        
        return render_template('login.html',msg="Incorrect username or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    