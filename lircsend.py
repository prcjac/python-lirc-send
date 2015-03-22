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
from threading import Lock

ENCODING = 'utf-8'
STRING_BUFFER_LEN = 256
DEFAULT_UNIX_SOCKET = "/var/run/lirc/lircd"
LOCAL_HOST_IP = "127.0.0.1"
DEFAULT_LIRC_PORT = 8765

class LircSend:
	"""Use the class methods instead"""
	_s = None
	_init = False
	_lock = Lock()
	_debug = False
	
	def __init__(self, location = None, port = None):
		if not port:
			self._s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			self._s.connect(DEFAULT_UNIX_SOCKET)
		else:
			self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._s.connect((location, port))
		self._init = True
	
	def set_debug(self, debug):
		if debug:
			self._debug = True
		else:
			self._debug = False
	
	def destroy(self):
		try:
			self._lock.acquire()
			self._s.close()
			self._s = None
			self._init = False
		finally:
			self._lock.release()
	
	@classmethod
	def create_local(cls, location = None):
		if not location:
			location = DEFAULT_UNIX_SOCKET
		return cls(location)

	@classmethod
	def create_remote(cls, location = None, port = None):
		if not location:
			location = LOCAL_HOST_IP
		if not port:
			port = DEFAULT_LIRC_PORT
		return cls(location, port)

	"""Internal method for communicating with LIRC"""
	def _send_packet(self, command):
		if not self._init:
			raise ValueError("Object has been destroyed")
		try:
			self._lock.acquire()
			self._s.sendall(command)
			buf = ""
			data = ""
			"""The socket caches IR recieve requests, we need to ignore them"""
			while not data.startswith("BEGIN"):
				data = self._s.recv(256)
				if self._debug:
					print data
			buf += data
			
			"""Start reading sensible content"""
			while not buf.endswith("END\n"):
				data = self._s.recv(256)
				buf += data
				if self._debug:
					print data
			return buf
		finally:
			self._lock.release()
	
	def send_once(self, key, remote, repeat = 1):
		command = "SEND_ONCE %s %s %d\n" % (key, remote, repeat)
		self._send_packet(command)
