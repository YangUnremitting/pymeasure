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

# import logging
# log = logging.getLogger(__name__)
# log.addHandler(logging.NullHandler())

# from pymeasure.instruments import Instrument, RangeException
# from pymeasure.adapters import PrologixAdapter
# from pymeasure.instruments.validators import truncated_range, strict_discrete_set

# class Keithley2182A(Instrument):
#     def __init__(self, adapter, **kwargs):
#         super(Keithley2182A, self).__init__(
#             adapter, "Keithley 2182A Nanovolmeter", includeSCPI=False, **kwargs
#         )

#     #################
#     # Sense command #
#     #################
#     measurement = Instrument.control(
#         ":SENS:FUNC?", ":SENS:FUNC %s",
#         """ Select the measurement function.""",
#         validator=strict_discrete_set,
#         values={"Voltage": "'VOLT'",
#                 "Temperature": "'TEMP'"},
#         map_values=True
#     )

#     channel = Instrument.control(
#         ":SENS:CHAN?", ":SENS:CHAN %d",
#         """ Select channel to measure; 0, 1 or 2 (0 = internal temperature sensor).""",
#         validator=strict_discrete_set,
#         values=[0, 1, 2],
#         map_values=True
#     )

#     read_instrument = Instrument.measurement(
#         ":SENS:DATA?",
#         """ Return the last instrument reading."""
#     )

#     read = Instrument.measurement(
#         ":SENS:DATA:FRES?",
#         """ Return a new (fresh) reading."""
#     )

#     #################
#     # Trace command #
#     #################
#     def get_data(self):
#         """ Read the contents of the buffer data store. """
#         datas = self.values(":TRAC:DATA?")
#         return datas

#     def buffer_clear(self):
#         """ Clear reading s form buffer."""
#         self.write(":TRAC:CLE")

#     buffer_size = Instrument.control(
#         ":TRAC:POIN?", ":TRAC:POIN %d",
#         """ Specify size of buffer; 2 to 1024.""",
#         validator=truncated_range,
#         values=[2, 1024]
#     )

#     buffer_source = Instrument.control(
#         ":TRAC:FEED?", ":TRAC:FEED %s",
#         """ Select source of readings for buffer; SENSe[1], CALCulate[1], or NONE.""",
#         validator=strict_discrete_set,
#         values={"Sense": "SENS", 
#                 "Calculate": "CALC", 
#                 "None": "NONE"},
#         map_values=True
#     )

#     buffer_control = Instrument.control(
#         ":TRAC:FEED:CONT?", ":TRAC:FEED:CONT %s",
#         """ Select buffer control mode (NEXT or NEVer).""",
#         validator=strict_discrete_set,
#         values={"Start": "NEXT",
#                 "Stop": "NEV"},
#         map_values=True
#     )

#     ###################
#     # Trigger command #
#     ###################
#     initiate = Instrument.control(
#         ":INIT:CONT?", ":INIT:CONT %d",
#         """ Enbale or disable continuous initiation.""",
#         validator=strict_discrete_set,
#         values={"Enable": 1,
#                 "Disable": 0},
#         map_values=True
#     )

#     ####################
#     # Status subsystem #
#     ####################
#     def reading_avaiable(self):
#         """ Query commands to read the event register."""
#         even = self.values(":STAT:MEAS?")
#         if even[0] == 32:
#             return False
#         else:
#             return True

##########################################################################################################################
# Above code is not working when includeSCPI=True and with includeSCPI=False, cannot get the buffer data greater than 10 #
##########################################################################################################################

import pyvisa
import time

class Keithley2182A():
    def __init__(self, resourceName):
        self.rm = pyvisa.ResourceManager()
        self.keithley = self.rm.open_resource(resourceName)

    def status(self):
        measurement_even = self.keithley.query(":STAT:MEAS:COND?")
        return int(measurement_even)

    def trigger(self):
        self.keithley.write(":TRAC:CLE;         \
                        :SENS:FUNC 'VOLT';      \
                        :TRAC:POIN 100;         \
                        :TRAC:FEED:CONT NEXT;   \
                        :TRAC:FEED SENS;        \
                        :INIT:CONT 1")
        time.sleep(1)

    def check_status(self):
        if self.status() < 896:
            return False
        else:
            return True

    def get_buffer(self):
        voltage = self.keithley.query_ascii_values("TRAC:DATA?")
        return voltage