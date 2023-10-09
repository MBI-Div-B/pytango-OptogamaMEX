# -*- coding: utf-8 -*-
#
# This file is part of the OptogamaMEX project
#
#
#
# Distributed under the terms of the MIT license.
# See LICENSE.txt for more info.

""" Optogama motorized beam expander

Control magnification, wavelength and offset factors on an Optogama motorized
beam expander connected via serial.
"""

# PyTango imports
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState
from tango import AttrWriteType, PipeWriteType

# Additional import
# PROTECTED REGION ID(OptogamaMEX.additionnal_import) ENABLED START #
import serial
import time



# PROTECTED REGION END #    //  OptogamaMEX.additionnal_import

__all__ = ["OptogamaMEX", "main"]


class OptogamaMEX(Device):
    """
    Control magnification, wavelength and offset factors on an Optogama
    motorized beam expander connected via serial.

    **Properties:**

    - Device Property
        serial_port
            - serial port to use for communication
            - Type:'DevString'
    """

    # PROTECTED REGION ID(OptogamaMEX.class_variable) ENABLED START #
    # PROTECTED REGION END #    //  OptogamaMEX.class_variable

    # -----------------
    # Device Properties
    # -----------------

    serial_port = device_property(dtype="DevString", default_value="/dev/ttyMEX")

    # ----------
    # Attributes
    # ----------

    wavelength = attribute(
        dtype="DevDouble",
        access=AttrWriteType.READ_WRITE,
        unit="nm",
    )

    magnification = attribute(
        dtype="DevDouble",
        access=AttrWriteType.READ_WRITE,
    )

    mag_offset = attribute(
        dtype="DevDouble",
        access=AttrWriteType.READ_WRITE,
        label="magnification adjustment",
    )

    divergence = attribute(
        dtype="DevDouble",
        access=AttrWriteType.READ_WRITE,
        label="divergence adjustment",
    )

    limit_low = attribute(
        dtype="DevBoolean",
    )

    limit_high = attribute(
        dtype="DevBoolean",
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initialises the attributes and properties of the OptogamaMEX."""
        Device.init_device(self)
        # PROTECTED REGION ID(OptogamaMEX.init_device) ENABLED START #
        self._limit_low = False
        self._limit_high = False
        self._last_status = 0
        self.serial = serial.Serial(
            self.serial_port,
            baudrate=57600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
        # PROTECTED REGION END #    //  OptogamaMEX.init_device

    def always_executed_hook(self):
        """Method always executed before any TANGO command is executed."""
        # PROTECTED REGION ID(OptogamaMEX.always_executed_hook) ENABLED START #
        now = time.time()
        if (now - self._last_status) > 0.2:
            self.update_device_status()
            self._last_status = now
        # PROTECTED REGION END #    //  OptogamaMEX.always_executed_hook

    def delete_device(self):
        """Hook to delete resources allocated in init_device.

        This method allows for any memory or other resources allocated in the
        init_device method to be released.  This method is called by the device
        destructor and by the device Init command.
        """
        # PROTECTED REGION ID(OptogamaMEX.delete_device) ENABLED START #
        self.serial.close()
        # PROTECTED REGION END #    //  OptogamaMEX.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_wavelength(self):
        # PROTECTED REGION ID(OptogamaMEX.wavelength_read) ENABLED START #
        """Return the wavelength attribute."""
        return self.get_value("CWL")
        # PROTECTED REGION END #    //  OptogamaMEX.wavelength_read

    def write_wavelength(self, value):
        # PROTECTED REGION ID(OptogamaMEX.wavelength_write) ENABLED START #
        """Set the wavelength attribute."""
        self.set_value("CWL", value)
        # PROTECTED REGION END #    //  OptogamaMEX.wavelength_write

    def read_magnification(self):
        # PROTECTED REGION ID(OptogamaMEX.magnification_read) ENABLED START #
        """Return the magnification attribute."""
        return self.get_value("MAG")
        # PROTECTED REGION END #    //  OptogamaMEX.magnification_read

    def write_magnification(self, value):
        # PROTECTED REGION ID(OptogamaMEX.magnification_write) ENABLED START #
        """Set the magnification attribute."""
        self.set_value("MAG", value)
        # PROTECTED REGION END #    //  OptogamaMEX.magnification_write

    def read_mag_offset(self):
        # PROTECTED REGION ID(OptogamaMEX.mag_offset_read) ENABLED START #
        """Return the mag_offset attribute."""
        return self.get_value("MOF")
        # PROTECTED REGION END #    //  OptogamaMEX.mag_offset_read

    def write_mag_offset(self, value):
        # PROTECTED REGION ID(OptogamaMEX.mag_offset_write) ENABLED START #
        """Set the mag_offset attribute."""
        self.set_value("MOF", value)
        # PROTECTED REGION END #    //  OptogamaMEX.mag_offset_write

    def read_divergence(self):
        # PROTECTED REGION ID(OptogamaMEX.divergence_read) ENABLED START #
        """Return the divergence attribute."""
        return self.get_value("DOF")
        # PROTECTED REGION END #    //  OptogamaMEX.divergence_read

    def write_divergence(self, value):
        # PROTECTED REGION ID(OptogamaMEX.divergence_write) ENABLED START #
        """Set the divergence attribute."""
        self.set_value("DOF", value)
        # PROTECTED REGION END #    //  OptogamaMEX.divergence_write

    def read_limit_low(self):
        # PROTECTED REGION ID(OptogamaMEX.limit_low_read) ENABLED START #
        """Return the limit_low attribute."""
        return self._limit_low
        # PROTECTED REGION END #    //  OptogamaMEX.limit_low_read

    def read_limit_high(self):
        # PROTECTED REGION ID(OptogamaMEX.limit_high_read) ENABLED START #
        """Return the limit_high attribute."""
        return self._limit_high
        # PROTECTED REGION END #    //  OptogamaMEX.limit_high_read

    # --------
    # Commands
    # --------

    @command(
        dtype_in="DevString",
        dtype_out="DevString",
    )
    @DebugIt()
    def query(self, argin):
        # PROTECTED REGION ID(OptogamaMEX.query) ENABLED START #
        """
        Send command to device and return reply.

        :param argin: 'DevString'

        :return:'DevString'
        """
        self.serial.write((f"{argin}\n").encode())
        ans = self.serial.readline().decode()
        return ans

    def get_value(self, name):
        """Query device for numerical value with basic error handling."""
        ans = self.query(f"MEX>{name}?")
        cmd, value = ans.split("_")
        if cmd != f"MEX>{name}":
            raise RuntimeError(f"Reply does not match expected format ({name} ->{ans})")
        return float(value)

    def set_value(self, name, value):
        """Set numerical value on device with basic error handling."""
        ans = self.query(f"MEX>{name}!_{value}")
        cmd, value = ans.split("_")
        if cmd != f"MEX>{name}":
            raise RuntimeError(f"Reply does not match expected format ({name} ->{ans})")

    def update_device_status(self):
        ans = self.query("MEX>STATUS?")
        # expected answer: DIS_COF_DIRECT_ERR_<statuscode>
        status_prefix = "DIS_COF_DIRECT_ERR_"
        if not ans.startswith(status_prefix):
            raise RuntimeError(f"Unexpected status reply ({ans})")
        statuscode = int(ans[len(status_prefix):])
        statusbits = [bool((statuscode >> i) & 1) for i in range(8)]
        if any(statusbits[:2]):
            self.set_state(DevState.MOVING)
        else:
            self.set_state(DevState.ON)
        if any(statusbits[3:6]):
            self.set_state(DevState.FAULT)

        self._limit_high = statusbits[7]
        self._limit_low = statusbits[6]
        # PROTECTED REGION END #    //  OptogamaMEX.query


# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    """Main function of the OptogamaMEX module."""
    # PROTECTED REGION ID(OptogamaMEX.main) ENABLED START #
    return run((OptogamaMEX,), args=args, **kwargs)
    # PROTECTED REGION END #    //  OptogamaMEX.main


if __name__ == "__main__":
    main()
