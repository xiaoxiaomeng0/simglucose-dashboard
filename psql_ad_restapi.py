from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meng:iaoeng@localhost:5432/simglucose'
db = SQLAlchemy(app)

class Results(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    bg = db.Column(db.Float)
    cgm = db.Column(db.Float)
    cho = db.Column(db.Float)
    insulin = db.Column(db.Float)
    lbgi = db.Column(db.Float)
    hbgi = db.Column(db.Float)
    risk = db.Column(db.Float)
    patient_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Results(Time = {time}, BG = {bg}, CGM = {cgm}, CHO = {cho}, INSULIN = {insulin}, LBGI = {lbgi}, HBGI = {hbgi}, RISK = {risk}, Patient_ID = {patient_id})"
    
# resource_fields = {
# 	'patient_id': fields.String,
# 	'bg': fields.Float,
# 	'cgm': fields.Float,
# 	#'likes': fields.Integer
# }

class Simglucose(Resource):
    # @marshal_with(resource_fields)
    def get(self, patient_id):
        print(patient_id)
        result = Results.query.filter_by(patient_id=patient_id).all()
        return result.json()

api.add_resource(Simglucose, "/Simglucose/<string:patient_id>")

if __name__ == "__main__":
    app.run(debug=True)