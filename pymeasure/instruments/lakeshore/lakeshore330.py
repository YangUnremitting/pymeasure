#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2020 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from time import sleep, time

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set

class LakeShore330(Instrument):
    """ Represents the Lake Shore 331 Temperature Controller and provides
    a high-level interface for interacting with the instrument.

    .. code-block:: python

        controller = LakeShore330("GPIB::1")

        print(controller.setpoint)        # Print the current setpoint for loop 1
        controller.setpoint = 50          # Change the setpoint to 50 K
        controller.heater_range = 'low'     # Change the heater range to Low
        controller.wait_for_temperature()   # Wait for the temperature to stabilize
        print(controller.temperature_A)     # Print the temperature at sensor A

    """
    def __init__(self, adapter, **kwargs):
        super(LakeShore330, self).__init__(
            adapter,
            "Lake Shore 331 Temperature Controller",
            **kwargs
        )

    temperature_A = Instrument.measurement(
        "KRDG? A",
        """ Reads the temperature of the sensor A in Kelvin. """
    )

    setpoint = Instrument.control(
        "SETP?", "SETP %g",
        """ A floating point property that controls the setpoint temperature
        in Kelvin. """,
        validator=truncated_range,
        values=[0, 475]      
    )

    heater_range = Instrument.control(
        "RANG?", "RANG %d",
        """ A string property that controls the heater range, which
        can take the values: off, low, medium, and high. These values
        correlate to 0, 0.5, 5 and 50 W respectively. """,
        validator=strict_discrete_set,
        values={'off':0, 'low':1, 'medium':2, 'high':3},
        map_values=True
    )

    auto_tune = Instrument.control(
        "TUNE?", "TUNE %d",
        """ Sets autotuning status: 0 = Manual, 1 = P, 2 = PI, 3 = PID, 4 = Zone""",
        validator=strict_discrete_set,
        values={'Manual':0, 'P':1, 'PI':2, 'PID':3, 'Zone': 4},
        map_values=True
    )

    gain = Instrument.control(
        "GAIN?", "GAIN %d",
        """ Gain corresponds to the proportional (P) portion of the PID autotuning control algorithm""",
        validator=truncated_range,
        values=[0, 999]
    )

    reset = Instrument.control(
        "RSET?", "RSET %d",
        """ Gain corresponds to the integral (I) portion of the PID autotuning control algorithm""",
        validator=truncated_range,
        values=[0, 999]
    )

    rate = Instrument.control(
        "RATE?", "RATE %d",
        """ Gain corresponds to the differential (D) portion of the PID autotuning control algorithm""",
        validator=truncated_range,
        values=[0, 999]
    )