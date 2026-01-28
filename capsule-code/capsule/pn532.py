# pn532.py
# Minimal PN532 core for MicroPython (no CircuitPython dependencies)

class PN532:
    # MIFARE commands
    MIFARE_CMD_AUTH_A = 0x60
    MIFARE_CMD_AUTH_B = 0x61

    # PN532 framing constants
    PREAMBLE = 0x00
    STARTCODE1 = 0x00
    STARTCODE2 = 0xFF
    POSTAMBLE = 0x00
    HOSTTOPN532 = 0xD4

    @staticmethod
    def checksum(data):
        return (~sum(data) + 1) & 0xFF
