from machine import Pin, PWM
import dht
import time
import network
import urequests

"""

SSID = ""
PASSWORD = ""

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)

print("Connected:", wlan.ifconfig())

"""

FAN_PIN = 14
TEMP_PIN = 12

A1 = Pin(16, Pin.OUT)
A2 = Pin(17, Pin.OUT)

Forward_button = Pin(3, Pin.IN, Pin.PULL_UP)
Backward_button = Pin(4, Pin.IN, Pin.PULL_UP)

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

def stop():
    A1.value(0)
    A2.value(0)

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

def make_ndef_text(text, lang="en"):
    lang_bytes = lang.encode("ascii")
    text_bytes = text.encode("utf-8")

    status = len(lang_bytes)
    payload = bytes([status]) + lang_bytes + text_bytes

    record = bytearray()
    record.append(0xD1)              # MB, ME, SR, TNF=1
    record.append(0x01)              # Type length
    record.append(len(payload))      # Payload length
    record.append(0x54)              # 'T'
    record.extend(payload)

    return record

def make_ndef_message(record):
    return bytes([0x03, len(record)]) + record + bytes([0xFE])

def write_ndef_text(pn532, uid, text):
    ndef_record = make_ndef_text(text)
    ndef_message = make_ndef_message(ndef_record)

    # pad to 4-byte pages
    while len(ndef_message) % 4 != 0:
        ndef_message += b"\x00"

    page = 4
    for i in range(0, len(ndef_message), 4):
        pn532.ntag2xx_write_block(page, ndef_message[i:i+4])
        page += 1

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

last_response = {}

while True:

    #response = urequests.get("http://localhost:8000/get-data")


#    if last_response != response.text:
 #       last_response = response.text
  #      print(response.status_code)
   #     print(response.text)

#    response.close()

    if Forward_button.value() == 0:
        print("Forward")
        forward()
    elif Backward_button.value() == 0:
        print("Backward")
        backward()
    else:
        stop

    time.sleep(2)
