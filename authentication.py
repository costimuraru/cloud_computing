from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, map_user_db_to_domain
from werkzeug.security import check_password_hash, generate_password_hash
from blog.__init__ import users_collection
import uuid



authentication = Blueprint('authentication', __name__)

@authentication.route('/2fa', methods=['GET', 'POST'])
def twofa():
    return render_template("2fa.html", user=current_user)

@authentication.route('/user-login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = users_collection.find_one({'email': email})
        if user_data and check_password_hash(user_data['password'], password):
            return render_template("2fa.html", user=current_user)
            if request.form['sms_code'] == user_data['sms_code']:
                flash('You have been logged in successfully!', category='success')
                user = map_user_db_to_domain(user_data)
                login_user(user, remember=True)
                return redirect(url_for('pages.home'))
        else:flash('The verification code you have entered is incorrect', category='error')
    else:
            flash('Your username or password is incorrect, please try again.', category='error')

    return render_template("user-login.html", user=current_user)


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))


@authentication.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone_number = request.form.get('phonenumber')
        user_data = users_collection.find_one({'email': email})
        if user_data:
            flash('This email already exists in database', category='error')
        elif len(email) < 6:
            flash('Email must be greater than 6 characters.', category='error')
        elif len(first_name) < 5:
            flash('First name must be greater than 4 character.', category='error')
        elif password1 != password2:
            flash('The passwords you entered do not match.', category='error')
        elif len(password1) < 10:
            flash('Password must be at least 10 characters.', category='error')
        else:
            flash('Your account was created!', category='success')
            hashed_password = generate_password_hash(password1)
            users_collection.insert({'_id': uuid.uuid4().hex, 'password': hashed_password, 'email': email, 'first_name': first_name, 'phone_number': phone_number, 'notes': None, 'sms_code': None})
            return redirect(url_for('pages.home'))

    return render_template("signup.html", user=current_user)
