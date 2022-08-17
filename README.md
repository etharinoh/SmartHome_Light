# Smart Home - Lighting


## Steps
1. Create python script to interact with lights
    * Change colour, predefined
    * Change brightness (0-100)
2. Setup bluetooth communication from Google Home
    * https://developers.google.com/assistant/smarthome/develop/seamless-setup
    * https://wayscript.com/viz/blog/run-python-script-google-assistant-voice-command
3. Connect each together and use voice commands to alter lighting

## NOTES
* BLE is case sensitive 
    * MAC must be upper case
* Lights can only be connected with 1 device at a time
    * AKA if connected on phone THEN PC cannot connect

### Light value comparison
looking like bits 5,6,7 are rgb, rest static
colours["off"] =          bytearray([0x7e, 0x07, 0x05, 0x03, 0x00, 0x00, 0x00 ,0x10, 0xef]) #not off (rgb = 0) light out

off / on
0x7e, 0x04, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef
0x7e, 0x04, 0x04, 0xf0, 0x00, 0x01, 0xff, 0x00, 0xef