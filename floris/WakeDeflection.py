"""
Copyright 2017 NREL

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

from BaseObject import BaseObject
import numpy as np


class WakeDeflection(BaseObject):

    def __init__(self, typeString):
        super().__init__()
        self.typeString = typeString

        typeMap = {
            "jimenez": self._jimenez
        }
        self.function = typeMap.get(self.typeString, None)

        # to be specified in user input
        self.kd = .17 # wake deflection
        self.ad = -4.5
        self.bd = -0.01

    def _jimenez(self, x_locations, turbine, coord):
        # this function defines the angle at which the wake deflects in relation to the yaw of the turbine
        # this is coded as defined in the Jimenez et. al. paper

        kd = 0.17
        ad = -4.5
        bd = -0.01

        # angle of deflection
        xi_init = (1. / 2.) * np.cos(turbine.yawAngle) * np.sin(turbine.yawAngle) * turbine.Ct
        # xi = xi_init / (1 + 2 * kd * x_locations / turbine.rotorDiameter)**2
        
        x_locations = x_locations - coord.x

        # yaw displacement
        yYaw_init = ( xi_init
            * ( 15 * (2 * kd * x_locations / turbine.rotorDiameter + 1)**4. + xi_init**2. )
            / ((30 * kd / turbine.rotorDiameter) * (2 * kd * x_locations / turbine.rotorDiameter + 1)**5.)) \
            - (xi_init * turbine.rotorDiameter * (15 + xi_init**2.) / (30 * kd))

        # corrected yaw displacement with lateral offset
        yYaw = yYaw_init + ad + bd * x_locations

        return yYaw