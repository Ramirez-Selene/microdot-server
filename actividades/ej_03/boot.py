# boot.py - Configuración al iniciar
import network
import time

def conectar_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(ssid, password)
        
        # Esperar conexión
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(1)
    
    if wlan.isconnected():
        print('WiFi conectado!')
        print('Dirección IP:', wlan.ifconfig()[0])
    else:
        print('No se pudo conectar a WiFi')
    
    return wlan
conectar_wifi('TU_SSID', 'TU_PASSWORD')# Configuracion inicial
