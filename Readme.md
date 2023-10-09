# OptogamaMEX

Tango device server to control Optogama's motorized beam expander via serial connection.

## Configuration

Set the `serial_port` device property to the correct address.

## Implemented

* wavelength (r/w): Set current working wavelength in nm. Only certain design wavelengths are available (e.g. 532 nm, 1064 nm).
* magnification (r/w): Set current beam magnification factor.
* magnification adjustment offset (r/w): Zero means lenses are in theoretically optimal position
* divergence (r/w): Set current divergence adjustment coefficient. Zero means lenses are in theoretically optimal positions.
* limit low (r): minimum position limit switch active
* limit high (r): maximum position limit switch active
* Status: ON, MOVING, FAULT

