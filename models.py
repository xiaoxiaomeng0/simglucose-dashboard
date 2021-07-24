from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_login import UserMixin
from sqlalchemy.orm.session import close_all_sessions

app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:iaoeng@localhost:5432/simglucose'
except:
    print("connection error")

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKRed'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
Bootstrap(app)

# close_all_sessions()
# db.session.close_all()
# db.drop_all()


class Result(db.Model):
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
    experiment_id = db.Column(db.Integer, db.ForeignKey(
        "experiment.id"), nullable=False)

    def __repr__(self):
        return f"Results(Time = {self.time}, Patient_ID = {self.patient_id}), BG = {self.bg}, \
        CGM = {self.cgm}, CHO = {self.cho}, reward = {self.reward}\
        INSULIN = {self.insulin}, LBGI = {self.lbgi}, \
        HBGI = {self.hbgi}, RISK = {self.risk}, experiment_id = {self.experiment_id}"


# db.session.query(Result).delete()
# db.session.commit()

# Schema


class ResultSchema(ma.Schema):
    class Meta:
        fields = ('result_id', 'patient_id', 'time', 'bg', 'cgm',
                  'cho', 'lbgi', 'hbgi', 'insulin', 'risk', "experiment_id")


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_name = db.Column(db.String, unique=True, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    results = db.relationship("Result", backref="experiment", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    experiment = db.relationship("Experiment", backref="user", lazy=True)


# db.create_all()
