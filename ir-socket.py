import socket
import time

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
time.sleep(10)

send_packet("ON")
send_packet("RED")
send_packet("OFF")
s.close()

