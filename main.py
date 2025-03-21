import signal
from epics import caget
import numpy as np
import pandas as pd
import time
from multiprocessing import Value
from threading import Thread
from ctypes import c_bool
import logging
from functools import partial


class DataCollector():
    def __init__(self):
        self.pv_dict = {
            "ppm_keithly": "IM3L0:PPM:SPM:K2700:Reading",
            "ppm_volt_rbv": "IM3L0:PPM:SPM:VOLT_RBV",
            "gdet1": "GDET:FEE1:241:ENRC",
            "gdet2": "GDET:FEE1:242:ENRC",
            "gdet3": "GDET:FEE1:361:ENRC",
            "gdet4": "GDET:FEE1:362:ENRC"
        }

        # Make space for PVs + Timestamp
        self.data = np.zeros((1000, len(self.pv_dict)+1))
        # Add time to column names
        colums = list(self.pv_dict.keys())
        colums.insert(0, "Time")

        # Create dataframe
        self.df = pd.DataFrame(data=self.data,
                               columns=colums)
        
        # Worker related variables
        self.do_work = Value(c_bool, False)
        self.thread = Thread(target=self.work_func)

    def start_work(self):
        if (self.do_work.value):
            logging.error("Work thread already started")
            return

        self.thread = Thread(target=self.work_func)
        self.do_work.value = True
        self.thread.start()
        logging.debug("Work thread spawned")

    def stop_work(self):
        if (not self.do_work.value):
            logging.error("Work thread not working doing nothing")
            return
        self.do_work.value = False
        self.thread.join()
        logging.debug("Work thread joined")

    def work_func(self):
        idx = 0
        elapsed = 0
        current_time = time.time()
        while (self.do_work.value):
            loop_start = current_time
            self.data[idx, 0] = current_time
            # iterate through keys
            i = 1
            for key, value in self.pv_dict.items():
                self.data[idx, i] = caget(value)
                i += 1
            idx += 1

            current_time = time.time()
            # wait till 100ms have elapsed
            while (elapsed < 0.1):
                elapsed = time.time() - loop_start


def sigint_handler(signum, frame, obj):
    obj.stop_work()


if __name__ == "__main__":
    dc = DataCollector()
    dc.start_work()
    signal.signal(signal.SIGINT, partial(sigint_handler, obj=dc))

    while (dc.do_work.value):
        time.sleep(1)
