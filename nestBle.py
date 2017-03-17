#!/usr/bin/python
from pcapfile import savefile
import binascii

#Opcodes
WRITE_REQUEST = '12' 
WRITE_RESPONSE = '13'
READ_REQUEST = '0a'
READ_RESPONSE = '0b'

btsnoop = open('/home/anon/nest/btsnoop_hci.pcap', 'rb')
capfile = savefile.load_savefile(btsnoop, verbose=True)

print(capfile)

i = 1
for pkt in capfile.packets:
	raw = binascii.b2a_hex(pkt.raw())
	op = ""
	gattHnd = ""
	payload = ""
	detailStr = ""
	if raw[8:10] == '02' and raw[22:26] == '0400': #HCI Packet Type: ACL Data (0x02) / L2CAP Protocol ATT (0x0004 little endian)
		opcode = raw[26:28]
		if opcode == WRITE_REQUEST:
			op = "Write Request"
			gattHnd = bytearray(raw[28:32])
			payload = raw[32:]
			if i == 476: op += "!" # remove
			detailStr = ": Handle 0x" + str(gattHnd) + " [" + payload + "] " #+ binascii.unhexlify(payload)
			#print "char-write-req 0xfffd " + payload
		elif opcode == WRITE_RESPONSE:
			op = "Write Response"
			detailStr = ": OK"
			#continue
		elif opcode == READ_REQUEST:
			op = "Read Request"
			gattHnd = bytearray(raw[28:32])
			detailStr = ": Handle 0x" + str(gattHnd)
			#continue
		elif opcode == READ_RESPONSE:
			op = "Read Response"
			payload = raw[28:]
			detailStr = ": [" + payload + "] " #+ binascii.unhexlify(payload)
			#if len(payload) < 3:
			#	continue
		else:
			print "Unknown opcode: " + opcode + " Pkt " + str(i) + " [" + raw + "]"
			continue
		print "[Pkt " + str(i) + "] " + op + detailStr
	i += 1