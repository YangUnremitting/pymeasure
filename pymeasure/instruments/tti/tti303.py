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

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set
from pyvisa.errors import VisaIOError

class TTi303(Instrument):
    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "Power supply",
            **kwargs
        )
    
    master_voltage = Instrument.control(
        "V1?", "V1 %g",
        """ Set the master output voltage""",
        validator=truncated_range,
        values=[0, 30]
    )

    master_current = Instrument.control(
        "I1?", "I1 %g",
        """ Set the master output current""",
        validator=truncated_range,
        values=[0, 3030]
    )

    slave_voltage = Instrument.control(
        "V2?", "V2 %g",
        """ Set the slave output voltage""",
        validator=truncated_range,
        values=[0, 30]
    )

    slave_current = Instrument.control(
        "I2?", "I2 %g",
        """ Set the slave output current""",
        validator=truncated_range,
        values=[0, 3030]
    )

    address = Instrument.measurement(
        "ADDRESS?",
        """ Returns the bus address of the instrument; This is the address used by GPIB, 
        if fitted, or may be used as a general identifier over the other interfaces."""
    )
    