from microdot import Microdot, Response, send_file
from machine import Pin, ADC
import time
import uasyncio as asyncio

app = Microdot()
Response.default_content_type = 'application/json'

sensor_temp = ADC(Pin(35))
sensor_temp.atten(ADC.ATTN_11DB)
buzzer = Pin(26, Pin.OUT)
setpoint = 25.0
buzzer_status = False
last_temp = 0.0

def leer_temperatura():
    valor_adc = sensor_temp.read()
    voltaje = valor_adc * (3.3 / 4095)
    temperatura = voltaje * 100
    return round(temperatura, 2)

def controlar_buzzer(temp, ref):
    global buzzer_status
    buzzer_status = temp > ref
    buzzer.value(buzzer_status)

@app.route('/')
def index(req):
    return send_file('index.html')

@app.route('/scripts/<path:path>')
def serve_script(req, path):
    return send_file(f'scripts/{path}')

@app.route('/styles/<path:path>')
def serve_style(req, path):
    return send_file(f'styles/{path}')

@app.route('/setpoint', methods=['POST'])
def actualizar_setpoint(req):
    global setpoint
    setpoint = req.json.get('setpoint', setpoint)
    return {'ok': True, 'nuevo_setpoint': setpoint}

@app.route('/estado')
def estado(req):
    global last_temp
    last_temp = leer_temperatura()
    controlar_buzzer(last_temp, setpoint)
    return {'temp': last_temp, 'buzzer': buzzer_status, 'setpoint': setpoint}

async def loop_sensor():
    while True:
        global last_temp
        last_temp = leer_temperatura()
        controlar_buzzer(last_temp, setpoint)
        await asyncio.sleep(2)

async def main():
    asyncio.create_task(loop_sensor())
    app.run(debug=True, port=80)

if __name__ == '__main__':
    asyncio.run(main())
