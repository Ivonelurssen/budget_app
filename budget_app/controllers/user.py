
from budget_app import app

from flask import Flask, render_template, request, redirect, session, flash

from budget_app.models import users

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('test.html')

@app.route('/register')
def register_form():

    return render_template('register.html')

@app.route('/create', methods = ['POST'])
def register():

    if request.form['action'] == 'register':

        if not users.User.validate(request.form):
            return redirect('/register')

        pw_hash = bcrypt.generate_password_hash(request.form["password"])

        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password': pw_hash
        
        }

        user_info = users.User.save(data)

        session['user_info'] = user_info


    else:


        user_info = users.User.get_onewith_email ({'email': request.form['email'].lower()})
        print(user_info)
        if user_info:
            if len(request.form['password']) < 8:
                flash("Password must be at least 8 characters")
                return redirect("/")
            if bcrypt.check_password_hash(user_info.password, request.form['password']):
                session["user_info"] = user_info.id
                return redirect("/")
            else:
                flash("Incorrect Password")
                return redirect("/register")
        else:
            flash("No user with this email")
            return redirect("/register")



    return redirect('/')