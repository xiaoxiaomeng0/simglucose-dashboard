from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:iaoeng@localhost:5432/simglucose'
except:
    print("connection error")

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    reward = db.Column(db.Float, nullable=False)
    cgm = db.Column(db.Float)
    cho = db.Column(db.Float)
    insulin = db.Column(db.Float)
    bg = db.Column(db.Float)
    lbgi = db.Column(db.Float)
    hbgi = db.Column(db.Float)
    risk = db.Column(db.Float)

    def __repr__(self):
        return f"Results(Time = {self.time}, Patient_ID = {self.patient_id}), BG = {self.bg}, \
        CGM = {self.cgm}, CHO = {self.cho}, reward = {self.reward}\
        INSULIN = {self.insulin}, LBGI = {self.lbgi}, \
        HBGI = {self.hbgi}, RISK = {self.risk}"

# Schema


class ResultSchema(ma.Schema):
    class Meta:
        fields = ('result_id', 'patient_id', 'time', 'bg', 'cgm',
                  'cho', 'lbgi', 'hbgi', 'insulin', 'risk')


# db.create_all()
