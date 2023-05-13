from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
db = SQLAlchemy()


teams = db.Table(
    'teams',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey(
        'pokemon.id'), nullable=False)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, )
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    caught = db.relationship('Pokemon',
                             secondary='teams',
                             backref= 'caught',
                             lazy='dynamic'
                             )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.wins = 0
        self.losses = 0

    def saveUser(self):
        db.session.add(self)
        db.session.commit()   

    def catchPokemon(self, pokemon):
        self.caught.append(pokemon)
        db.session.commit()

    def releasePokemon(self, pokemon):
        self.caught.remove(pokemon)
        db.session.commit()

    def winner(self):
        self.wins += 1
        db.session.commit()

    def loser(self):
        self.losses += 1
        db.session.commit()

        
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, nullable=False, unique=True)
    picture = db.Column(db.String, nullable=True)
    pokemon_name = db.Column(db.String, nullable=False, unique=True)
    ability = db.Column(db.String, nullable=False)
    base_hp = db.Column(db.Integer, nullable=False)
    base_attack = db.Column(db.Integer, nullable=False)
    base_defense = db.Column(db.Integer, nullable=False)

    def __init__(self, poke_id, picture, pokemon_name, ability, base_hp, base_attack, base_defense):
        self.poke_id = poke_id
        self.picture = picture
        self.pokemon_name = pokemon_name
        self.ability = ability
        self.base_hp = base_hp
        self.base_attack = base_attack
        self.base_defense = base_defense

    def savePokemon(self):
        db.session.add(self)
        db.session.commit()

    def convertDict(self):
        return {"Name": self.pokemon_name,
                "Ability": self.ability,
                "Front Shiny": self.picture,
                "Base ATK": self.base_attack,
                "Base HP": self.base_hp,
                "Base DEF": self.base_defense}