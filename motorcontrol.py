import RPi.GPIO as GPIO
import time

#right motor
in1 = 26
in2 = 19
in3 = 13
in4 = 6
#left motor
in5 = 21
in6 = 20
in7 = 16
in8 = 12

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.0018

step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

direction = True # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

step_sequence_back = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( in5, GPIO.OUT )
GPIO.setup( in6, GPIO.OUT )
GPIO.setup( in7, GPIO.OUT )
GPIO.setup( in8, GPIO.OUT )
# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( in5, GPIO.LOW )
GPIO.output( in6, GPIO.LOW )
GPIO.output( in7, GPIO.LOW )
GPIO.output( in8, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_pins_left = [in5,in6,in7,in8]
motor_step_counter = 0 ;

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in5, GPIO.LOW )
    GPIO.output( in6, GPIO.LOW )
    GPIO.output( in7, GPIO.LOW )
    GPIO.output( in8, GPIO.LOW )
    GPIO.cleanup()

# the meat

try:
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
            GPIO.output( motor_pins_left[pin], step_sequence[motor_step_counter][pin] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

except KeyboardInterrupt:
    cleanup()
    exit( 1 )

cleanup()
exit( 0 )