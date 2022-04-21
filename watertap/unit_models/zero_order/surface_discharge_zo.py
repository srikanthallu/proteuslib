###############################################################################
# WaterTAP Copyright (c) 2021, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory, Oak Ridge National
# Laboratory, National Renewable Energy Laboratory, and National Energy
# Technology Laboratory (subject to receipt of any required approvals from
# the U.S. Dept. of Energy). All rights reserved.
#
# Please see the files COPYRIGHT.md and LICENSE.md for full copyright and license
# information, respectively. These files are also available online at the URL
# "https://github.com/watertap-org/watertap/"
#
###############################################################################
"""
This module contains a zero-order representation of a surface discharge unit
operation.
"""

from pyomo.environ import Constraint, Reference, units as pyunits, Var
from idaes.core import declare_process_block_class

from watertap.core import build_pt, pump_electricity, ZeroOrderBaseData

# Some more information about this module
__author__ = "Travis Arnold"


@declare_process_block_class("SurfaceDischargeZO")
class SurfaceDischargeData(ZeroOrderBaseData):
    """
    Zero-Order model for a surface discharge unit operation.
    """

    CONFIG = ZeroOrderBaseData.CONFIG()

    def build(self):
        super().build()

        self._tech_type = "surface_discharge"
        build_pt(self)
        self._Q = Reference(self.properties[:].flow_vol)

        pump_electricity(self, self._Q)

        self.pipe_distance = Var(
            self.flowsheet().config.time, units=pyunits.miles, doc="Piping distance"
        )

        self.pipe_diameter = Var(
            self.flowsheet().config.time, units=pyunits.inches, doc="Pipe diameter"
        )

        self._fixed_perf_vars.append(self.pipe_distance)
        self._fixed_perf_vars.append(self.pipe_diameter)

        self._perf_var_dict["Pipe Distance"] = self.pipe_distance
        self._perf_var_dict["Pipe Diameter"] = self.pipe_diameter