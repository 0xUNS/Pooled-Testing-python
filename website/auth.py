from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        immat = request.form.get('immat')
        password = request.form.get('password')

        user = User.query.filter_by(immat=immat).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Connecté avec succès!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Mot de passe incorrect, réessayez.', category='error')
        else:
            flash('Ce compte n\'existe pas.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        immat = request.form.get('immat')
        labo_name = request.form.get('LaboName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(immat=immat).first()
        if user:
            flash('Cette immatriculation existe déjà.', category='error')
        elif not (len(immat) == 5 and ('A' <= immat[0] <= 'Z' or 'a' <= immat[0] <= 'z') and ('0000'<immat[1:5]<='9999')):
            flash('Numéro d\'immatriculation : X0000', category='error')
        elif len(labo_name) < 3:
            flash('Est-ce vraiment le nom du laboratoire ? réessayez.', category='error')
        elif password1 != password2:
            flash('Les mots de passe ne correspondent pas.', category='error')
        elif len(password1) < 7:
            flash('Le mot de passe doit comporter au moins 7 caractères.', category='error')
        else:
            new_user = User(immat=immat, labo_name=labo_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Compte créé avec succès!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
