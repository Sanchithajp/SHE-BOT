from report import db, app

try:
    with app.app_context():
        db.create_all()
        print("✅ Database created successfully!")
except Exception as e:
    print("❌ Error creating database:", e)
