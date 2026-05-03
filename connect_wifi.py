import network
import time

# ใส่ชื่อ WiFi และรหัสผ่านของคุณ
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# เชื่อมต่อ WiFi
wlan.connect(ssid, password)

print("Connecting to WiFi...", end="")

# รอจนกว่าจะเชื่อมต่อสำเร็จ
timeout = 10
while timeout > 0:
    if wlan.isconnected():
        break
    timeout -= 1
    print(".", end="")
    time.sleep(1)

# ตรวจสอบผลลัพธ์
if wlan.isconnected():
    print("\nConnected!")
    print("IP address:", wlan.ifconfig()[0])
else:
    print("\nFailed to connect")
    
    
# import urequests

# response = urequests.get("http://example.com")
# print(response.text)
# response.close()    

