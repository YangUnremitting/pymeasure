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

from pymeasure.instruments import Instrument, RangeException
from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.validators import truncated_range, strict_discrete_set
import numpy as np

class Keithley2420(Instrument):
    """ Represents the Keithely 2400 SourceMeter and provides a
    high-level interface for interacting with the instrument.

    .. code-block:: python

        keithley = Keithley2400("GPIB::1")

        keithley.apply_current()                # Sets up to source current
        keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
        keithley.compliance_voltage = 10        # Sets the compliance voltage to 10 V
        keithley.source_current = 0             # Sets the source current to 0 mA
        keithley.enable_source()                # Enables the source output

        keithley.measure_voltage()              # Sets up to measure voltage

        keithley.ramp_to_current(5e-3)          # Ramps the current to 5 mA
        print(keithley.voltage)                 # Prints the voltage in Volts

        keithley.shutdown()                     # Ramps the current to 0 mA and disables output

    """

    def __init__(self, adapter, **kwargs):
        super(Keithley2420, self).__init__(
            adapter, "Keithley 2400 SourceMeter", **kwargs
        )

    config_measurement = Instrument.control(
        ":CONF?", ":CONF:%s",
        """ Configures the instrument to a specific setup for measurements on the specified function""",
        validator= strict_discrete_set,        
        values={"Amps": "CURR:DC",
                "Volts": "VOLT:DC",
                "Ohms": "RES"},
        map_values=True
    )

    count = Instrument.control(
        "COUN?", "COUN %d",
        """ This command is used to specify how many times an operations perofmed in the specified layer of the trigger model""",
        validator=truncated_range,
        values=[1, 2500]
    )

    buffer_points = Instrument.control(
        ":TRAC:POIN?", ":TRAC:POIN %d",
        """ An integer property that controls the number of buffer points. This
        does not represent actual points in the buffer, but the configuration
        value instead. """,
        validator=truncated_range,
        values=[1, 2500]
    )
    
    def initiate(self):
        """ A property that allow user to set the awaiting trigger state. """
        self.write(":INIT")

    def abort(self):
        """ Reset trigger system. Goes to idle state. """
        self.write(":ABOR")

    def get_data(self):
        """ Get data from keithly store """
        return np.array(self.values(":TRAC:DATA?"), dtype=np.float64)

    def is_buffer_full(self):
        """ Returns True if the buffer is full of measurements. """
        status_bit = int(self.ask("*STB?"))
        return status_bit == 65