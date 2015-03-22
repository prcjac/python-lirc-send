"""
lirc-send.py
Provides a Python Send API for the lirc libraries
Copyright (C) 2015 peter.cowan@cantab.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Realistically this code shouldn't be required since lirc 0.9.2 has a
C API to send IR and the very capable python-lirc project should be
extended. Sadly lirc 0.9.2  isn't yet available for Raspian so
falling back to raw socket communication... delicious.
"""
import socket

ENCODING = 'utf-8'
STRING_BUFFER_LEN = 256

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.2.98", 8765))

def send_packet(command):
	message = "SEND_ONCE LED_24_KEY %s\n" % command
	s.sendall(message)
	buf = ""
	while not buf.endswith("END\n"):
		data = s.recv(256)
		buf += data
		print data

print "start"

send_packet("ON")
send_packet("RED")
send_packet("OFF")
s.close()

