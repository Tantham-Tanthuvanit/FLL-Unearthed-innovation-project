from machine import I2C, Pin
from pn532_i2c import PN532_I2C
from pn532 import PN532
import time

# ---------- I2C ----------
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
pn532 = PN532_I2C(i2c)
pn532.SAM_configuration()

print("Tap card to write...")

KEY = b'\xFF\xFF\xFF\xFF\xFF\xFF'
BLOCK = 4
DATA = b'1'.ljust(16, b'\x00')

while True:
    uid = pn532.read_passive_target()
    if not uid:
        continue

    print("UID:", uid)

    # Authenticate
    if not pn532.mifare_classic_authenticate_block(
        uid, BLOCK, PN532.MIFARE_CMD_AUTH_B, KEY
    ):
        print("Auth failed")
        time.sleep(1)
        continue

    print("Auth OK")

    # Write
    pn532.mifare_classic_write_block(BLOCK, DATA)
    print("Write successful!")

    # Read back to confirm
    read_data = pn532.mifare_classic_read_block(BLOCK)
    print("Read back:", read_data)

    print("Remove card...")
    time.sleep(2)
