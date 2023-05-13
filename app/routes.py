from app import app
from flask import render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from .pokemon.getpoke import findpokemon
from .forms import SignUpForm, LoginForm, findPoke
from .models import User, Pokemon 
import random

@app.route('/')
def homePage():
    form = findPoke()
    return render_template('index.html', form = form)

@app.route('/catch')
def randomPokemon():
    form = findPoke()
    random_list=[]
    poke_stuff=[]
    for n in range(5):
        random_list.append(random.randint(1,1015))
    for i in random_list:
        poke = findpokemon(i)
        poke_stuff.append(poke)  
    for p in poke_stuff:
        poke_id = p['Id']
        poke_db = Pokemon.query.filter_by(poke_id=poke_id).first()
        if poke_db == None:
            poke = findpokemon(poke_id)
            pokemon = Pokemon(picture=poke['Front Shiny'], pokemon_name=poke['Name'], poke_id=poke['Id'] , ability=poke['Ability'],
                            base_hp=poke['Base HP'], base_attack=poke['Base ATK'], base_defense=poke['Base DEF'])
            pokemon.savePokemon()
            
    p1 = poke_stuff[0]
    p2 = poke_stuff[1]
    p3 = poke_stuff[2]
    p4 = poke_stuff[3]
    p5 = poke_stuff[4]
  
  
    return render_template('pokemon.html', pokemon1=p1,pokemon2=p2,pokemon3=p3,pokemon4=p4,pokemon5=p5, form=form)

