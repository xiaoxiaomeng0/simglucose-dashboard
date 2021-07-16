from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://meng:iaoeng@localhost:5432/simglucose'

db = SQLAlchemy(app)
ma = Marshmallow(app)


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
        return f"Results(Time = {self.time}, BG = {self.bg}, \
        CGM = {self.cgm}, CHO = {self.cho}, \
        INSULIN = {self.insulin}, LBGI = {self.lbgi}, \
        HBGI = {self.hbgi}, RISK = {self.risk}, \
        Patient_ID = {self.patient_id})"

# Schema


class ResultSchema(ma.Schema):
    class Meta:
        fields = ('result_id', 'patient_id', 'time', 'bg', 'cgm',
                  'cho', 'lbgi', 'hbgi', 'insulin', 'risk')


# Init schema
result_schema = ResultSchema()
results_schema = ResultSchema(many=True)


@app.route('/api/results/<patient_id>', methods=['GET'])
def get(patient_id):
    results = Results.query.filter_by(patient_id=patient_id).all()
    # return results.json()
    return results_schema.jsonify(results)


@app.route('/api/results/allpatientid', methods=['GET'])
def allPatientID():
    all_patient_name = []
    for result in Results.query.distinct(Results.patient_id):
        all_patient_name.append(result.patient_id)
    return jsonify(all_patient_name)


@app.route('/api/results/', methods=['POST'])
def post():
    patient_id = request.json['patient_id']
    time = request.json['time']
    risk = request.json['risk']

    new_result = Results(patient_id, time, risk)

    db.session.add(new_result)
    db.session.commit()
    # return results.json()
    return result_schema.jsonify(new_result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
