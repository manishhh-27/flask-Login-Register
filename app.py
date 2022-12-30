from flask import Flask, render_template, url_for, request, redirect,session
from flask_pymongo import PyMongo
import bcrypt


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


        
    

        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        users.insert_one({'username': request.form['username'], 'password': hashed, 'email': request.form['email'],'address': request.form['address'],'mobile_no': request.form['mobile'],'bio':request.form['bio']})
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
            if  bcrypt.checkpw(request.form['password'].encode('utf-8'),login_user['password']):
                session['username'] = request.form['username']
                dat=request.form
                return render_template('welcome.html',data=login_user)
        
        
        return render_template('login.html',msg="Incorrect username or password!")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    users = mongo.db.users
    update_user = users.find_one({'username': session['username']})
    if request.method=='POST':
        users.update_one({"username":update_user['username']},{ "$set": { 'email': request.form['email'],'address':request.form['address'],'mobile_no':request.form['mobile'] ,'bio':request.form['bio']}}  )
        update_user = users.find_one({'username': session['username']})
        return render_template('welcome.html',data=update_user)

    return render_template('edit.html',data=update_user)




if __name__ == "__main__":
    app.run(debug=True)
    