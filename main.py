try:
  import usocket as socket
except:
  import socket
  
import esp
esp.osdebug(None)  

import network

ssid = 'ssid'
password = 'password'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig()[0])

import gc
gc.collect()

import picoweb

app = picoweb.WebApp(__name__)

@app.route("/")
def index(request, response):
    yield from picoweb.start_response(response, content_type="text/html")

    file = open('index.html', 'r')

    for line in file:
        yield from response.awrite(line)

def get_ip():
    wifi = network.WLAN(network.STA_IF)
    if wifi.active():
        address = wifi.ifconfig()[0]
    else:
        wifi = network.WLAN(network.AP_IF)
        if wifi.active():
            address = wifi.ifconfig()[0]
        else:
            print("No active connection")
    return address

host = get_ip()
app.run(debug=True, host=host)

