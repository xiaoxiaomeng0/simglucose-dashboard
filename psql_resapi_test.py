from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meng:IAOeng19910804@localhost/simglucose'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

class Results(db.Model):
    __table__ = db.Model.metadata.tables['Results']
    
    # def __repr__(self):
    #     return f"Results(BG = {bg}, CGM = {cgm}, CHO = {cho}, INSULIN = {insulin}, LBGI = {lbgi}, HBGI = {hbgi}, RISK = {risk}, Patient_ID = {patient_id})"

class Simglucose(Resource):
    def get(self, patient_id):
        result = Results.query.filter_by(patient_id=patient_id).all()
        return result

api.add_resource(Simglucose, "/Simglucose/<string:patient_id>")

if __name__ == "__main__":
    app.run(debug=True)