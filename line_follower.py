import brian.motors as motors
import brian.sensors as sensors
from time import sleep
from math import pi

motor_l = motors.EV3LargeMotor(motors.MotorPort.A)
motor_r = motors.EV3LargeMotor(motors.MotorPort.B)

color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S1)

WHEEL_D = 5.5
WHEEL_R = WHEEL_D/2
WHEEL_CIRCUMFERENCE = 2*pi*WHEEL_R
AXLE_D = 11.5 # Wheel center to wheel center

CALIBRATION_DEGREES = 100
CALIBRATION_SPEED = 300

DRIVE_SPEED = -600
MAIN_RATIO = 1.0
SIDE_RATIO = 0.15

motor_l.wait_until_ready()
motor_r.wait_until_ready()
color.wait_until_ready()

BLACK = color.reflected_value()
motor_r.rotate_by_angle(CALIBRATION_DEGREES, 300)
WHITE = color.reflected_value()
# motor_r.rotate_by_angle(CALIBRATION_DEGREES, -300)

print(f"BLACK: {BLACK}, WHITE: {WHITE}")
def get_color() -> float: # 0.0 = black,  1.0 = white
    return min(max((color.reflected_value()-BLACK)/(WHITE-BLACK), 0.0), 1.0)


# motor_r.run_at_speed(-500)
# while get_color() < 0.9:
#     sleep(0.05)
# motor_r.hold()

# while True:
#     sleep(0.05)
#     print(get_color())

main_motor = motor_r
side_motor = motor_l

n = 1

STRAIGHT_TIME = 0.7

while True:
    main_motor.run_at_speed(DRIVE_SPEED*MAIN_RATIO)
    side_motor.run_at_speed(DRIVE_SPEED*SIDE_RATIO)

    sleep(STRAIGHT_TIME)
    while get_color() > 0.5:
        sleep(0.05)

    print(f"Prepinam smer  {n}")
    sleep(STRAIGHT_TIME)
    n += 1

    main_motor.run_at_speed(DRIVE_SPEED)
    side_motor.run_at_speed(DRIVE_SPEED)
    side_motor, main_motor = main_motor, side_motor
    sleep(STRAIGHT_TIME)