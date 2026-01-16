# pn532_i2c.py
from time import sleep
from pn532 import PN532

PN532_I2C_ADDR = 0x24


class PN532_I2C(PN532):
    def __init__(self, i2c, addr=PN532_I2C_ADDR):
        self.i2c = i2c
        self.addr = addr
        sleep(0.1)

    # ---------------- Core ----------------

    def SAM_configuration(self):
        self._write_command([0x14, 0x01, 0x14])
        self._read_response(8)

    def read_passive_target(self, timeout=1):
        self._write_command([0x4A, 0x01, 0x00])

        for _ in range(int(timeout * 10)):
            try:
                resp = self._read_response(24)
                if resp and resp[7] > 0:
                    uid_len = resp[12]
                    return bytes(resp[13:13 + uid_len])
            except:
                pass
            sleep(0.1)

        return None

    # ---------------- MIFARE Classic ----------------

    def mifare_classic_authenticate_block(self, uid, block, cmd, key):
        data = [cmd, block] + list(key) + list(uid[-4:])
        self._write_command([0x40] + data)
        resp = self._read_response(10)
        return resp is not None

    def mifare_classic_read_block(self, block):
        self._write_command([0x40, 0x30, block])
        resp = self._read_response(26)
        return bytes(resp[8:24])

    def mifare_classic_write_block(self, block, data):
        if len(data) != 16:
            raise ValueError("Data must be exactly 16 bytes")
        self._write_command([0x40, 0xA0, block] + list(data))
        self._read_response(10)

    # ---------------- Low-level ----------------

    def _write_command(self, command):
        length = len(command) + 1
        frame = [
            PN532.PREAMBLE,
            PN532.STARTCODE1,
            PN532.STARTCODE2,
            length,
            (~length + 1) & 0xFF,
            PN532.HOSTTOPN532
        ] + command

        frame.append(PN532.checksum(frame[5:]))
        frame.append(PN532.POSTAMBLE)

        self.i2c.writeto(self.addr, bytes(frame))
        sleep(0.05)

    def _read_response(self, length):
        sleep(0.05)
        data = self.i2c.readfrom(self.addr, length)
        return list(data)
