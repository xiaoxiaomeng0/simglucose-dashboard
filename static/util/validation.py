from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class SimulationForm(FlaskForm):
    sim-time = IntegerField(
        "Input Simulation Time: ",
        validators=[DataRequired(),
                    NumberRange(min=6, max=24, message="The simulation time must between 6 to 24")])
    random-seed = IntegerField(
        "Input random seed for random scenario:",
        validators=[DataRequired(),
                    NumberRange(min=1, message="The random seed must be greater than 0")])
    breakfast-time = IntegerField(
        "Breakfast Time (hr)",
        validators=[]
    )
