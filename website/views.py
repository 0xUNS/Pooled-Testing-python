from . import cubelist
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Person, Groupe
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/about')
def aboutus():
    return render_template("about.html")

@views.route('/groupe/<groupId>/add-person', methods=['GET', 'POST'])
def create_person(groupId):
    groupe = Groupe.query.get(groupId)
    if groupe:
        if groupe.user_id == current_user.id:
            if request.method == 'POST':
                CIN = request.form.get('CIN')
                fam_name = request.form.get('Fam_Name')
                name = request.form.get('Name')
                gender = request.form.get('Gender')
                phone = request.form.get('Phone')
                email = request.form.get('Email')
                address = request.form.get('Address')

                if len(CIN) > 9:
                    flash('CIN n\'est pas valable. XX00000', category='error')
                elif len(fam_name) < 2:
                    flash('Est-ce vraiment le nom de famille ? réessayez.', category='error')
                elif len(name) < 2:
                    flash('Est-ce vraiment le prénom ? réessayez.', category='error')
                elif len(phone) > 20:
                    flash('Numéro de téléphone non valide \'0600000000\', réessayez.', category='error')
                elif len(email) < 4:
                    flash('Adresse E-mail non valide \'xxxx@mail.com\', réessayez.', category='error')
                elif len(address) < 7:
                    flash('Entrer une adresse valable', category='error')
                else:
                    new_person = Person(cin=CIN, fam_name=fam_name, name=name, sexe=gender, phone=phone, email=email,address=address, groupe_id=groupe.id)

                    db.session.add(new_person)
                    db.session.commit()
                    flash('Nouveau individu a été ajouté à la liste!', category='success')
                    return redirect(url_for('views.showgroupe', groupId=groupe.id))

            return render_template("add_person.html", user=current_user, groupe=groupe)
    
    flash('Groupe introuvable, choisissez dans la liste ci-dessous!', category='error')
    return redirect(url_for('views.home'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        group_name = request.form.get('Group_Name')
        note = request.form.get('Note')
        if len(group_name) == 0 :
            flash('Erreur! Voulez vous ajouter un groupe à la liste?', category='error')
        else:
            if len(note) == 0:
                note = ' '
            new_groupe = Groupe(name=group_name, note=note, user_id=current_user.id)
            db.session.add(new_groupe)
            db.session.commit()
            flash('Nouveau groupe est ajouté à la liste!', category='success')
        
    return render_template("home.html", user=current_user )


@views.route('/groupe/<groupId>',  methods=['GET', 'POST'])
def showgroupe(groupId):
    groupe = Groupe.query.get(groupId)
    if groupe:
        if groupe.user_id == current_user.id:
            return render_template("showgroup.html", user=current_user, groupe=groupe) 
    
    flash('Groupe introuvable, choisissez dans la liste ci-dessous!', category='error')
    return redirect(url_for('views.home'))

@views.route('/delete-group', methods=['POST'])
def delete_group():
    groupe = json.loads(request.data)
    groupId = groupe['groupId']
    groupe = Groupe.query.get(groupId)
    if groupe:
        if groupe.user_id == current_user.id:
            db.session.delete(groupe)
            db.session.commit()

    return jsonify({})

@views.route('/delete-person', methods=['POST'])
def delete_person():
    person = json.loads(request.data)
    personId = person['personId']
    person = Person.query.get(personId)
    if person:
        db.session.delete(person)
        db.session.commit()

    return jsonify({})

@views.route('/groupe/<groupId>/rang',  methods=['GET', 'POST'])
def bloc(groupId):
    groupe = Groupe.query.get(groupId)
    if groupe:
        if groupe.user_id == current_user.id:
            person = []
            resultats = []
            for p in groupe.persons:
                person.append(p.id)
            listIndv = cubelist.mainlist(person)
            if request.method == "POST":
                for i in range(len(listIndv)):
                    resultats.append(request.form.get(f'resultat[{i}]'))
            if resultats:
                positiveIndv = cubelist.infectees(resultats, person)
            else:
                positiveIndv=''
    return render_template("rang.html", user=current_user, groupe = groupe, listIndv = listIndv, positive=positiveIndv)
