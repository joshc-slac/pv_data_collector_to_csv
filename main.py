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
    def __init__(self, run_time=60, sample_period_s=0.1):
        self.pv_dict = {
            "ppm_keithly": "IM3L0:PPM:SPM:K2700:Reading",
            "ppm_volt_rbv": "IM3L0:PPM:SPM:VOLT_RBV",
            "gdet1": "GDET:FEE1:241:ENRC",
            "gdet2": "GDET:FEE1:242:ENRC",
            "gdet3": "GDET:FEE1:361:ENRC",
            "gdet4": "GDET:FEE1:362:ENRC"
        }
        self.run_time = run_time
        self.sample_period_s = sample_period_s
        self.num_samps = int(run_time * 1.0 / sample_period_s) + 1

        # Make space for PVs + Timestamp
        self.data = np.zeros((self.num_samps, len(self.pv_dict)+1))
        # Add time to column names
        self.colums = list(self.pv_dict.keys())
        self.colums.insert(0, "Time")
        
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
        start_time = time.time()
        current_time = start_time
        while (self.do_work.value and 
               (current_time - start_time) < self.run_time):
            loop_start = current_time
            print(idx)
            self.data[idx, 0] = current_time - start_time
            # iterate through keys
            i = 1
            for key, value in self.pv_dict.items():
                self.data[idx, i] = caget(value)
                i += 1
            idx += 1

            # wait till 100ms have elapsed
            elapsed = 0
            while (elapsed < self.sample_period_s):
                elapsed = time.time() - loop_start
            
            current_time = time.time()

        self.do_work.value = False


def sigint_handler(signum, frame, obj):
    obj.stop_work()


if __name__ == "__main__":
    dc = DataCollector(60, 0.1)
    dc.start_work()
    signal.signal(signal.SIGINT, partial(sigint_handler, obj=dc))

    while (dc.do_work.value):
        time.sleep(.1)

    logging.debug("Writing to df...")
    # Create dataframe
    df = pd.DataFrame(data=dc.data,
                      columns=dc.colums)
    df.to_csv("eggs.csv")
