#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db, Hero,HeroPower,Power

app = Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

class HeroData(Resource):
    def get(self):
         
        response_dict=[data.to_dict() for data in Hero.query.all()]
        
        response=make_response(
            (response_dict),
            200
        )
        return response
   
    
api.add_resource(HeroData, '/heroes')

class HeroById(Resource):
    def get(self,id):
        data = Hero.query.filter_by(id=id).first()
        response_dict=data.to_dict()
        
        response=make_response(
            (response_dict),
            200
        )
        return response
api.add_resource(HeroById, '/heroes/<int:id>')

class PowerData(Resource):
    def get(self):
        data=[one.to_dict() for one in Power.query.all()]
        
        response=make_response(
            data,
            200
        )
        return response
    
  
    
api.add_resource(PowerData, '/powers')


class PowerById(Resource):
    
    def get(self,id):
        power = Power.query.get(id)
        if not power:
            return jsonify({'error': 'Power not found'}), 404
        return make_response(
            jsonify({'id': power.id, 'name': power.name, 'description': power.description}),
            200
        )
        # data = Power.query.filter_by(id=id).first().to_dict()

       
        
        # response=make_response(
        #     jsonify(data),
        #     200
        # )
        # return response
    
    def patch(self,id):
        data=Power.query.filter_by(id=id).first()
        
        for attr in request.form:
            setattr(data,attr,request.form[attr])
        db.session.add(data)    
        db.session.commit()

        response_dict=data.to_dict()
        response=make_response(
            response_dict,
            200
        )
        return response
    
api.add_resource(PowerById, '/powers/<int:id>')  
class NewHeroPower(Resource):
    def get(self):
        data=[one.to_dict() for one in HeroPower.query.all()]
        response_dict=make_response(
            jsonify(data),
            200
        )
        return response_dict

    def post(self):
      
        data = request.get_json()
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        strength = data.get('strength')

        if hero_id is None or power_id is None or strength is None:
            return make_response(jsonify({'errors': ['Missing required data']}), 400)

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return make_response(jsonify({'errors': ['Hero or Power not found']}), 404)

        new_hero_power = HeroPower(hero=hero, power=power, strength=strength)

        try:
            db.session.add(new_hero_power)
            db.session.commit()
            return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': [{'id': power.id, 'name': power.name, 'description': power.description}]})
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 400)
        
api.add_resource(NewHeroPower, '/hero_powers')   

 
if __name__ == '__main__':
    app.run(port=5555)
