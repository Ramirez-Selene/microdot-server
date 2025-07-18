import network

ssid = 'Cooperadora Alumnos'
password = ' '

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print('Conectado a WiFi:', wlan.ifconfig())

from microdot import Microdot

app = Microdot()

@app.route('/')
def index(request):
    return '''
        <html>
        <head><title>Servidor</title></head>
        <body style="text-align: center; font-family: Arial;">
            <h1>holap B)!</h1>
            <p>funciona el microcontrolador.</p>
        </body>
        </html>
    ''', 200, {'Content-Type': 'text/html'}

app.run(port=80)