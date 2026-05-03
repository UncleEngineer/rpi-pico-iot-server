import network
import socket
import time
from machine import Pin

# =====================
# ตั้งค่า WiFi
# =====================
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to WiFi...", end="")
timeout = 10
while timeout > 0:
    if wlan.isconnected():
        break
    timeout -= 1
    print(".", end="")
    time.sleep(1)

if not wlan.isconnected():
    print("\nFailed to connect")
    raise SystemExit

ip = wlan.ifconfig()[0]
print("\nConnected! IP:", ip)

# =====================
# ตั้งค่า Relay (GP14)
# =====================
relay = Pin(14, Pin.OUT)
relay.value(0)  # เริ่มต้น OFF

# =====================
# ตั้งค่า Socket Server
# =====================
addr = socket.getaddrinfo('0.0.0.0', 5000)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Listening on", addr)

# =====================
# Loop รับคำสั่ง
# =====================
while True:
    print("Waiting for client...")
    client, client_addr = s.accept()
    print("Client connected from", client_addr)

    try:
        while True:
            data = client.recv(1024)
            if not data:
                break

            cmd = data.decode().strip()
            print("Received:", cmd)

            if cmd == "RL14-ON":
                relay.value(1)
                client.send("Relay ON\n")
            elif cmd == "RL14-OFF":
                relay.value(0)
                client.send("Relay OFF\n")
            else:
                client.send("Unknown command\n")

    except Exception as e:
        print("Error:", e)

    finally:
        client.close()
        print("Client disconnected")
