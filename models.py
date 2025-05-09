from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    calorie_goal = db.Column(db.Integer, nullable=False)
    preference = db.Column(db.String(50), default='Vegetarian') 
    entries = db.relationship('DailyEntry', back_populates='user')
    
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    calories = db.Column(db.Float)
    category = db.Column(db.String(100))

    calorie_category = db.Column(db.String(100))
    caloric_density = db.Column(db.Float)
    protein_ratio = db.Column(db.Float)
    fat_ratio = db.Column(db.Float)
    carb_ratio = db.Column(db.Float)
    sugar_to_fiber_ratio = db.Column(db.Float)

    total_fat = db.Column(db.Float)
    saturated_fat = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    sodium = db.Column(db.Float)
    choline = db.Column(db.Float)
    folate = db.Column(db.Float)
    folic_acid = db.Column(db.Float)
    niacin = db.Column(db.Float)
    pantothenic_acid = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    vitamin_a = db.Column(db.Float)
    vitamin_a_rae = db.Column(db.Float)
    carotene_alpha = db.Column(db.Float)
    carotene_beta = db.Column(db.Float)
    cryptoxanthin_beta = db.Column(db.Float)
    lutein_zeaxanthin = db.Column(db.Float)
    lucopene = db.Column(db.Float)
    vitamin_b12 = db.Column(db.Float)
    vitamin_b6 = db.Column(db.Float)
    vitamin_c = db.Column(db.Float)
    vitamin_d = db.Column(db.Float)
    vitamin_e = db.Column(db.Float)
    tocopherol_alpha = db.Column(db.Float)
    vitamin_k = db.Column(db.Float)
    calcium = db.Column(db.Float)
    copper = db.Column(db.Float)
    irom = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    manganese = db.Column(db.Float)
    phosphorous = db.Column(db.Float)
    potassium = db.Column(db.Float)
    selenium = db.Column(db.Float)
    zink = db.Column(db.Float)

    protein = db.Column(db.Float)
    alanine = db.Column(db.Float)
    arginine = db.Column(db.Float)
    aspartic_acid = db.Column(db.Float)
    cystine = db.Column(db.Float)
    glutamic_acid = db.Column(db.Float)
    glycine = db.Column(db.Float)
    histidine = db.Column(db.Float)
    hydroxyproline = db.Column(db.Float)
    isoleucine = db.Column(db.Float)
    leucine = db.Column(db.Float)
    lysine = db.Column(db.Float)
    methionine = db.Column(db.Float)
    phenylalanine = db.Column(db.Float)
    proline = db.Column(db.Float)
    serine = db.Column(db.Float)
    threonine = db.Column(db.Float)
    tryptophan = db.Column(db.Float)
    tyrosine = db.Column(db.Float)
    valine = db.Column(db.Float)

    carbohydrate = db.Column(db.Float)
    fiber = db.Column(db.Float)
    sugars = db.Column(db.Float)
    fructose = db.Column(db.Float)
    galactose = db.Column(db.Float)
    glucose = db.Column(db.Float)
    lactose = db.Column(db.Float)
    maltose = db.Column(db.Float)
    sucrose = db.Column(db.Float)

    fat = db.Column(db.Float)
    saturated_fatty_acids = db.Column(db.Float)
    monounsaturated_fatty_acids = db.Column(db.Float)
    polyunsaturated_fatty_acids = db.Column(db.Float)
    fatty_acids_total_trans = db.Column(db.Float)

    alcohol = db.Column(db.Float)
    ash = db.Column(db.Float)
    caffeine = db.Column(db.Float)
    theobromine = db.Column(db.Float)
    water = db.Column(db.Float)

class DailyEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)

    user = db.relationship('User', back_populates='entries')
    food = db.relationship('Food')