# HealthByte

HealthByte is a Flask‑based web application for tracking daily nutrition, setting calorie goals, and receiving food recommendations based on dietary preferences to complete daily calorie intake (Vegan, Vegetarian, Non‑Vegetarian).  

This project was done for the coursework of Applied Database Technologies.

## Features
- User signup, login and secure password storage
- Set and track daily calorie goals
- Search and compare nutritional profiles of foods
- Log daily intake with quantity and view history
- Automatic recommendations for remaining calories
- Visual charts for food comparison

## Functionalities

1. Login Page
<figure>
  <img src="screenshots/login.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

2. Signup Page
<figure>
  <img src="screenshots/signup.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

3. Food Searching
<figure>
  <img src="screenshots/search.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

4. Food Adding
<figure>
  <img src="screenshots/foodadd.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

5. Daily Log
<figure>
  <img src="screenshots/dailycomplete.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

6. Recommendations based on left calories for day
<figure>
  <img src="screenshots/recommendations.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

7. Comparing two food items
<figure>
  <img src="screenshots/comparepage.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

<figure>
  <img src="screenshots/chart2.png" alt="Alt text caption" width="500">
  <!-- <figcaption>Login Page</figcaption> -->
</figure>

## Directory Structure
```
/healthbyte
├── app.py              # Main Flask application with routes
├── models.py           # SQLAlchemy models: User, Food, DailyEntry
├── modified_nutrition.csv  # Nutrition dataset used by the app
├── templates/          # Jinja2 HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── search.html
│   ├── compare.html
│   ├── daily.html
│   └── layout.html
├── static/             # Static assets (CSS, JS, images)
├── .env                # Environment variables (SECRET_KEY, DATABASE_URL)
├── .gitignore
└── README.md           # This documentation
```

## Setup & Installation
1. Clone the repo:  
   `git clone https://github.com/yourusername/healthbyte.git`  
2. Create and activate a virtual environment:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:  
   `pip install -r requirements.txt`  
4. Configure `.env` with:  
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql://user:pass@host/db_name
   ```
5. Initialize the database:  
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Running the App
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Open `http://localhost:5000` in your browser.

## Usage Workflow
1. **Signup/Login**: Create an account or login.
2. **Set Preferences**: Define your daily calorie goal and dietary preference.
3. **Search Foods**: Lookup items from `modified_nutrition.csv`.
4. **Compare**: Select two foods to see a side‑by‑side nutrient bar chart.
5. **Log Intake**: Record quantity consumed each day.
6. **Daily View**: Check your calories, history, status (✓/✗), and get recommendations.

## How It Works
- **Flask & SQLAlchemy**: Routes in `app.py` handle HTTP requests. Models in `models.py` map to MySQL tables.
- **Authentication**: Managed with Flask-Login; passwords hashed via Werkzeug.
- **Data**: Food records loaded from CSV into the `Food` table.
- **Visualization**: Matplotlib generates comparison charts, embedded as Base64 images.
- **Recommendations**: Calculates remaining calories and filters foods by user preference.

## Authors
Dhruvil Joshi<br>
Meryl Jacob
