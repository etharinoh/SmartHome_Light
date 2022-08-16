import base64
import socket
from tkinter import Y


PC_MAC_ADDR = "21:49:86:01:A7:71"
LIGHTS_MAC_ADDR = "BE:FF:F0:00:45:D0"

colours = dict()
# S= static                          S    S     S?     S?    R     G     B     S     S
colours["Blue"] =       bytearray([0x7e, 0x07, 0x05, 0x03, 0x00, 0x0, 0xff, 0x10, 0xef])
colours["Cyan"] =       bytearray([0x7e, 0x07, 0x05, 0x03, 0x00, 0xff, 0xff, 0x10, 0xef])
colours["Green"] =      bytearray([0x7e, 0x07, 0x05, 0x03, 0x00, 0xff, 0x00, 0x10, 0xef])
colours["Yellow"] =     bytearray([0x7e, 0x07, 0x05, 0x03, 0xff, 0xff, 0x00, 0x10, 0xef])
colours["Red"] =        bytearray([0x7e, 0x07, 0x05, 0x03, 0xff, 0x00, 0x00, 0x10, 0xef])
colours["Pink"] =       bytearray([0x7e, 0x07, 0x05, 0x03, 0xff, 0x00, 0xff, 0x10, 0xef])
colours["White"] =      bytearray([0x7e, 0x07, 0x05, 0x03, 0xff, 0xff, 0xff ,0x10, 0xef])

OFF =        bytearray([0x7e, 0x04, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef]) 
ON =         bytearray([0x7e, 0x04, 0x04, 0xf0, 0x00, 0x01, 0xff, 0x00, 0xef])

VENDOR_SPEC_C1 = "0000fff3-0000-1000-8000-00805f9b34fb"

import asyncio
from bleak import *

async def main():
    
    async with BleakClient(LIGHTS_MAC_ADDR) as client:
        print(f"Connected: {client.is_connected}")

        await printServices(client)


        for colourKey in colours:
            print("Attempting to change light to:" + colourKey)
            # vendorReturn = client.read_gatt_char(VENDOR)
            try:
                await client.write_gatt_char('0000fff3-0000-1000-8000-00805f9b34fb', colours[colourKey])
                await asyncio.sleep(2.0)
            except BleakError as error:
                print(f"   error was found: {error}")

        await client.disconnect()

def convert_rgb(rgb):
    scale = 0xFF
    adjusted = [max(1, chan) for chan in rgb]
    total = sum(adjusted)
    adjusted = [int(round(chan / total * scale)) for chan in adjusted]

    # Unknown, Red, Blue, Green
    return bytearray([0x1, adjusted[0], adjusted[2], adjusted[1]])

"""

"""
async def printServices(client):
    print(f"Services for {client}:")
    svcs = await client.get_services()
    for service in svcs:
        print(service)
"""
@usage: await findAndPrint()
"""
async def findAndPrint():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

def createRGB(Red, Green, Blue) -> bytearray:
    assert Red < 256
    assert Green < 256
    assert Blue < 256

    redHex = hex(Red)
    greenHex = hex(Green)
    blueHex = hex(Blue)

    return bytearray([0x7e, 0x07, 0x05, 0x03, redHex, greenHex, blueHex, 0x10, 0xef])


asyncio.run(main())