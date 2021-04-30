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

import pyvisa
import time

class Keithley6430():
    def __init__(self, resourceName):
        self.rm = pyvisa.ResourceManager()
        self.keithley = self.rm.open_resource(resourceName)

    def status(self):
        measurement_even = self.keithley.query(":STAT:MEAS:COND?")
        return int(measurement_even)

    def trigger(self):
        self.keithley.write(":TRAC:CLE;         \
                        :SOUR:FUNC VOLT;        \
                        :SENS:FUNC 'CURR';      \
                        :SENS:VOLT:NPLC 1;      \
                        :DISP:DIG 7;            \
                        :FORM:ELEM CURR;        \
                        :TRAC:POIN 100;         \
                        :TRIG:COUN 100;         \
                        :TRAC:FEED SENS;        \
                        :TRAC:FEED:CONT NEXT;   \
                        :OUTP ON;               \
                        :INIT;")
        time.sleep(1)

    def check_status(self):
        if self.status() < 768:
            return False
        else:
            return True
    
    def get_buffer(self):
        voltage = self.keithley.query_ascii_values("TRAC:DATA?")
        avg_voltage = sum(voltage) / len(voltage)
        # print("Average voltage ({}): {}".format(len(voltage), avg_voltage))
        return avg_voltage

    def disable_source(self):
        self.keithley.write(":OUTP OFF")

# keithley = Keithley6430("GPIB0::13")
# keithley.trigger()
# status = keithley.check_status()
# print("Keithley6430 Voltage Meter Status: ", status)

# while  not keithley.check_status():
#     print("Channel Voltage measuring ...")
#     time.sleep(1)
# keithley.disable_source()
# print("Channel Voltage: ", keithley.get_buffer())
# print("Measurement Done")