from machine import Pin, PWM
import dht
import time

FAN_PIN = 14
TEMP_PIN = 12

A1 = Pin(16, Pin.OUT)
A2 = Pin(17, Pin.OUT)

TARGET_TEMP = 25

FAN_RELAY = Pin(FAN_PIN, Pin.OUT)

TEMP_SENSOR = dht.DHT22(Pin(TEMP_PIN))

def forward():
    A1.value(1)
    A2.value(0)
    print("Motor on")

def backward():
    A1.value(0)
    A2.value(1)

def toggle_relay():
    FAN_RELAY.value(1)
    print("ON")
    time.sleep(10)

    FAN_RELAY.value(0)
    print("OFF")
    time.sleep(10)

def fan_on():
    FAN_RELAY.value(1)
    print("FAN ON")

def fan_off():
    FAN_RELAY.value(0)
    print("FAN OFF")

def read_temp()->float:
    
    try:
        TEMP_SENSOR.measure()
        temp = TEMP_SENSOR.temperature()
        humidity = TEMP_SENSOR.humidity()

        print("Temp: ", temp, "°C")
        print("Humi: ", humidity, "%")

        return temp

    except Exception as e:
        print(f"Sensor error: {e}")
        return 0


while True:

    forward()

    #if read_temp() > TARGET_TEMP:
    #    fan_on()
    #else:
    #    fan_off()

    time.sleep(2)
