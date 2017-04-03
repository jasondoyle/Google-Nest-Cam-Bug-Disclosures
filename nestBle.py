#!/usr/bin/python
from pcapfile import savefile
import binascii
import unicodedata

def toAscii(s):
    s = binascii.unhexlify(s)
    asciiStr = ""
    for c in s:
        try:
            ch = unicode(c, "utf-8")
            if unicodedata.category(ch)[0]!="C":
                asciiStr += ch
            else:
                asciiStr += "."
        except:
            asciiStr += "."
    return asciiStr

#Opcodes
WRITE_REQUEST = '12' 
WRITE_RESPONSE = '13'
READ_REQUEST = '0a'
READ_RESPONSE = '0b'

btsnoop = open('btsnoop_hci.pcap', 'rb')
capfile = savefile.load_savefile(btsnoop, verbose=True)
print(capfile)

i = 1
for pkt in capfile.packets:
	raw = binascii.b2a_hex(pkt.raw())
	op = ""
	gattHnd = ""
	payload = ""
	detailStr = ""
	if raw[8:10] == '02' and raw[22:26] == '0400':
		opcode = raw[26:28]
		if opcode == WRITE_REQUEST:
			op = "Write Request"
			gattHnd = bytearray(raw[28:32])
			payload = raw[32:]
                        payloadAscii = toAscii(payload)
			detailStr = ": Handle 0xfffd [" + "{:<40}".format(payload) + "] " + payloadAscii
		elif opcode == WRITE_RESPONSE:
			op = "Write Response"
			detailStr = ": OK"
			continue
		elif opcode == READ_REQUEST:
			op = "Read Request"
			gattHnd = bytearray(raw[28:32])
			detailStr = ": Handle 0x" + str(gattHnd)
			continue
		elif opcode == READ_RESPONSE:
			op = "Read Response"
			payload = raw[28:]
                        payloadAscii = toAscii(payload)
			detailStr = ": Handle 0xffff [" + "{:<40}".format(payload) + "] " + payloadAscii
			if len(payload) < 3:
				continue
		else:
			#print "Unknown opcode: " + opcode + " Pkt " + str(i) + " [" + raw + "] "
			continue

		print "[Pkt " + str(i) + "] " + op + detailStr
	i += 1

