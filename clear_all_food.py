# from app import app, db
# from models import Food

# with app.app_context():
#     db.session.query(Food).delete()
#     db.session.commit()
#     print("All food entries deleted.")

# from app import app, db

with app.app_context():
    db.drop_all()
    print("✅ All tables dropped.")

    db.create_all()
    print("✅ All tables recreated.")