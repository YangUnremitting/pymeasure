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

buffers = {"Buffer1": "BUF1", "Buffer2": "BUF2", "Buffer3": "BUF3"}

class LI5640(Instrument):

    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "NF Lock-In Amplifier LI5640",
            **kwargs
        )

    ######################################
    # Reference system, 09 March 2021 #
    ######################################
    phase = Instrument.control(
        "PHAS?","PHAS %g",
        """ Setting and query of phase offset""",
        validator=truncated_range,
        values=[-180, 179.99]
    )

    frequency = Instrument.control(
        "FREQ?","FREQ %g",
        """ Setting and query of internal-oscillator frequency""",
        validator=truncated_range,
        values=[0.0005, 105.00]
    )

    amplitude_50mV = Instrument.control(
        "AMPL?","AMPL %g, 0",
        """ Setting and query of internal-oscillator frequency""",
        validator=truncated_range,
        values=[0.0, 50.0]
    )

    amplitude_500mV = Instrument.control(
        "AMPL?","AMPL %g, 1",
        """ Setting and query of internal-oscillator frequency""",
        validator=truncated_range,
        values=[0.0, 500.0]
    )

    amplitude_5V = Instrument.control(
        "AMPL?","AMPL %g, 2",
        """ Setting and query of internal-oscillator frequency""",
        validator=truncated_range,
        values=[0.0, 5]
    )

    harmonic = Instrument.control(
        "HARM?","HARM %d",
        """ Setting and query of internal-oscillator frequency""",
        validator=truncated_range,
        values=[1, 19999]
    )

    source = Instrument.control(
        "RSRC?", "RSRC %d",
        """ Setting and query of refference signal.""",
        validator=strict_discrete_set,
        values={"Ref": 0,
                "Int": 1,
                "Signal": 2},
        map_values=True
    )

    edge = Instrument.control(
        "REDG?", "REDG %d",
        """ Setting and query of reference signal synchoronous edge""",
        validator=strict_discrete_set,
        values={"Sine": 0,
                "TTLP": 1,
                "TTLN": 2},
        map_values=True
    )

    ###########################################
    # Messages of Signal Input, 09 March 2021 #
    ###########################################
    signal = Instrument.control(
        "ISRC?", "ISRC %d",
        """ Setting and query of measured signal input""",
        validator=strict_discrete_set,
        values={"A": 0,
                "AB": 1,
                "I6": 2,
                "I8": 3},
        map_values=True
    )

    coupling = Instrument.control(
        "ICPL?", "ICPL %d",
        """ Setting and query of measured signal input coupling""",
        validator=strict_discrete_set,
        values={"AC": 0,
                "DC": 1},
        map_values=True
    )

    ground = Instrument.control(
        "IGND?", "IGND %d",
        """ Setting and query of measured signal ground""",
        validator=strict_discrete_set,
        values={"Float": 0,
                "Ground": 1},
        map_values=True
    )

    ##############################
    # Sensitivity, 09 March 2021 #
    ##############################
    voltage_sensitivity = Instrument.control(
        "VSEN?", "VSEN %d",
        """ Setting and query of voltage sensitivity""",
        validator=strict_discrete_set,
        values={2e-9: 0, 5e-9: 1, 10e-9: 2, 20e-9: 3, 50e-9: 4, 100e-9: 5, 200e-9: 6, 500e-9: 7,
                1e-6: 8, 2e-6: 9, 5e-6: 10, 10e-6: 11, 20e-6: 12, 50e-6: 13, 100e-6: 14, 200e-6: 15, 500e-6: 16,
                1e-3: 17, 2e-3: 18, 5e-3: 19, 10e-3: 20, 20e-3: 21, 50e-3: 22, 100e-3: 23, 200e-3: 24, 500e-3: 25,
                1: 26},
        map_values=True
    )

    ################################
    # Time Constant, 09 March 2021 #
    ################################
    time_constant = Instrument.control(
        "TCON?", "TCON %d",
        """ Setting and query of time constant.""",
        validator=strict_discrete_set,
        values={10e-6: 0, 30e-6: 1, 100e-6: 2, 300e-6: 3, 
                1e-3: 4, 3e-3: 5, 10e-3: 6, 30e-3: 7, 100e-3: 8, 300e-3: 9,
                1: 10, 3: 11, 10: 12, 30: 13, 100: 14, 300: 15, 
                1e3: 16, 3e3: 17, 10e3: 18, 30e3: 19},
        map_values=True
    )

    synchronous = Instrument.control(
        "SYNC?", "SYNC %d",
        """ Setting and query of synchronous filter.
            On: Synchronous filter,
            Off: Conventional filter.""",
        validator=strict_discrete_set,
        values={"On": 1, "Off": 0},
        map_values=True
    )

    slope = Instrument.control(
        "SLOP?", "SLOP %d",
        """ Setting and query attenuation slope.""",
        validator=strict_discrete_set,
        values={6: 0, 12: 1, 18: 2, 24: 3},
        map_values=True
    )

    data1 = Instrument.control(
        "DDEF? 1", "DDEF 1, %d",
        """ Setting and query of display parameter.""",
        validator=strict_discrete_set,
        values={"X": 0,
                "R": 1,
                "Noise": 2,
                "AUX1": 3},
        map_values=True
    )

    data2 = Instrument.control(
        "DDEF? 2", "DDEF 2, %d",
        """ Setting and query display parameter.""",
        validator=strict_discrete_set,
        values={"Y": 0,
                "Theta": 1,
                "AUX1": 2,
                "AUX2": 3},
        map_values=True
    )

    data_type = Instrument.control(
        "DTYP?", "DTYP %d",
        """ Setting and query of the kind of data to record""",
        validator=strict_discrete_set,
        values={"Data1": 0,
                "Data2": 1,
                "Data1,2": 2},
        map_values=True
    )

    data_size = Instrument.control(
        "DSIZ?", "DSIZ %d",
        """ Setting and query of record length.""",
        validator=strict_discrete_set,
        values={"2K": 0,
                "4K": 1,
                "8K": 2,
                "16K": 3,
                "32K": 4,
                "64K": 5},
        map_values=True
    )

    data_number = Instrument.control(
        "DNUM?", "DNUM %d",
        """ Setting and query of data memory number to record.""",
        validator=truncated_range,
        values=[0, 31]
    )

    data_sampling_period = Instrument.control(
        "DSMP?", "DSMP %d",
        """ Setting and query of record sampling period.""",
        validator=strict_discrete_set,
        values={62.5e-6: 1, 125e-6: 2, 250e-6: 3, 500e-6: 4, 
                1e-3: 5, 2e-3: 6, 5e-3: 7, 10e-3: 8, 20e-3: 9, 50e-3: 10, 100e-3: 11, 200e-3: 12, 500e-3: 13, 
                1: 14, 2: 15, 5: 16, 10: 17, 20: 18},
        map_values=True
    )

    read = Instrument.measurement(
        "DOUT?",
        """Query of the newest measurement data."""
    )

    def data_sampling_by_gpib(self):
        self.write("DSMP 0")

    def trigger(self):
        self.write("*TRG")

    def start(self):
        self.write("STRT")

    def stop(self):
        self.write("STOP")

    def stored_points(self):
        self.values("SPTS?")