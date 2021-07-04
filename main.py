from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from static.util.catch_keyerror import catch_keyerror
from static.util.selection import select_path, select_animate, select_parallel, select_scenario, build_env, select_controller
# from simglucose.simulation.user_interface import build_envs
from simglucose.simulation.sim_engine import SimObj, batch_sim
from simglucose.analysis.report import report
from datetime import timedelta
import copy
import pkg_resources
import pandas as pd


PATIENT_PARA_FILE = pkg_resources.resource_filename(
    'simglucose', 'params/vpatient_params.csv')
patient_params = pd.read_csv(PATIENT_PARA_FILE)


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simulate", methods=["GET", "POST"])
def simulate():
    if request.method == "POST":
        sim_time = timedelta(float(request.form["sim-time"]))
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
        results = batch_sim(sim_instances, parallel=parallel)

        df = pd.concat(
            results, keys=[s.env.patient.name for s in sim_instances])
        results, ri_per_hour, zone_stats, figs, axes = report(df, save_path)
        return redirect("/")

    return render_template("start_simulate.html", patient_names=patient_params["Name"].values)


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
