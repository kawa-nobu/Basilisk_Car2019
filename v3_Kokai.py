# coding:utf-8
import RPi.GPIO as GPIO
import time
import struct
import pygame.mixer
import Adafruit_PCA9685

device_path = "/dev/input/js0"
EVENT_FORMAT = "LhBB";
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
#GPIO.setmode( GPIO.BOARD)
#GPIO.setup( 7, GPIO.OUT)

GPIO.setmode(GPIO.BCM)
##############################################
GPIO.setup(12, GPIO.OUT)#Ue_1CH.OUT
GPIO.setup(16, GPIO.OUT)#Ue_1CH.OUT_GY
GPIO.setup(20, GPIO.OUT)#Ue_2CH.OUT
GPIO.setup(21, GPIO.OUT)#Ue_2CH.OUT_GY
##############################################
GPIO.setup(6, GPIO.OUT)#Shita_1CH.OUT
GPIO.setup(13, GPIO.OUT)#Shita_1CH.OUT_GY
GPIO.setup(19, GPIO.OUT)#Shita_2CH.OUT
GPIO.setup(26, GPIO.OUT)#Shita_2CH.OUT_GY
##############################################
#Sarvo
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
##############################################
print('開始')
s = 0
sv_def = 477
try:
  with open(device_path, "rb") as device:
    event = device.read(EVENT_SIZE)
    while event:
      (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(EVENT_FORMAT, event)
      if ds3_type == 1:
        if ds3_num == 13:
          sw = False if ds3_val == 0 else True
          print('LEDオン')
        if ds3_num == 3:
          pygame.mixer.init()
          pygame.mixer.music.load("basilisc.mp3")
          pygame.mixer.music.set_volume(0.1)
          pygame.mixer.music.play(-1)
          print('バジリスクタイム!')
        if ds3_num == 0:
          pygame.mixer.init()
          pygame.mixer.music.stop()
          print('バジリスクタイム終了')
        if ds3_num == 16:
          time.sleep(0.2)
          print('LOGO!')
          GPIO.output(16, True)
          time.sleep(0.50)
          GPIO.output(16, False)
          count = 0
        if ds3_num == 5:
            
          time.sleep(0.4)
          print('on')
          s = s+1
          kakudo = 990
          sv_kakudo =int( 81+ 41 / 90 * kakudo )
          pwm.set_pwm(0, 0, sv_kakudo)
          time.sleep(1)
          pwm.set_pwm(0, 0, sv_def)
      if ds3_type == 2:
        if ds3_num == 19:
          #time.sleep(0.5)
          print('Go')
          sw = False if ds3_val == 0 else True
          GPIO.output(6, sw)
          GPIO.output(19, sw)
          GPIO.output(12, sw)
          GPIO.output(20, sw)
        if ds3_num == 16:
          #time.sleep(0.5)
          print('back')
          sw = False if ds3_val == 0 else True
          GPIO.output(13, sw)
          GPIO.output(26, sw)
          GPIO.output(16, sw)
          GPIO.output(21, sw)
        if ds3_num == 0 and ds3_val > -5000:
            
            print('AAA')
            k = 1100
            sv =int( 81+ 41 / 90 * k )
            pwm.set_pwm(0, 0, sv)
        if ds3_val == 0:
            pwm.set_pwm(0, 0, sv_def)
            
        if ds3_num == 0 and ds3_val < 4000:
            
            print('BBB')
            k = 700
            sv =int( 81+ 41 / 90 * k )
            pwm.set_pwm(0, 0, sv)
        if ds3_val == 0:
            pwm.set_pwm(0, 0, sv_def)
            ##right##
            
        if ds3_num == 3 and ds3_val < -5000:
            
            print('AAA')
            sw = True
            print('go')
            GPIO.output(6, sw)
            GPIO.output(19, sw)
            GPIO.output(12, sw)
            GPIO.output(20, sw)
        if ds3_num == 3 and ds3_val == 0:
            sw2 = False
            print('go-stop')
            GPIO.output(6, sw2)
            GPIO.output(19, sw2)
            GPIO.output(12, sw2)
            GPIO.output(20, sw2)
        if ds3_num == 3 and ds3_val > 4000:
            
            print('BBB')
            sw = True
            print('back')
            
            
            GPIO.output(13, sw)
            GPIO.output(26, sw)
            GPIO.output(16, sw)
            GPIO.output(21, sw)
        if ds3_num == 3 and ds3_val == 0:
            sw2 = False
            print('back')
            GPIO.output(13, sw2)
            GPIO.output(26, sw2)
            GPIO.output(16, sw2)
            GPIO.output(21, sw2)
            

      # print( "{0}, {1}, {2}, {3}".format( ds3_time, ds3_val, ds3_type, ds3_num ) )
      event = device.read(EVENT_SIZE)
finally:
  GPIO.cleanup()
  
