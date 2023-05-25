import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time
import math

from runmotorforamps import *
from cameraControl import *
button = 17



setup()
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#camSetup
#camSetup()
#getPoint()
print("abo")
distance = 0
speed = 0.0017
currentspeed = 0.005
direction = "front"
incontrolloop = True
steps = 0;
while (incontrolloop):
    if (GPIO.input(button) == GPIO.HIGH):
        print("Success!")
        incontrolloop = False
        break
    start_time = time.time()
    point = getPoint()
    #print(point[1])
    currentsize=point[1]
    wantedsize = 500
    buffer = 0.4

    if (point[1]>0):
        here = (math.log(currentsize/125)/0.104)*1000
        goal = (math.log(wantedsize/125)/0.104)*1000
        #turn a bit
        if point[0]>100 or point[0]<-100:
            if point[1]<170:
                degrees = int(4000/90)
                distance=45*degrees
                if point[0]>0:
                    direction ="right"
                    opposite = "left"
                if point[0]<0:
                    direction ="left"
                    opposite = "right"
                run(distance,0.0018,direction)
                run(int(abs(point[0])*4.5),0.0018,"front")
                run(distance,0.0018,opposite)
                distance = 0
            else:
                if point[0]>0:
                    direction ="right"
                if point[0]<0:
                    direction ="left"
                run(10,0.0018,direction)
        elif point[0]>30 or point[0]<-30:
            if point[0]>0:
                direction ="right"
            if point[0]<0:
                direction ="left"
            run(10,0.0018,direction)
        #go the distance
        elif (point[1]<wantedsize):
            distance=(goal-here)*buffer
            #distance=1000
            print(f"calculated: {here},{currentsize}, going {distance}")
            steps = steps+distance
            direction ="front"
        #...or go a bit backwards...
        elif (point[1]>wantedsize):
            distance=abs(goal-here)*(buffer/2)
            print(f"calculated: {here},{currentsize}, going {distance}")
            steps = steps-distance
            direction ="back"
    while (distance>0):
        if (currentspeed>speed):
            currentspeed = currentspeed-0.0001
        run(10,currentspeed,direction)
        distance=distance-10
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{steps},{point[1]}")
    #print(f"Execution time: {execution_time:.6f} seconds")
