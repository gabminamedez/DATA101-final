from . import db 


class IncidentVehicles(db.Model):
    __tablename__ = "incident_vehicles"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    vehicle = db.Column(db.String(150))
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))

class IncidentTweet(db.Model):
    __tablename__ = "incident_tweet"
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(150))
    source = db.Column(db.String(150))
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))

class Incident(db.Model):
    __tablename__ = "incident"
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    city = db.Column(db.String(150))
    location = db.Column(db.String(150))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    high_accuracy = db.Column(db.Integer)
    direction = db.Column(db.String(10))
    incident_type = db.Column(db.String(150))
    lanes_blocked = db.Column(db.Integer)
    involved = db.relationship('IncidentVehicles')
    tweet = db.relationship('IncidentTweet')