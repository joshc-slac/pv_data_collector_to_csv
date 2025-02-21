from epics import caget
import numpy as np
import time

if __name__ == "__main__":
  power_meter_mv = "PF1K0:PPM:VOLT_RBV"
  gmd_mJ = "GMD:PV"
  x_gmd_mJ = "x_GMD:PV"
  data = np.array((1000, 4))

  idx = 0
  elapsed = 0
  current_time = time.now()
  while(True):
    loop_start = current_time
    data[idx, 0] = current_time
    data[idx, 1] = caget(power_meter_mv)
    data[idx, 2] = caget(gmd_mJ)
    data[idx, 3] = caget(x_gmd_mJ)
    idx += 1

    current_time = time.now()
    # wait till 100ms have elapsed
    while(elapsed < 0.1)
      elapsed = time.now() - loop_start


