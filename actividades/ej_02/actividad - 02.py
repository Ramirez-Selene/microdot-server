import network
import machine
import neopixel

ssid = 'Cooperadora Alumnos'
password = ' '

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    pass
ip = wlan.ifconfig()[0]
print('Conectado. IP:', ip)

led1 = machine.Pin(15, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
led3 = machine.Pin(17, machine.Pin.OUT)

np = neopixel.NeoPixel(machine.Pin(18), 8) 

def set_color(r, g, b):
    for i in range(len(np)):
        np[i] = (r, g, b)
    np.write()
app = Microdot()
@app.route('/')
def index(request):
    return f'''
    <html>
    <head>
        <title>Control IoT</title>
    </head>
    <body style="font-family: Arial; text-align: center;">
        <header>
            <h1>Panel de Control - Kit Maker IoT</h1>
            <p>Dispositivo conectado en: {ip}</p>
        </header>
        
        <main>
            <h2>Control de LEDs individuales</h2>
            <form action="/led1" method="post">
                <button name="state" value="on">LED 1 ON</button>
                <button name="state" value="off">LED 1 OFF</button>
            </form>
            <form action="/led2" method="post">
                <button name="state" value="on">LED 2 ON</button>
                <button name="state" value="off">LED 2 OFF</button>
            </form>
            <form action="/led3" method="post">
                <button name="state" value="on">LED 3 ON</button>
                <button name="state" value="off">LED 3 OFF</button>
            </form>

            <h2>Color para la tira WS2812B</h2>
            <form action="/color" method="post">
                <label>Color:</label><br>
                <input type="color" name="color" value="#ff0000"><br><br>
                <button type="submit">Cambiar Color</button>
            </form>
        </main>

        <footer>
            <p>&copy; 2025 Proyecto Maker IoT | IP: {ip}</p>
        </footer>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.post('/led1')
def control_led1(request):
    state = request.form.get('state')
    led1.value(1 if state == 'on' else 0)
    return redirect('/')

@app.post('/led2')
def control_led2(request):
    state = request.form.get('state')
    led2.value(1 if state == 'on' else 0)
    return redirect('/')

@app.post('/led3')
def control_led3(request):
    state = request.form.get('state')
    led3.value(1 if state == 'on' else 0)
    return redirect('/')

@app.post('/color')
def change_color(request):
    hex_color = request.form.get('color')
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    set_color(r, g, b)
    return redirect('/')

app.run(port=80)