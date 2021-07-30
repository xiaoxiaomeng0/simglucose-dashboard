import datetime
from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
from flask_login.utils import login_required
import requests
# from static.util.catch_keyerror import catch_keyerror
from static.util.selection import select_path, select_animate, select_parallel, select_scenario, build_env, select_controller, select_patient
from sim_engine import SimObj, batch_sim
from models import Result, db, app, ResultSchema, Experiment, User
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
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


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = generate_password_hash(
            register_form.password.data, salt_length=8)
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Username Taken, please try another name!")
            return redirect(url_for("login"))
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("simulate"))
    return render_template("register.html", form=register_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("simulate"))
            flash("Username and password does not match!")
            return redirect(url_for("login"))
        flash("Username does not exist, please register!")
        return redirect(url_for("register"))
    return render_template("login.html", form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/all_results")
def show_all_results():
    all_results = Result.query.all()
    return results_schema.jsonify(all_results)


@app.route("/results/<experiment_name>")
def show_curr_experiment_results(experiment_name):
    curr_experiment = Experiment.query.filter_by(
        experiment_name=experiment_name).first()
    all_results = Result.query.filter_by(
        experiment_id=curr_experiment.id).all()
    return results_schema.jsonify(all_results)


@app.route("/simulate", methods=["GET", "POST"])
@login_required
def simulate():
    if request.method == "POST":
        print(request.form)
        experiment_name = request.form["experiment_name"]

        time = datetime.now()
        new_experiment = Experiment(
            experiment_name=experiment_name, time=time, user_id=current_user.id)
        db.session.add(new_experiment)
        db.session.commit()
        sim_time = timedelta(hours=float(request.form["sim_time"]))
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
        batch_sim(sim_instances, experiment_name, parallel=parallel)

        return jsonify({"experiment_name": experiment_name})

    return render_template("start_simulate.html", patient_names=patient_params["Name"].values, system=platform.system())


@app.route("/test")
def test():
    return render_template("test.html", system=platform.system())


@app.route("/view")
def view_result():
    return render_template("view.html")


if __name__ == "__main__":
    app.run(debug=True, port=5004)
