from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
  # Enables CORS for all routes

# Configure Database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Incident Model
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    incident_type = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    anonymous = db.Column(db.Boolean, default=False)

# Create database tables
with app.app_context():
    db.create_all()
@app.route('/reports', methods=['GET'])
def get_reports():
    try:
        reports = Incident.query.all()
        report_list = [{
            "id": report.id,
            "name": report.name,
            "phone": report.phone,
            "location": report.location,
            "time": report.time,
            "incident_type": report.incident_type,
            "details": report.details,
            "anonymous": report.anonymous
        } for report in reports]

        return jsonify(report_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle incident report submission
@app.route('/report', methods=['POST'])
def report():
    try:
        data = request.json
        new_incident = Incident(
            name=data.get('name') if not data.get('anonymous') else "Anonymous",
            phone=data.get('phone'),
            location=data.get('location'),
            time=data.get('time'),
            incident_type=data.get('incidentType'),
            details=data.get('details'),
            anonymous=data.get('anonymous')
        )
        db.session.add(new_incident)
        db.session.commit()

        return jsonify({"message": "Incident report submitted successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
