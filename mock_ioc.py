#!/usr/bin/env python3
from random import random
from textwrap import dedent

from caproto.server import PVGroup, ioc_arg_parser, pvproperty, run


class MockIML20(PVGroup):
    """
    # An IOC with three uncoupled read/writable PVs.

    # Scalar PVs:
        * IM2L0:XTES:CLZ.RBV - Zoom motor percentage of actuation
        * IM2L0:XTES:CLF.RBV - Focus motor percentage of actuation
    * Enum PVs:
        * IM2L0:XTES:MMS:STATE:GET_RBV - enumerated state of imager target
        * IM2L0:XTES:MFW:GET_RBV - enumerated state of filter wheel "actuation"
    ----------
    """

    ppm_keithly = pvproperty(
        name="IM3L0:PPM:SPM:K2700:Reading",
        value=0.0,
        dtype=float,
        doc="Volt rbv",
    )
    ppm_volt_rbv = pvproperty(
        name="IM3L0:PPM:SPM:VOLT_RBV",
        value=0,
        dtype=float,
        doc="Represents GMD",
    )
    gdet1 = pvproperty(
        name="GDET:FEE1:241:ENRC",
        value=0,
        dtype=float,
        doc="Represents XGMD",
    )
    gdet2 = pvproperty(
        name="GDET:FEE1:242:ENRC",
        value=0,
        dtype=float,
        doc="Represents XGMD",
    )
    gdet3 = pvproperty(
        name="GDET:FEE1:361:ENRC",
        value=0,
        dtype=float,
        doc="Represents XGMD",
    )
    gdet4 = pvproperty(
        name="GDET:FEE1:362:ENRC",
        value=0,
        dtype=float,
        doc="Represents XGMD",
    )
    
    @ppm_keithly.startup
    async def ppm_keithly(self, instance, async_lib):
        while True:
            x = self.ppm_keithly.value + 1
            print(x)
            await instance.write(value=x)

            await async_lib.library.sleep(1)


if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix="",
        desc=dedent(MockIML20.__doc__)
    )
    ioc = MockIML20(**ioc_options)
    run(ioc.pvdb, **run_options)
