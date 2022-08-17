from bleak import *
import asyncio
import base64
import socket
from tkinter import Y



LIGHTS_MAC_ADDR = "BE:FF:F0:00:45:D0" 
"""
    This is the address for my Bluetooth lights to connect to
"""

colours = dict()
"""
    The dictionary of predefined colours in the bytearray ready to be sent the Bluetooth lights
"""
colours["Blue"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0x00, 0x0, 0xff, 0x10, 0xef])
colours["Cyan"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0x00, 0xff, 0xff, 0x10, 0xef])
colours["Green"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0x00, 0xff, 0x00, 0x10, 0xef])
colours["Yellow"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0xff, 0xff, 0x00, 0x10, 0xef])
colours["Red"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0xff, 0x00, 0x00, 0x10, 0xef])
colours["Pink"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0xff, 0x00, 0xff, 0x10, 0xef])
colours["White"] = bytearray(
    [0x7e, 0x07, 0x05, 0x03, 0xff, 0xff, 0xff, 0x10, 0xef])

OFF = bytearray([0x7e, 0x04, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef])
"""
    Signal turning off the lights with this bytearray
"""
ON = bytearray([0x7e, 0x04, 0x04, 0xf0, 0x00, 0x01, 0xff, 0x00, 0xef])
"""
    Signal turning on the lights with this bytearray
"""

VENDOR_SPEC_C1 = "0000fff3-0000-1000-8000-00805f9b34fb"
"""
    This is the specified vendor characteristic "C1" which has access for READ and WRITE without response
"""

async def main(*args):
    """ Runs argument checking

    args: 
        args: these will check for predefined commands which can be used and will run the 

    """
    async with BleakClient(LIGHTS_MAC_ADDR) as client:
        print(f"Connected: {client.is_connected}")
        while client.is_connected:
            # Command checking goes here
            await client.write_gatt_char(VENDOR_SPEC_C1, OFF)

        await client.disconnect()


async def cycleColours(client, cycletime):
    """Goes through each of the predefined colours in predefined colour dictionary

    Args:
        client: The Bluetooth device to interact with

        cycletime: The amount of time in seconds to keep the lights on
        
    """
    for colourKey in colours:
        print("Attempting to change light to:" + colourKey)
        # vendorReturn = client.read_gatt_char(VENDOR)
        try:
            await client.write_gatt_char(VENDOR_SPEC_C1, colours[colourKey])
            await asyncio.sleep(cycletime)
        except BleakError as error:
            print(f"   error was found: {error}")


async def printServices(client):
    """ Prints the services for the provided client

    This takes a client and will print each of the services for the client

    Args:
        client: This is the client which the current connection to the Bluetooth device. Which the services will be found for.VENDOR_SPEC_C1

    Returns:
        Console output of each service for the client
    
    """
    print(f"Services for {client}:")
    svcs = await client.get_services()
    for service in svcs:
        print(service)


async def findAndPrint():
    """Scans for bluetooth devices and prints to console

    This uses BleakScanner to listen for Bluetooth devices which are available and then prints dech device in the console

    Args:
        None

    Returns:
        Console output of each Bluetooth device
    
    """
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)


def createRGB(Red, Green, Blue) -> bytearray:
    """Converts RGB to Hex Bytearray

    Converts RGB values from the form (RRR,GGG,BBB) to a bytearray that can be sent to the light device.
    255 corresponds to high light. 0 is low

    Args:
        Red: The value less than 255 which represents the colour red
        Green: The value less than 255 which represents the colour green
        Blue: The value less than 255 which represents the colour blue

    Returns:
        A byte array that will be sent to the device. 
        This array is 9 bytes, where the first 4 bits are static for changing colour.VENDOR_SPEC_C1
        The next 3 bits correspond to RGB in Hex
    """
    assert Red < 256
    assert Green < 256
    assert Blue < 256

    redHex = hex(Red)
    greenHex = hex(Green)
    blueHex = hex(Blue)

    return bytearray([0x7e, 0x07, 0x05, 0x03, redHex, greenHex, blueHex, 0x10, 0xef])


asyncio.run(main())
