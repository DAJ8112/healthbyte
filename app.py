from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime, timedelta
import io, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import func
from models import db, User, Food, DailyEntry
from dotenv import load_dotenv
import os
import pymysql

# --- App Setup ---
load_dotenv()
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create tables on startup
with app.app_context():
    db.create_all()

# Inject current time into templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    return redirect(url_for('login'))

# --- Signup ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pw = request.form['password']
        goal = int(request.form['calorie_goal'])
        preference = request.form.get('preference', '')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(pw),
            calorie_goal=goal,
            preference=preference
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created; please log in')
        return redirect(url_for('login'))

    return render_template('signup.html')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, pw):
            login_user(user)
            return redirect(url_for('search'))
        flash('Invalid credentials')
    return render_template('login.html')

# --- Logout ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Search ---
@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').strip()
    foods = []
    if query:
        foods = (Food.query
                    .filter(Food.name.ilike(f"%{query}%"))
                    .order_by(Food.name)
                    .limit(10)
                    .all())
    return render_template('search.html', foods=foods, query=query)

# --- Compare ---
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Food
import matplotlib.pyplot as plt
import io
import base64

@app.route('/compare', methods=["GET", "POST"])
@login_required
def compare():
    names = [f.name for f in Food.query.all()]

    if request.method == "POST":
        f1_name = request.form.get('product1')
        f2_name = request.form.get('product2')

        f1 = Food.query.filter_by(name=f1_name).first()
        f2 = Food.query.filter_by(name=f2_name).first()

        if not f1 or not f2:
            flash("One or both food items not found.")
            return redirect(url_for('compare'))

        keys = ["caloric_density", "protein_ratio", "fat_ratio",
            "carb_ratio", "sugar_to_fiber_ratio", "total_fat", "protein",
            "carbohydrate", "vitamin_d"]
        vals1 = [getattr(f1, k) or 0 for k in keys]
        vals2 = [getattr(f2, k) or 0 for k in keys]

        # Generate comparison bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        index = range(len(keys))
        ax.bar(index, vals1, width=0.4, label=f1.name, color='#A4BE5C')  # Light olive green
        ax.bar([i + 0.4 for i in index], vals2, width=0.4, label=f2.name, color='#8B4513')  # Brown
        ax.set_xticks([i + 0.2 for i in index])
        ax.set_xticklabels(keys, rotation=45)
        ax.legend()
        fig.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_data = base64.b64encode(buf.read()).decode()
        plt.close(fig)

        # Helper function to render calorie category badges
        def badge(category):
            colors = {
                "Low": "#28a745",
                "Moderate": "#ffc107",
                "High": "#fd7e14",
                "Very High": "#dc3545"
            }
            color = colors.get(category, "#6c757d")
            return f'<span style="display:inline-block; width:12px; height:12px; background:{color}; border-radius:3px; margin-right:6px;"></span>{category}'

        return render_template("compare.html",
                               names=names,
                               chart_data=chart_data,
                               cat1=badge(f1.calorie_category),
                               cat2=badge(f2.calorie_category),
                               name1=f1.name,
                               name2=f2.name)

    # For GET: just show the dropdowns
    return render_template("compare.html", names=names)


# --- Daily Tracking + Recommendations ---
@app.route('/daily', methods=['GET', 'POST'])
@login_required
def daily():
    if request.method == 'POST':
        name = request.form['food_name']
        qty = float(request.form['quantity'])
        food = Food.query.filter_by(name=name).first()
        if food:
            today = date.today()
            entry = DailyEntry(user_id=current_user.id,
                               food_id=food.id,
                               quantity=qty,
                               date=today)
            db.session.add(entry)
            db.session.commit()
            flash(f"Added {qty} of {name}")
        else:
            flash(f"Food '{name}' not found")
        return redirect(url_for('daily'))

    # Get today's entries
    today = date.today()
    entries = DailyEntry.query.filter_by(user_id=current_user.id, date=today).all()
    total_cals = sum(e.quantity * e.food.calories for e in entries if e.food and e.food.calories)

    # 30-day history
    history = []
    for i in range(30):
        d = today - timedelta(days=i)
        daily_entries = DailyEntry.query.filter_by(user_id=current_user.id, date=d).all()
        cals = sum(e.quantity * e.food.calories for e in daily_entries if e.food and e.food.calories)
        symbol = '✓' if cals >= current_user.calorie_goal else '✗'
        history.append({
            'date': d,
            'symbol': symbol,
            'calories': round(cals, 1)
        })
    history.reverse()

    # Calculate remaining calories
    remaining = current_user.calorie_goal - total_cals
    recommendations = []
    
    if remaining > 0:
        # Determine allowed categories based on user preference
        pref = current_user.preference.lower()
        if pref == 'vegan':
            allowed = ['Vegan']
        elif pref == 'vegetarian':
            allowed = ['Vegan', 'Vegetarian']
        else:
            allowed = ['Vegan', 'Vegetarian', 'Non-Vegetarian']

        # Widen buffer to improve match rate
        min_cals = max(remaining - 100, 0)
        max_cals = remaining + 100

        print("DEBUG: Remaining calories =", remaining)
        print("DEBUG: Allowed categories =", allowed)
        print("DEBUG: Calorie range =", min_cals, "-", max_cals)

        recommendations = Food.query.filter(
            Food.calories >= min_cals,
            Food.calories <= max_cals,
            Food.category.in_(allowed)
        ).limit(5).all()

    return render_template('daily.html',
                           entries=entries,
                           total_cals=total_cals,
                           history=history,
                           recommendations=recommendations,
                           remaining_calories=remaining)

    # --- AJAX endpoint for food details ---
@app.route('/food/<int:food_id>')
def get_food_details(food_id):
    food = Food.query.get_or_404(food_id)
    data = {col.name: getattr(food, col.name) for col in food.__table__.columns}
    return jsonify(data)

# Delete and update food entry
@app.route('/delete-entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = DailyEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('daily'))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted successfully")
    return redirect(url_for('daily'))

@app.route('/edit-entry/<int:entry_id>', methods=['POST'])
@login_required
def edit_entry(entry_id):
    entry = DailyEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('daily'))
    try:
        new_qty = float(request.form['quantity'])
        entry.quantity = new_qty
        db.session.commit()
        flash("Entry updated successfully")
    except Exception as e:
        flash("Invalid update")
    return redirect(url_for('daily'))

if __name__ == '__main__':
    app.run(debug=True)