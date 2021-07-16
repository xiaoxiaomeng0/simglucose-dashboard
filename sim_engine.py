from models import Result, db, app, ResultSchema
import logging
import time
import os


pathos = True
try:
    from pathos.multiprocessing import ProcessPool as Pool
except ImportError:
    print('You could install pathos to enable parallel simulation.')
    pathos = False

logger = logging.getLogger(__name__)


class SimObj(object):
    def __init__(self,
                 env,
                 controller,
                 sim_time,
                 animate=True,
                 path=None):
        self.env = env
        self.controller = controller
        self.sim_time = sim_time
        self.animate = animate
        self._ctrller_kwargs = None
        self.path = path

    def simulate(self):
        obs, reward, done, info = self.env.reset()
        while self.env.time < self.env.scenario.start_time + self.sim_time:
            action = self.controller.policy(obs, reward, done, **info)
            new_result = Result(patient_id=info["patient_name"],
                                time=self.env.time,
                                reward=reward,
                                cgm=obs.CGM,
                                cho=info["meal"],
                                insulin=action.basal + action.bolus,
                                bg=info["bg"],
                                lbgi=info["lbgi"],
                                hbgi=info["hbgi"],
                                risk=info["risk"])
            db.session.add(new_result)
            db.session.commit()
            obs, reward, done, info = self.env.step(action)

    def reset(self):
        self.env.reset()
        self.controller.reset()


def batch_sim(sim_instances, parallel=False):
    tic = time.time()
    if parallel and pathos:
        with Pool() as p:
            results = p.map(sim, sim_instances)
    else:
        if parallel and not pathos:
            print('Simulation is using single process even though parallel=True.')
        results = [s.simulate() for s in sim_instances]
    toc = time.time()
    print('Simulation took {} sec.'.format(toc - tic))
    return results
