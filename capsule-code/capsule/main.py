from machine import Pin, PWM
import dht
import time

FAN_PIN = 14
TEMP_PIN = 12

FAN_RELAY = Pin(FAN_PIN, Pin.OUT)

TEMP_SENSOR = dht.DHT22(Pin(TEMP_PIN))

def toggle_relay():
    FAN_RELAY.value(1)
    print("ON")
    time.sleep(1)

    FAN_RELAY.value(0)
    print("OFF")
    time.sleep(1)

def read_temp():
    
    try:
        TEMP_SENSOR.measure()
        temp = TEMP_SENSOR.temperature()
        humidity = TEMP_SENSOR.humidity()

        print("Temp: ", temp, "°C")
        print("Humi: ", humidity, "%")

    except Exception as e:
        print(f"Sensor error: {e}")


while True:
    toggle_relay()