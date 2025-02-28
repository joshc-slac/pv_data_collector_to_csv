import signal
from epics import caget
import numpy as np
import pandas as pd
import time
from threading import Value, Thread
from ctypes import c_bool
import logging


class DataCollector():
    def __init__(self):
        self.power_meter_mv = "PF1K0:PPM:VOLT_RBV"
        self.gmd_mJ = "GMD:PV"
        self.x_gmd_mJ = "x_GMD:PV"
        data = np.zeros((1000, 4))  # make arg parse-able
        colums = ["Time", "PM", "GMD", "xGMD"]
        self.df = pd.DataFrame(data, colums)
        self.do_work = Value(c_bool, False)
        self.thread = None

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
        current_time = time.now()
        while (self.do_work.value):
            loop_start = current_time
            self.df[idx, "Time"] = current_time
            self.df[idx, "PM"] = caget(self.power_meter_mv)
            self.df[idx, "GMD"] = caget(self.gmd_mJ)
            self.df[idx, "xGMD"] = caget(self.x_gmd_mJ)
            idx += 1

            current_time = time.now()
            # wait till 100ms have elapsed
            while (elapsed < 0.1):
                elapsed = time.now() - loop_start


if __name__ == "__main__":
    dc = DataCollector()
    signal.signal(signal.SIGINT, dc.stop_work())
    time.sleep(1)