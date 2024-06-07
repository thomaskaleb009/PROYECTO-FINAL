import utime
import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
import socket
from machine import Pin,PWM, Timer

pwm_pin=Pin(16)
pwm=PWM(pwm_pin)
pwm.freq(50)

pwm_pin2=Pin(17)
pwm2=PWM(pwm_pin2)
pwm2.freq(50)

pwm_pin3=Pin(20)
pwm3=PWM(pwm_pin3)
pwm3.freq(50)

M1 = Pin(15, Pin.OUT)
pwm_pin = machine.Pin(13)
pwm_motoi = machine.PWM(pwm_pin)
pwm_motoi.freq(1000)
M2 = Pin(14, Pin.OUT)



M3 = Pin(12, Pin.OUT)
pwm_pin = machine.Pin(11)
pwm_motod = machine.PWM(pwm_pin)
pwm_motod.freq(1000)
M4 = Pin(9, Pin.OUT)
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))


def send_data_via_uart(data):
    data_str = str(data)
    uart.write(data_str)
    print(f"Data sent: {data_str}")

def mover_moti(p):
    multi = 2
    M1.value(0)
    M2.value(1)
    M3.value(1)
    M4.value(0)
    
    pwm_motod.duty_u16(int(p/multi))
    pwm_motoi.duty_u16(p)
def mover_motd(p):
    multi = 2
    M3.value(1)
    M4.value(0)
    M1.value(0)
    M2.value(1)
    pwm_motod.duty_u16(p)
    pwm_motoi.duty_u16(p//multi)
    
def parar():
    M1.value(0)
    M2.value(0)
    M3.value(0)
    M4.value(0)
    
def avanzar_mot(p):
    M1.value(0)
    M2.value(1)
    pwm_motoi.duty_u16(p)
    M3.value(1)
    M4.value(0)
    pwm_motod.duty_u16(p)
    
def retroceder_mot(p):
    M1.value(1)
    M2.value(0)
    pwm_motoi.duty_u16(p)
    M3.value(0)
    M4.value(1)
    pwm_motod.duty_u16(p)

def convert_angle(angle,max_duty,min_duty):
    m=180/(max_duty-min_duty)
    b=90-m*max_duty
    por=(angle-b)/m
    return int(65535*por/100)
def bailar():
    M1.toggle()
    M3.toggle()
    time.sleep(0.2)
    M1.toggle()
    M3.toggle()
    d=45
    pwm.duty_u16(convert_angle(d,11.5,1.6))
    i=80
    pwm2.duty_u16(convert_angle(i,11,1.5))
    time.sleep(.8)
    M2.toggle()
    M4.toggle()
    time.sleep(0.2)
    M2.toggle()
    M4.toggle()
    d=-45
    pwm.duty_u16(convert_angle(d,11.5,1.6))
    i=-45
    pwm2.duty_u16(convert_angle(i,11,1.5))
    time.sleep(.8)
    d=85
    pwm.duty_u16(convert_angle(d,11.5,1.6))
    i=60
    pwm2.duty_u16(convert_angle(i,11,1.5))
    time.sleep(.8)
    M4.toggle()
    M1.toggle()
    time.sleep(0.2)
    M4.toggle()
    M1.toggle()
    i=-30
    pwm2.duty_u16(convert_angle(i,11,1.5))
    time.sleep(.8)
    M2.toggle()
    M3.toggle()
    time.sleep(0.2)
    M2.toggle()
    M3.toggle()
    i=0
    d=0
    pwm.duty_u16(convert_angle(d,11.5,1.6))
    pwm2.duty_u16(convert_angle(i,11,1.5))
    
# Set country to avoid possible errors
#rp2.country('DE')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = 'Andres B)'
pw = '35478433'

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed ',wlan_status)
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)
def bot_mot(url):
    v=int(65536/3)
    
    if url.find('=arrib')>-1:
        avanzar_mot(v)
        return
    if url.find('=izq')>-1:
        mover_moti(v)
        return
    if url.find('=aba')>-1:
        retroceder_mot(v)
        return
    if url.find('=dere')>-1:
        mover_motd(v)
        return
    
        
def eleccion(url):
    if url.find('=-90')>-1:
        print('-90')
        return -90
    if url.find('=-45')>-1:
        print('-45')
        return -45
    if url.find('=45')>-1:
        print('45')
        return 45
    if url.find('=90')>-1:
        print('90')
        return 90
    if url.find('=0')>-1:
        print('0')
        return 0
    
    
# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)
        shoulder=0
        elbow=0
        baile=0
        r = str(r)
        led_quit=r.find('?QUIT')
        shoulder= r.find('?Shoulder=')
        elbow = r.find('?Elbow=')
        baile=r.find('?Baile')
        moto=r.find('?moto=')
        entre=r.find('?entrenar')
        subir=r.find('?Subir')
        Bajar=r.find('?Bajar')
        print('led_quit = ', led_quit)
        if subir>-1:
            pwm3.duty_u16(convert_angle(90,10.2,1.8))
            send_data_via_uart(int(2))
            time.sleep(2)
            send_data_via_uart(int(1))
            time.sleep(2)
            send_data_via_uart(int(-1))
            time.sleep(2)
            send_data_via_uart(int(-2))
        if Bajar>-1:
            pwm3.duty_u16(convert_angle(-90,10.2,1.8))
            send_data_via_uart(int(-2))
            time.sleep(2)
            send_data_via_uart(int(-1))
            time.sleep(2)
            send_data_via_uart(int(1))
            time.sleep(2)
            send_data_via_uart(int(2))
        if moto>-1:
            bot_mot(r)
        if shoulder> -1:
            pwm.duty_u16(convert_angle(eleccion(r),11.5,1.6))
        if elbow > -1:
            pwm2.duty_u16(convert_angle(eleccion(r),11,1.5))
        if baile>-1:
            bailar()
        if entre>-1:
            parar()
        if led_quit > -1:
            print('QUIT')
            cl.close()
            print('Connection closed')
            s.close()
            wlan.active(False)
            wlan.disconnect()
            print('Bye')
            break
            
        response = get_html('Brazo.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close() 