from machine import Pin, PWM, I2C
import dht
import time

from pn532 import PN532
from pn532_i2c import PN532_I2C

# variable init
TEMP_PIN = 12
FAN_1_PIN = 14
FAN_2_PIN = 15

NFC_SDA_PIN = 4
NFC_SCL_PIN = 5

TARGET_TEMP = 0

FULL_FAN_POWER_TEMP_THRESHOLD = 10

# sensor init
temp_sensor = dht.DHT22(Pin(TEMP_PIN))

# fan init
fan1 = PWM(Pin(FAN_1_PIN))
fan1.freq(25000)

fan2 = PWM(Pin(FAN_2_PIN))
fan2.freq(25000)

# nfc init
i2c = I2C(0, sda=Pin(NFC_SDA_PIN), scl=Pin(NFC_SCL_PIN))
pn532 = PN532_I2C(i2c)
pn532.SAM_configuration()

# converts a float value between 0 and 1 to a value between 0 and 65535
def set_fan_speed(speed):
    # set speed between 0 - 1
    duty = int(speed * 65535)
    fan1.duty_u16(duty)
    fan2.duty_u16(duty)

# main loop
while True:

    temp = 0

    try:
        # read sensor data
        temp_sensor.measure()
        temp = temp_sensor.temperature()
        humidity = temp_sensor.humidity()

        # display the values
        print("Tempreture: ", temp, "°C")
        print("Humidity:", humidity, "%")


    except Exception as e:
        print(f"Sensor error: {e}")

    if temp < TARGET_TEMP:
        # turn fan off
        set_fan_speed(0)
    else:
        # caluclate the difference between the target temp and actual current temp
        error = TARGET_TEMP - temp

        # check if the error is greater than the threshold for full fan speed
        if error > FULL_FAN_POWER_TEMP_THRESHOLD:
            set_fan_speed(1)
        else:
            set_fan_speed(error / 10)

        

    time.sleep(2)