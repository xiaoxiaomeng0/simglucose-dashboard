
import flask
from flask import request, jsonify

import psycopg2
from psycopg2 import Error

app = flask.Flask(__name__)
app.config["DEBUG"] = True


try:
    # Connect to an existing database
    connection = psycopg2.connect(user="meng",password="IAOeng19910804",database="simglucose")

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404


    @app.route('/simglucose/results/', methods=['GET'])
    def get():
        query_parameters = request.args

        # Connect to an existing database
        connection = psycopg2.connect(user="meng",password="IAOeng19910804",database="simglucose")

    # Create a cursor to perform database operations
        cursor = connection.cursor()

        # time = query_parameters.get('time')
        # bg = query_parameters.get('bg')
        # cgm = query_parameters.get('cgm')
        # cho = query_parameters.get('cho')
        # insulin = query_parameters.get('insulin')
        # lbgi = query_parameters.get('lbgi')
        # hbgi = query_parameters.get('hbgi')
        # risk = query_parameters.get('risk')
        patient_id = query_parameters.get('patient_id')

        query = "SELECT * FROM results WHERE"

        # if time:
        #     query += ' time=(%s) AND'
        #     to_filter.append(str(time))
        # if bg:
        #     query += ' bg=(%s) AND'
        #     to_filter.append(str(bg))
        # if cgm:
        #     query += ' cgm=(%s) AND'
        #     to_filter.append(str(cgm))
        # if cho:
        #     query += ' cho=(%s) AND'
        #     to_filter.append(str(cho))
        # if insulin:
        #     query += ' insulin=(%s) AND'
        #     to_filter.append(str(insulin))
        # if lbgi:
        #     query += ' lbgi=(%s) AND'
        #     to_filter.append(str(lbgi))
        # if hbgi:
        #     query += ' hbgi=(%s) AND'
        #     to_filter.append(str(hbgi))
        # if risk:
        #     query += ' risk=(%s) AND'
        #     to_filter.append(str(risk))
        if patient_id:
            query += f" patient_id='{patient_id}' AND"
        # if not (time or bg or cgm or cho or insulin or lbgi or hbgi or risk or patient_id):
        #     return page_not_found(404)
        if not patient_id:
            return page_not_found(404)

        query = query[:-4] + ';'

        cursor.execute(query)
        results = cursor.fetchall()

        return jsonify(results)
        
    connection.commit()
    app.run()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
