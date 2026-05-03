import socket

pico_ip = "192.168.1.46"  # เปลี่ยนเป็น IP ที่ Pico แสดง
port = 5000

s = socket.socket()
s.connect((pico_ip, port))

# ลองส่งคำสั่ง
#s.send(b"RL14-ON")
#print(s.recv(1024))

s.send(b"RL14-OFF")
print(s.recv(1024))

s.close()
