from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    
    __tablename__='heros'
    
    
    
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    super_name=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())
    
    heropowers = db.relationship('HeroPower', back_populates='hero')
    serialize_rules = ('-heropowers.hero',)

    
class HeroPower(db.Model, SerializerMixin):
    
    __tablename__='heropowers'
    
    id =db.Column(db.Integer, primary_key=True)
    strength=db.Column(db.String)
    hero_id=db.Column(db.Integer,db.ForeignKey("heros.id"))
    power_id=db.Column(db.Integer,db.ForeignKey("powers.id"))
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())
    
    hero = db.relationship('Hero', back_populates='heropowers')
    power = db.relationship('Power', back_populates='heropowers')
    
    
    serialize_rules = ('-hero.heropowers','-power.heropowers')
    
    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:

            raise ValueError(f"Strength must be one of:{', '.join(valid_strengths)}")
        return value

            
            
        
class Power(db.Model, SerializerMixin):
    
    __tablename__='powers'
    
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())
    
    heropowers = db.relationship('HeroPower', back_populates='power')
    serialize_rules = ('-heropowers.power',)
    
    @validates('description')
    def validate_description(self, key, value):

        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")

        return value

    
