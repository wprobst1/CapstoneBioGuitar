import time
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.scl, board.sca)
pca = PCA9685(i2c)
pca.frequency = 50

def move(servo, pulse):
    pca.channels[servo].duty_cycle = pulse

move(0, 7000)
time.sleep(1)
move(1, 7000)
time.sleep(1)
move(2, 7000)
time.sleep(1)
move(3, 7000)
time.sleep(1)
move(4, 7000)