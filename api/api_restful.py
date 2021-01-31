from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meng:iaoeng@localhost:5432/simglucose'
db = SQLAlchemy(app)

# Create Database Models
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

    # Print one row from database if necessary
    def __repr__(self):
        return f"Results(Time = {self.time}, BG = {self.bg}, \
        CGM = {self.cgm}, CHO = {self.cho}, \
        INSULIN = {self.insulin}, LBGI = {self.lbgi}, \
        HBGI = {self.hbgi}, RISK = {self.risk}, \
        Patient_ID = {self.patient_id})"

# Pass argument
results_args = reqparse.RequestParser()
results_args.add_argument("bg", type=float)
results_args.add_argument("cgm", type=float)
results_args.add_argument("time", type=str)
results_args.add_argument("cho", type=float)
results_args.add_argument("insulin", type=float)
results_args.add_argument("lbgi", type=float)
results_args.add_argument("hbgi", type=float)
results_args.add_argument("risk", type=float)

# Define the format to show to the client
resource_fields = {
	'patient_id': fields.String,
	'bg': fields.Float,
	'cgm': fields.Float,
	'time': fields.String
}

class Simglucose(Resource):
    @marshal_with(resource_fields)
    def get(self, patient_id):
        result = Results.query.filter_by(patient_id=patient_id).all()
        return result 

    @marshal_with(resource_fields)
    def post(self, patient_id):
        args = results_args.parse_args()
        result = Results.query.filter_by(patient_id=patient_id).first()
        if result:
            abort(409, messsage="patient_id taken...")
        sim_result = Results(
            patient_id=patient_id,
            bg=args['bg'], 
            cgm=args['cgm'], 
            time=args['time'], 
            cho=args['cho'],
            insulin=args['insulin'], 
            lbgi=args['lbgi'], 
            hbgi=args['hbgi'], 
            risk=args['risk'])
        db.session.add(sim_result)
        db.session.commit()
        return sim_result, 201
    
    def delete(self, patient_id):
        result = Results.query.filter_by(patient_id=patient_id).all()
        if not result:
            abort(409, messsage="patient_id does not exist...")
        db.session.delete(result)
        db.session.commit()
        return "", 204

api.add_resource(Simglucose, "/Simglucose/<string:patient_id>")

if __name__ == "__main__":
    app.run(debug=True, port=5001)