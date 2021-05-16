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

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set

class TDS380(Instrument):

    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "Tektronix TDS 380",
            **kwargs
        )

    source = Instrument.control(
        "DAT:SOU?", "DAT:SOU %s",
        """Select the waveform source. """,
        validator=strict_discrete_set,
        values={"Channel1": "CH1",
                "Channel2": "CH2",
                "Reference2": "REF2",
                "Math1": "MATH1",
                },
        map_values=True
    )

    data_format = Instrument.control(
        "DAT:ENC?", "DAT:ENC %s",
        """Specify the waveform data format. """,
        validator=strict_discrete_set,
        values={"ASCII": "ASCI",
                "Ribinary": "RIB",
                "Rpbinary": "RPB",
                "Sribinary": "SRI",
                "Srpbinary": "SRP",
                },
        map_values=True    
    )

    data_width = Instrument.control(
        "DAT:WID?", "DAT:WID %d", 
        """Specify the number of bytes per data point.""",
        values=[1, 2],
        map_values=False
    )
    
    data_start = Instrument.control(
        "DAT:STAR?", "DAT:STAR %d",
        """Specify the start portion of waveform.""",
        validator=truncated_range,
        values=[1, 500]
    )

    data_stop = Instrument.control(
        "DAT:STOP?", "DAT:STOP %d",
        """Specify the start portion of waveform.""",
        validator=truncated_range,
        values=[501, 1000]
    )

    waveform_info = Instrument.measurement(
        "WFMPR?",
        """Get the waveform preamble information.""",
    )

    get_curve = Instrument.measurement(
        "CURV?",
        """Get waveform data from oscilloscope.""",
    )