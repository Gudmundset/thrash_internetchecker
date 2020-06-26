
from m5stack import *
from m5ui import *
from uiflow import *
import urequests as requests
import wifiCfg
import machine
from easyIO import *
import imu
import random


def main():
    #checks flask webserver for internet speed
    lcd.clear()
    M5Led.on()
    time.sleep(.2)
    M5Led.off()
    setScreenColor(0x437432)
    wifiCfg.autoConnect(lcdShow = False)
    #replace 0's with the computer's IP in internetspeed.py
    res = requests.get('http://0.0.0.0:5000/internetspeed/all').json()
    down = res['download']
    up = res['upload']

    if down < 10 or up < 1:
        #sets background to red to indicate terrible speed.
        setScreenColor(0xFF0000)
        title0 = M5Title(title="Speedtest", x=3 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label0 = M5TextBox(0, 50, '{}\ndown\n{}\nup'.format(down, up), lcd.FONT_DejaVu18,0xFFFFFF, rotate=0)
    wait(5)

title0 = M5Title(title="Speedtest", x=3 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)

while True:
    acclimit = .8
    dblimit = 100
    lcd.clear()
    #lcd.polygon(10, 10, 10, 0, 10, color=0xffffff, rotate=10)

    #microphone detection. This is actually super broken for M5stickC
    adc0 = machine.ADC(34)
    adc0.width(machine.ADC.WIDTH_9BIT)
    adc0.atten(machine.ADC.ATTN_11DB)
    testdb = adc0.read()
    
    # gyro / accel / position detection
    imu0 = imu.IMU()
    imudict = {}
    imudict['x'] = imu0.ypr[1]
    imudict['y'] = imu0.ypr[0]
    # imudict['xacc'] = imu0.acceleration[0]
    # imudict['yacc'] = imu0.acceleration[1]
    # imudict['zacc'] = imu0.acceleration[2]
    # imudict['xgyro'] = imu0.gyro[0]
    # imudict['ygyro'] = imu0.gyro[1]
    # imudict['zgyro'] = imu0.gyro[2]
    title0 = M5Title(title="Speedtest", x=3 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label1 = M5TextBox(0, 40, 'detecting\nyelling or\nflailing!'.format(acclimit), lcd.FONT_Default,0xFFFF33, rotate=0)
    label0 = M5TextBox(0, 80, '{}'.format(imudict), lcd.FONT_Default,0xFFFFFF, rotate=0)
    label0 = M5TextBox(0, 120, '{:.2f} db'.format(testdb), lcd.FONT_Default,0xFFFFFF, rotate=0)
    time.sleep(5)
    if imudict['y'] > acclimit or imudict['x'] > acclimit:
        main()
    if testdb > dblimit:
        main()
    if btnB.isPressed():
        main()
