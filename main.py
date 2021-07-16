from flask import Flask, render_template, url_for, request, redirect, jsonify
# from static.util.catch_keyerror import catch_keyerror
from static.util.selection import select_path, select_animate, select_parallel, select_scenario, build_env, select_controller, select_patient
from sim_engine import SimObj, batch_sim
from models import Result, db, app, ResultSchema, Experiment, User
from datetime import timedelta
import copy
import pkg_resources
import pandas as pd
import platform

# Init schema
result_schema = ResultSchema()
results_schema = ResultSchema(many=True)


PATIENT_PARA_FILE = pkg_resources.resource_filename(
    'simglucose', 'params/vpatient_params.csv')
patient_params = pd.read_csv(PATIENT_PARA_FILE)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/results")
def show_all_results():
    all_results = Result.query.all()
    return results_schema.jsonify(all_results)


@app.route("/simulate", methods=["GET", "POST"])
def simulate():
    if request.method == "POST":
        sim_time = timedelta(hours=float(request.form["sim-time"]))
        scenario, start_time = select_scenario()
        controller = select_controller()
        save_path = select_path()
        animate = select_animate()
        parallel = select_parallel()
        envs = build_env(scenario, start_time)
        ctrllers = [copy.deepcopy(controller) for _ in range(len(envs))]
        sim_instances = [SimObj(e,
                                c,
                                sim_time,
                                animate=animate,
                                path=save_path) for (e, c) in zip(envs, ctrllers)]
        batch_sim(sim_instances, parallel=parallel)

        # df = pd.concat(
        #     results, keys=[s.env.patient.name for s in sim_instances])
        # print(df)
        # report(df, save_path)
        return redirect(url_for("show_all_results"))

    return render_template("start_simulate.html", patient_names=patient_params["Name"].values, system=platform.system())


@app.route("/test")
def test():
    return render_template("test.html", system=platform.system())


@app.route("/view")
def view_result():
    return "None."


if __name__ == "__main__":
    app.run(debug=True, port=5000)
