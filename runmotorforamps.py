import RPi.GPIO as GPIO
import time

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in5, GPIO.LOW )
    GPIO.output( in6, GPIO.LOW )
    GPIO.output( in7, GPIO.LOW )
    GPIO.output( in8, GPIO.LOW )
    #GPIO.cleanup()

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


# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
def setup():
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




# the meat

def run(_steps,_sleep,_direction):
    step_sleep = _sleep
    step_count = _steps # 5.625*(1/64) per step, 4096 steps is 360°

    direction = _direction # True for clockwise, False for counter-clockwise
    
    motor_pins_right = [in1,in2,in3,in4]
    motor_pins_left = [in5,in6,in7,in8]
    motor_step_counter_right = 0 ;
    motor_step_counter_left = 0 ;
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins_left)):
            GPIO.output( motor_pins_right[pin], step_sequence[motor_step_counter_right][pin] )
            GPIO.output( motor_pins_left[pin], step_sequence[motor_step_counter_left][pin] )
        if direction=="back":
            motor_step_counter_right = (motor_step_counter_right - 1) % 8
            motor_step_counter_left = (motor_step_counter_left + 1) % 8
        elif direction=="front":
            motor_step_counter_right = (motor_step_counter_right + 1) % 8
            motor_step_counter_left = (motor_step_counter_left - 1) % 8
        elif direction=="right":
            motor_step_counter_right = (motor_step_counter_right - 1) % 8
            motor_step_counter_left = (motor_step_counter_left - 1) % 8
        elif direction=="left":
            motor_step_counter_right = (motor_step_counter_right + 1) % 8
            motor_step_counter_left = (motor_step_counter_left + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )
    cleanup()
#setup()
#degrees = int(4000/90)
#run(90*degrees,0.0018,"right")
#
#exit( 0 )




