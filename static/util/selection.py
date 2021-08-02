import pkg_resources
import pandas as pd
from simglucose.controller.basal_bolus_ctrller import BBController
from werkzeug.wrappers import request
from flask import request
from simglucose.simulation.scenario_gen import RandomScenario
from simglucose.simulation.scenario import CustomScenario
from simglucose.sensor.cgm import CGMSensor
from simglucose.actuator.pump import InsulinPump
from simglucose.patient.t1dpatient import T1DPatient
from simglucose.simulation.env import T1DSimEnv
from datetime import datetime, timedelta
import os
import copy
import json
import numpy


PATIENT_PARA_FILE = pkg_resources.resource_filename(
    'simglucose', 'params/vpatient_params.csv')


def str2bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError(f"{s} cannot be converted to boolean.")


def parsetime(s, period):
    date = datetime.now().date()
    s = str(date) + " " + s + period
    datetime_object = datetime.strptime(s, "%Y-%m-%d %I:%M%p")
    return datetime_object


def select_scenario():
    sim_start_hour = request.form["start_hour"]
    sim_start_period = request.form["start_period"]
    if sim_start_period == "AM":
        convert_time = timedelta(hours=float(sim_start_hour.split(":")[0]))
    else:
        convert_time = timedelta(
            hours=(float(sim_start_hour.split(":")[0]) + 12))

    start_time = datetime.combine(datetime.now().date(),
                                  datetime.min.time()) + convert_time

    scenario_select = request.form["scenario"]
    if scenario_select == "1":
        rand_scenario_seed = int(
            request.form["random_seed"])
        scenario = RandomScenario(
            start_time=start_time, seed=rand_scenario_seed)
    elif scenario_select == "2":
        scenario_tuple = []
        breakfast_time = request.form.get("breakfast-time", None)
        breakfast_period = request.form.get("breakfast-period", None)
        breakfast_size = request.form.get("breakfast-size", None)
        if breakfast_time and breakfast_size:
            scenario_tuple.append(
                (parsetime(breakfast_time, breakfast_period), float(breakfast_size)))

        lunch_time = request.form.get("lunch-time", None)
        lunch_period = request.form.get("lunch-period", None)
        lunch_size = request.form.get("lunch-size", None)
        if lunch_time and lunch_size:
            scenario_tuple.append(
                (parsetime(lunch_time, lunch_period), float(lunch_size)))

        dinner_time = request.form.get("dinner-time", None)
        dinner_period = request.form.get("dinner-period", None)
        dinner_size = request.form.get("dinner-size", None)
        if dinner_time and dinner_size:
            scenario_tuple.append(
                (parsetime(dinner_time, dinner_period), float(dinner_size)))

        snack_time = request.form.get("snack-time", None)
        snack_period = request.form.get("snack-period", None)
        snack_size = request.form.get("snack-size", None)
        if snack_time and snack_size:
            scenario_tuple.append(
                (parsetime(snack_time, snack_period), float(snack_size)))

        scenario = CustomScenario(
            start_time=start_time, scenario=scenario_tuple)
    return scenario, start_time


def select_path():
    path = request.form["path"]
    if path == "custom":
        save_path = request.form["custom-path-input"]
    elif path == "default" or path == "":
        foldername = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_path = os.path.join(os.path.abspath('./results/'), foldername)
    return save_path


def select_controller():
    controller = request.form["controller"]
    if controller == "basal-bolus":
        controller = BBController()
    return controller


def select_patient():
    adults = request.form.get("adults", None)
    adolescents = request.form.get("adolescents", None)
    children = request.form.get("children", None)
    custom_patient = request.form.get("patientID", None)
    patient_params = pd.read_csv(PATIENT_PARA_FILE)
    all_patient_names = list(patient_params["Name"].values)
    patients = []
    if adolescents:
        patients = all_patient_names[0:10]
    if adults:
        patients = all_patient_names[10:20]
    if children:
        patients = all_patient_names[20:30]
    if custom_patient:
        custom_patients = json.loads(custom_patient)
        patients.extend(custom_patients)
    return patients


def select_animate():
    animate = request.form["animate"]
    animate = str2bool(animate)
    return animate


def select_parallel():
    parallel = request.form["parallel"]
    parallel = str2bool(parallel)
    return parallel


def build_env(scenario, start_time):
    patient_names = select_patient()
    cgm_sensor_name = request.form["sensor"]
    cgm_seed = int(request.form["seed_noise"])
    insulin_pump_name = request.form["pump"]

    def local_build_env(pname):
        patient = T1DPatient.withName(pname)
        cgm_sensor = CGMSensor.withName(cgm_sensor_name, seed=cgm_seed)
        insulin_pump = InsulinPump.withName(insulin_pump_name)
        scen = copy.deepcopy(scenario)
        env = T1DSimEnv(patient, cgm_sensor, insulin_pump, scen)
        return env

    envs = [local_build_env(p) for p in patient_names]
    return envs
