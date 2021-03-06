"""
    Envelope Subscriber
"""

import sys
sys.path.append('/home/odroid/ecen490/')

import math
import select
import time
import thread
import zmq
from timeit import default_timer

import MotionControl.scripts.kalman_filter.Robot as robot
import MotionControl.scripts.motor_control.velchange as velchange
import MotionControl.scripts.motor_control.roboclaw as roboclaw
import MotionControl.scripts.Point as Point
import MotionControl.scripts.param as param
from MotionControl.scripts.MotionSkills import MotionSkills
from threading import Thread, Lock
from MotionControl.scripts.utilities import kick

ip = "192.168.1.24"
port = "5563"

robot_update_delay = 0.01
goalie_update_delay = 0.004

mutex = Lock()

team1_robot_state = robot.State()
# team2_robot_state = robot.State()
ball = Point.Point()

# Define a function for the thread
def receive(threadName, *args):
    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    while True:
        address, contents = subscriber.recv_multipart()
        contentArray = contents.split()

        home_robot_angle = contentArray[0]
        home_robot_x = contentArray[1]
        home_robot_y = contentArray[2]

        # away_robot_angle = contentArray[3]
        # away_robot_x = contentArray[4]
        # away_robot_y = contentArray[5]

        ball_x = float(contentArray[6])
        ball_y = float(contentArray[7])
        ball.x = param.pixelToMeter(ball_x)
        ball.y = param.pixelToMeter(ball_y)

        team1_robot_state.pos_theta_est = param.degreeToRadian(float(home_robot_angle))
        team1_robot_state.pos_x_est = param.pixelToMeter(float(home_robot_x))
        team1_robot_state.pos_y_est = param.pixelToMeter(float(home_robot_y))

        # team2_robot_state.pos_theta_est = param.degreeToRadian(float(away_robot_angle))
        # team2_robot_state.pos_x_est = param.pixelToMeter(float(away_robot_x))
        # team2_robot_state.pos_y_est = param.pixelToMeter(float(away_robot_y))

        try:
            mutex.release()
        except:
            pass

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

def rush_goal():
    print "rush goal"

    mutex.acquire()

    desiredPoint = param.AWAY_GOAL

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.4)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.3) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.3)):

        if team1_robot_state.pos_x_est < ball.x:
            print "break"
            break

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), desiredPoint)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(5)
        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

        # kick.kick()

    velchange.goXYOmega(0,0,0)

def follow_behind_ball():
    mutex.acquire()

    while True:
        desiredPoint = MotionSkills.getPointBehindBall(ball)

        if (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):
            go_to_point_behind_ball()

def go_to_point_behind_ball():

    desiredPoint = MotionSkills.getPointBehindBall(ball, param.AWAY_GOAL)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.13) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.13)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.13) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.13)):

        robot_point = Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est)
        desiredPoint = MotionSkills.getPointBehindBall(ball, param.AWAY_GOAL)

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), param.AWAY_GOAL)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(5)
        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
    velchange.goXYOmega(0,0,angular_command.omega)
    time.sleep(angular_command.runTime)

    velchange.goXYOmega(0,0,0)

def go_to_center():
    mutex.acquire()

    desiredPoint = param.CENTER

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), desiredPoint)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(7)
        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)

def goal_scored():
    if(ball.x < -param.pixelToMeter(310)):
        return True
    if(ball.x > param.pixelToMeter(335)):
        return True

    return False

def defend_goal():
    desiredPoint = Point.Point(param.HOME_GOAL.x - 0.38 , ball.y)

    # keep robot within the bounds of the goal
    if desiredPoint.y > param.HOME_GOAL.y + 0.25:
        desiredPoint.y = param.HOME_GOAL.y + 0.25
    elif desiredPoint.y < param.HOME_GOAL.y - 0.25:
        desiredPoint.y = param.HOME_GOAL.y - 0.25

    # move to the desiredPoint
    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.13) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.13)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.13) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.13)):

        desiredPoint = Point.Point(param.HOME_GOAL.x - 0.38 , ball.y)

        # keep robot within the bounds of the goal
        if desiredPoint.y > param.HOME_GOAL.y + 0.25:
            desiredPoint.y = param.HOME_GOAL.y + 0.25
        elif desiredPoint.y < param.HOME_GOAL.y - 0.25:
            desiredPoint.y = param.HOME_GOAL.y - 0.25

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), param.AWAY_GOAL)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(7)

        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(goalie_update_delay)

    velchange.goXYOmega(0,0,0)

def go_to_home():
    mutex.acquire()

    desiredPoint = Point.Point(param.HOME_GOAL.x - 0.5, 0)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.1) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.1)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.1) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.1)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)

def score_goal():
    print "score goal"
    mutex.acquire()

    go_to_point_behind_ball()
    rush_goal()
    go_to_center()

def go_prepare_spin():
    mutex.acquire()

    desiredPoint = Point.Point(param.pixelToMeter(90), 0)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.1) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.1)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.1) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.1)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, 2.0, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
    velchange.goXYOmega(0,0,angular_command.omega)
    time.sleep(angular_command.runTime)

    velchange.goXYOmega(0,0,0)

def one_on_one():
    mutex.acquire()

    state = "idle"
    start = default_timer()
    ball_prev_x = ball.x
    ball_prev_y = ball.y

    while True:
        if goal_scored() and state != "idle":
            print "goal scored", param.meterToPixel(ball.x)
            state = "reset"

        # If there's input ready, do something, else do something
        # else. Note timeout is zero so select won't block at all.
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            command = sys.stdin.readline().strip().lower()
            if command == "r":
                state = "reset"
            elif command == "s":
                state = "defend"
            elif command == "k":
                velchange.goXYOmega(0,0,0)
                state = "idle"

        if state == "idle":
            print "state: idle"
            pass

        elif state == "defend":
            print "state: defend"
            if ball.x < 0:
                # transition
                state = "score"
            else:
                # save state
                ball_prev_x = ball.x
                ball_prev_y = ball.y

                # restart timer
                start = default_timer()

                # transition
                state = "defend_goal"

        elif state == "defend_goal":
            print "state: defend_goal"

            if ball.x < 0:
                # transition
                state = "score"
                continue

            if abs(ball.x - ball_prev_x) < 0.02 and abs(ball.y - ball_prev_y) < 0.02:
                if default_timer() - start > 0.5:
                    # transition
                    state = "score"
                else:
                    defend_goal()
            else:
                start = default_timer()
                ball_prev_x = ball.x
                ball_prev_y = ball.y
                defend_goal()

        elif state == "score":
            print "state: score"

            go_to_point_behind_ball()
            rush_goal()

            state = "defend"

        elif state == "reset":
            print "state: reset"

            go_prepare_spin()

            state = "idle"

# face away from goal as robot goes to defend
# if the ball starts moving when the robot goes to attack, will it go back to defend?

def main():
    """ main method """

    print "Calibrating Roboclaws..."
    roboclaw.calibrateRoboclaws()
    print "...Done"

    try:
        thread.start_new_thread(receive, ("ReceiverThread", 1))
    except:
        print "Error: unable to start thread"

    mutex.acquire()

    one_on_one()

if __name__ == "__main__":
    main()
