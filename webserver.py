import network
import socket
from machine import Pin
import time

# =====================
# WiFi Config
# =====================
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to WiFi...", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("\nConnected! IP:", ip)

# =====================
# Relay (GP14)
# =====================
relay = Pin(14, Pin.OUT)
relay.value(0)

# =====================
# HTML Page
# =====================
def render_page(state):
    status_text = "ON" if state else "OFF"
    status_color = "#22c55e" if state else "#ef4444"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pico Relay Control</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            background: #0f172a;
            color: white;
            margin-top: 50px;
        }}
        .card {{
            background: #1e293b;
            padding: 30px;
            border-radius: 15px;
            display: inline-block;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        h1 {{
            margin-bottom: 10px;
        }}
        .status {{
            font-size: 24px;
            margin: 20px 0;
            color: {status_color};
        }}
        button {{
            width: 120px;
            height: 50px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            margin: 10px;
            cursor: pointer;
        }}
        .on {{
            background-color: #22c55e;
            color: white;
        }}
        .off {{
            background-color: #ef4444;
            color: white;
        }}
        button:hover {{
            opacity: 0.85;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Relay Control</h1>
        <p>GPIO 14</p>
        <div class="status">Status: {status_text}</div>
        <a href="/on"><button class="on">ON</button></a>
        <a href="/off"><button class="off">OFF</button></a>
    </div>
</body>
</html>
"""
    return html

# =====================
# Socket Server
# =====================
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Web server running on http://{}".format(ip))

# =====================
# Main Loop
# =====================
while True:
    client, addr = s.accept()
    print("Client connected from", addr)

    request = client.recv(1024)
    request = request.decode()
    print("Request:", request)

    # ตรวจ path
    if "GET /on" in request:
        relay.value(1)
        print("Relay ON")
    elif "GET /off" in request:
        relay.value(0)
        print("Relay OFF")

    # ส่งหน้าเว็บกลับ
    response = render_page(relay.value())

    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    client.send(response)
    client.close()
