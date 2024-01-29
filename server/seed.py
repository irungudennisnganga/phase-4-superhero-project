from models import db, Hero, Power, HeroPower
from app import app
print("🦸‍♀ Seeding powers...")
powers = [
    Power(name="super strength", description="gives the wielder super-human strengths"),
    Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
    Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
    Power(name="elasticity", description="can stretch the human body to extreme lengths"),
]
with app.app_context():
    db.session.bulk_save_objects(powers)
    db.session.commit()

print("🦸‍♀ Seeding heroes...")
heroes = [
    Hero(name="Kamala Khan", super_name="Ms. Marvel"),
    Hero(name="Doreen Green", super_name="Squirrel Girl"),
    Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
    Hero(name="Janet Van Dyne", super_name="The Wasp"),
    Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
    Hero(name="Carol Danvers", super_name="Captain Marvel"),
    Hero(name="Jean Grey", super_name="Dark Phoenix"),
    Hero(name="Ororo Munroe", super_name="Storm"),
    Hero(name="Kitty Pryde", super_name="Shadowcat"),
    Hero(name="Elektra Natchios", super_name="Elektra"),
]
with app.app_context():
    db.session.bulk_save_objects(heroes)
    db.session.commit()

print("‍♀ Adding powers to heroes...")
strengths = ["Strong", "Weak", "Average"]  # Ensure enough elements

with app.app_context():
    for hero in Hero.query.all():
        for _ in range(1, 4):
            power = Power.query.order_by(db.func.random()).first()
            if strengths:  # Check if the list is not empty
                hero_power = HeroPower(hero=hero, power=power, strength=strengths.pop())
                db.session.add(hero_power)
            else:  # Handle the case when the list is empty
                print("No more strengths available for assignment.")
    db.session.commit()

print("‍♀ Done seeding!")
