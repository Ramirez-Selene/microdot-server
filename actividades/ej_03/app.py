# Aplicacion del servidor
from microdot import Microdot, Response, send_file
from machine import Pin, ADC
import time
import uasyncio as asyncio
import json

app = Microdot()
Response.default_content_type = 'application/json'


sensor_temp = ADC(Pin(35))
sensor_temp.atten(ADC.ATTN_11DB)
buzzer = Pin(26, Pin.OUT)


setpoint = 25.0
buzzer_status = False
last_temp = 0.0

def leer_temperatura():
    """Lee la temperatura del sensor"""
    valor_adc = sensor_temp.read()
    voltaje = valor_adc * (3.3 / 4095)
    temperatura = voltaje * 100
    return round(temperatura, 2)

def controlar_buzzer(temp, ref):
    """Controla el buzzer según la temperatura"""
    global buzzer_status
    buzzer_status = temp > ref
    buzzer.value(buzzer_status)

@app.route('/')
def index(request):
    """Sirve la página principal"""
    return send_file('index.html')

@app.route('/styles.css')
def styles(request):
    """Sirve los estilos CSS"""
    return send_file('styles.css', content_type='text/css')

@app.route('/setpoint', methods=['POST'])
def actualizar_setpoint(request):
    """Actualiza el setpoint de temperatura"""
    global setpoint
    data = json.loads(request.body)
    setpoint = float(data.get('setpoint', setpoint))
    return {'ok': True, 'nuevo_setpoint': setpoint}

@app.route('/estado')
def estado(request):
    """Devuelve el estado actual del sistema"""
    global last_temp
    last_temp = leer_temperatura()
    controlar_buzzer(last_temp, setpoint)
    
    return {
        'temp': last_temp,
        'buzzer': buzzer_status,
        'setpoint': setpoint
    }


async def loop_sensor():
    """Loop principal para lectura de sensor"""
    while True:
        global last_temp
        last_temp = leer_temperatura()
        controlar_buzzer(last_temp, setpoint)
        await asyncio.sleep(2)

async def main():
    """Función principal de la aplicación"""
    
    asyncio.create_task(loop_sensor())
    
    print("Servidor iniciado...")
    app.run(debug=True, port=80)

if __name__ == '__main__':
    asyncio.run(main())
