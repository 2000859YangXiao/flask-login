
from config import app, db, bcrypt, User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
import forms

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def hello_world():

    # Creating a new user when the register form validates
    if forms.RegistrationForm().validate_on_submit():
        # Creating a new user in the database
        register_form = forms.RegistrationForm()
        fo = open("backend\pwd.txt", "r")
        file_contents = fo.read()
        Flag = 0
        for i in file_contents.split('\n'):
            if register_form.password == i:
                Flag = 1
        if Flag == 1:
            return redirect(url_for('hello_world'))

        user = User(username = register_form.username.data,
                email = register_form.email.data,
                password = register_form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("registered")
        # Signing in the user after creating them
        user = User.query.filter_by(email = forms.RegistrationForm().email.data).first()
        if user :
            login_user(user)
        # Taking the user to the authenticated side of the site
        return redirect(url_for('hello_world'))
        
 

    if forms.LoginForm().validate_on_submit():
        user = User.query.filter_by(email = forms.LoginForm().email.data).first()
        if user :
            login_user(user, remember = forms.LoginForm().remember.data)
            flash("login")
            return redirect(url_for('hello_world'))

    if (request.method == "POST") & (request.form.get('post_header') == 'log out'):
        logout_user()
        return redirect(url_for('hello_world'))


    return render_template('index.html',
                           login_form = forms.LoginForm(),
                           register_form = forms.RegistrationForm())

