# imports camra
import sys
import digitalio
from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
    OV7670_TEST_PATTERN_COLOR_BAR_FADE,
)


#Imports comunes
import busio
import board
import time

# Imports de la oled
import math
import adafruit_ssd1306

# Función para enviar datos por UART
def send_data_via_uart(data):
    global uart
    
    data_str = f"{data}\n"
    uart.write(data_str.encode('utf-8'))

# Inicializacion OLED
SCL_OLED, SDA_OLED = board.GP22, board.GP21

# Inicializacion OLED con los nuevos pines
i2c_oled = busio.I2C(SCL_OLED, SDA_OLED)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c_oled)
display.fill(0)
display.show()

# Inicializar CAMARA con los nuevos pines


# Inicializar el UART
uart = busio.UART(board.GP4, board.GP5,
                    baudrate=9600,
                    bits=8,
                    parity=None,
                    stop=1)

SCL_CAM, SDA_CAM = board.GP20, board.GP19
        
# Inicializar CAMARA
cam_bus = busio.I2C(SCL_CAM, SDA_CAM)
cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP9,
    shutdown=board.GP15,
    reset=board.GP14,
)
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = True
buf = bytearray(2 * cam.width * cam.height)


chars = b"9876543210"
width = cam.width
row = bytearray(2 * width)

while True:    
    
    # OLED
    if uart.in_waiting > 0:
        data = uart.readline().strip()
        data = int(data) # Num of case
        
        # data = 2 totalmente recogido
        # data = 1 bajando
        # data = -1 subiendo
        # data = -2 totalmente extendido        
        
        if data == 2:
            text = 'IMAN EN REPOSO'
        elif data == 1:
            text = 'BAJANDO IMAN'
        elif data == -1:
            text = 'SUBIENDO IMAN'
        elif data == -2:
            text = 'CARGANDO'
            
        display.fill(0)
        display.show()
        load_words = text.split()
        
        renglon = 0
        for word in load_words:
            display.text(f'{word}', 0, renglon)
            renglon += 10
            
        display.show()
    
    else:
        
        mandar_uart = [0]*cam.width
        cam.capture(buf)
        j = cam.height//2
        for i in range(cam.width):
            mandar_uart[i] = chars[
                buf[2 * (width * j + i)] * (len(chars) - 1) // 255
            ]-48
        
        counter = 0
        if sum([1 for i in mandar_uart if i > 6]) > int(0.7*len(mandar_uart)):
            send_data_via_uart(1)  # Llego al limite
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        