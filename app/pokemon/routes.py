from ..models import User, Pokemon, teams, db
from ..forms import SignUpForm, LoginForm, findPoke
from .getpoke import findpokemon
from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
pokemon = Blueprint('pokemon', __name__, template_folder='pokemon_templates')

@pokemon.route('/view-team/poke/<int:t_id>')
def viewTeamsPoke(t_id):
    user = User.query.get(t_id)
    user_pokemon = user.caught.all()
    return render_template('view_team_poke.html', pokemon = user_pokemon)

@pokemon.route('/teams')
def Teams():
    teams =  User.query.all()
    team_info = []
    for t in teams:
        teams_pokemon = t.caught.all()
        team_info.append(teams_pokemon)
    print(team_info)
    return render_template('teams.html', teams=teams)

@pokemon.route('/rankings')
def leaderBoard():
    users = User.query.all()
    return render_template('leaderboard.html', users=users)

@pokemon.route('/my-pokemon')
def showMyPokemon():
    pokemon = current_user.caught.all()
    count = len(pokemon)
    return render_template('my-pokemon.html', pokemon = pokemon, count=count)

@pokemon.route('/catch-em-all/<int:p1>/<int:p2>/<int:p3>/<int:p4>/<int:p5>/')
def catchAll(p1,p2,p3,p4,p5):
    rando_poke = [p1,p2,p3,p4,p5]
    catch_poke = []
    current_user_poke_count = len(current_user.caught.all())
    if current_user_poke_count >= 1:
        flash("You can't have ANY Pokemon if you want to catch them all!")
        return redirect(url_for('pokemon.showMyPokemon'))
    else:
        for i in rando_poke:
            poke_db = Pokemon.query.filter_by(poke_id=i).first()
            catch_poke.append(poke_db)
        for c in catch_poke:
            current_user.catchPokemon(c)
        return redirect(url_for('pokemon.showMyPokemon'))


@pokemon.route('/catch-em/<int:p_id>')
def catchPokemon(p_id):
    current_user_poke_count = len(current_user.caught.all())
    if current_user_poke_count >= 5:
        flash("You need to release one in order to catch more!")
        return redirect(url_for('pokemon.showMyPokemon'))
    else:
        poke = Pokemon.query.filter_by(poke_id=p_id).first()
        flash(f"{poke} has been caught!")
        current_user.catchPokemon(poke)
        pokemon_info = Pokemon.query.filter_by(poke_id=p_id).first()
        print(pokemon_info)
        return redirect(url_for('pokemon.showMyPokemon'))
    
@pokemon.route('/release-em/<int:p_id>')
def releasePokemon(p_id):
    pokemon_search = Pokemon.query.get(p_id)
    current_user.releasePokemon(pokemon_search)
    print(p_id)
    print(pokemon_search)
    return redirect(url_for('pokemon.showMyPokemon'))
    
@pokemon.route('/release-all')
def releaseAll():
    current_user.caught = []
    db.session.commit()
    return redirect(url_for('pokemon.showMyPokemon'))
    
@pokemon.route('/battles')
def battlePokemon():
    current_user_poke_count = len(current_user.caught.all())
    if current_user_poke_count == 5:
        current_user_pokemon = current_user.caught.all()
        p1 = current_user_pokemon[0]
        p2 = current_user_pokemon[1]
        p3 = current_user_pokemon[2]
        p4 = current_user_pokemon[3]
        p5 = current_user_pokemon[4]    
        users = User.query.all()
        users_able_to_battle = []
        for t in users:
            pokemon_caught = len(t.caught.all())
            if pokemon_caught == 5:
                users_able_to_battle.append(t)
        return render_template('battle.html', p1 = p1, p2 = p2, p3 = p3, p4 = p4, p5 = p5, users=users_able_to_battle)
    else:
        
        return redirect(url_for('pokemon.showMyPokemon'))
    
@pokemon.route('/final-battle/<int:t_id>')
def FinalBattle(t_id):
    enemy = User.query.get(t_id)
    print(f'{current_user} VS. {enemy}')
    current_user_team = current_user.caught.all()
    enemy_team = enemy.caught.all()
    current_user_attack = 0
    enemy_team_attack = 0
    for a in current_user_team:
        attack = (a.base_attack)
        current_user_attack += attack
    for a in enemy_team:
        attack = (a.base_attack)
        enemy_team_attack += attack
    print(f'CURRENT:{current_user_attack}\nENEMY:{enemy_team_attack}')
    if current_user_attack > enemy_team_attack:
        current_user.winner()
        enemy.loser()
        print('CURRENT USER WIN\nENEMY TEAM LOSE')
        return render_template('battleplayer2.html')
    else:
        current_user.loser()
        enemy.winner()
        print('ENEMY TEAM WINNER\nCURRENT USER LOSS')
        return render_template('battleplayer.html')