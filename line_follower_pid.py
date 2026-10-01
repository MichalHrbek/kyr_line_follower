# ROBOT N. 55

import brian.motors as motors
import brian.sensors as sensors
import time

motor_l = motors.EV3LargeMotor(motors.MotorPort.A)
motor_r = motors.EV3LargeMotor(motors.MotorPort.B)

color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S1)

CALIBRATION_DEGREES = 100
CALIBRATION_SPEED = 300

DRIVE_SPEED = -600

TARGET = 0.0
K_P = 1.0
K_D = 1.0
K_I = 1.0
MAX_I = 500

motor_l.wait_until_ready()
motor_r.wait_until_ready()
color.wait_until_ready()

BLACK = color.reflected_value()
motor_r.rotate_by_angle(CALIBRATION_DEGREES, CALIBRATION_SPEED)
WHITE = color.reflected_value()
motor_r.rotate_by_angle(-CALIBRATION_DEGREES*0.95, CALIBRATION_SPEED)

print(f"BLACK: {BLACK}, WHITE: {WHITE}")
def get_color() -> float: # -1.0 = black,  +1.0 = white
    return (min(max((color.reflected_value()-BLACK)/(WHITE-BLACK), 0.0), 1.0)-1.0)*2.0

prev_error = 0.0
prev_us = time.ticks_us()
FREQ: int = 1_000
PERIOD: int = 1_000_000//FREQ

while True:
    current_us = time.ticks_us()
    delta = current_us - prev_us
    if delta < PERIOD:
        continue
    prev_us = current_us

    error = get_color()-TARGET

    p = error*K_P
    d = (error-prev_error)*K_D/delta # negative?
    i = 0.5*(error+prev_error)*K_I*delta
    i = min(max(i, -MAX_I), MAX_I) # Anti windup clamp
    prev_error = error

    motor_l.run_at_speed(DRIVE_SPEED+p+d+i)
    motor_r.run_at_speed(DRIVE_SPEED-p-d-i)

    print(f"Error: {error}")
    