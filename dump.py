# This is a sample Python script that will open a telnet connection to openocd
# and dump nrf51822 flash memory content
# Some inspiration was drawn from https://github.com/geeksville/nrf51-extractor/blob/master/readout.py

from telnetlib import Telnet
import re
import struct
import time

tn = Telnet('localhost', 4444)
tn.set_debuglevel(0)

def send_cmd(cmd):
    tn.write(cmd)
    tn.write(b"\n")
    return tn.read_until(b">")

print(tn.read_until(b">"))
send_cmd(b"reset halt")

with open ("firmware_" + str(int(time.time())) + ".bin", "wb") as out_file:
    for addr in range(0, int("0x40000", 16), 4):
        send_cmd(b"step 0x000006da")
        byte_addr = bytes(str(addr), encoding='utf-8')
        send_cmd(b"reg r3 " + byte_addr)
        send_cmd(b"step")
        resp = str(send_cmd(b"reg r3"))
        data = re.findall(r'0x[0-9a-fA-F]+', resp)
        if data:
            out_file.write(struct.pack("I", int(data[0], 16)))
            print(hex(addr), data[0])
