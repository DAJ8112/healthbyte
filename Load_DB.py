from models import db, Food
from flask import Flask
import pandas as pd
import math
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

pymysql.install_as_MySQLdb()
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/healthbyte'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def convert_nan_to_none(data_dict):
    return {k: (None if pd.isna(v) or (isinstance(v, float) and math.isnan(v)) else v) for k, v in data_dict.items()}

with app.app_context():
    db.create_all()

    # Load and clean CSV
    df = pd.read_csv('./nutrition_features.csv')
    df.drop_duplicates(subset=['name'], inplace=True)

    # Only keep columns that match Food model attributes
    valid_columns = [col.name for col in Food.__table__.columns if col.name != 'id']

    inserted = 0
    for _, row in df.iterrows():
        if Food.query.filter_by(name=row['name']).first():
            continue

        food_data = {col: row.get(col) for col in valid_columns if col in row}
        food_data = convert_nan_to_none(food_data)

        food = Food(**food_data)
        db.session.add(food)
        inserted += 1

    db.session.commit()
    print(f"{inserted} rows inserted successfully!")
