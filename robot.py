import RPi.GPIO as GPIO
import time
import PiMotor
import os

class Motor():
    def __init__(self):
        GPIO.setwarnings(False)
        TRIG = 29
        ECHO = 31
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        #motor1 top-left, motor2 back-left, motor3 top-right, motor4 bottom-right
        self.motor1 = PiMotor.MotorBoard("MOTOR1",1)
        self.motor2 = PiMotor.MotorBoard("MOTOR2",1)
        self.motor3 = PiMotor.MotorBoard("MOTOR3",1)
        self.motor4 = PiMotor.MotorBoard("MOTOR4",1)

        self.backward_led = PiMotor.Arrow(1)
        self.left_led = PiMotor.Arrow(2)
        self.forward_led = PiMotor.Arrow(3)
        self.right_led = PiMotor.Arrow(4)

    def stop(self):
        self.leds_off()
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()

    def forward(self,speed,time_sleep):
        self.leds_off()
        self.forward_led.on()
        self.motor1.forward(speed)
        self.motor2.forward(speed)
        self.motor3.forward(speed)
        self.motor4.forward(speed)
        time.sleep(time_sleep)
        self.stop()

    def backward(self,speed,time_sleep):
        self.leds_off()
        self.backward_led.on()
        self.motor1.reverse(speed)
        self.motor2.reverse(speed)
        self.motor3.reverse(speed)
        self.motor4.reverse(speed)
        time.sleep(time_sleep)
        self.stop()

    def left(self,speed,time_sleep):
        self.leds_off()
        self.left_led.on()
        self.motor1.reverse(speed)
        self.motor2.reverse(speed)
        self.motor3.forward(speed)
        self.motor4.forward(speed)
        time.sleep(time_sleep)
        self.stop()

    def right(self,speed,time_sleep):
        self.leds_off()
        self.right_led.on()
        self.motor1.forward(speed)
        self.motor2.forward(speed)
        self.motor3.reverse(speed)
        self.motor4.reverse(speed)
        time.sleep(time_sleep)
        self.stop()

    def leds_off(self):
        self.forward_led.off()
        self.backward_led.off()
        self.left_led.off()
        self.right_led.off()



class File():
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.move_path = self.dir_path + "/moves/"

    def store_moves(self, file_name, moves):
        file_name = self.move_path + file_name
        with open(file_name, "w") as file:
            file.writelines(moves)

    def read_moves(self, file_name):
        file_name = self.move_path + file_name
        try:
            with open(file_name, "r") as file:
                moves = file.readlines()
            
            for move in range(len(moves)):
                moves[move] = moves[move].replace("\n","").split(",")

            return moves
        
        except FileNotFoundError:
            print(f"file: {file_name} does not exist")
            return ""

    def delete_moves(self, file_name):
        file_name = self.move_path + file_name
        try:
            os.remove(file_name)
        except:
            print(f"file:{file_name} does not exist")

    def stringify(self, moves_array):
        for move in range(len(moves_array)):
            moves_array[move] = f"{moves_array[move][0]},{str(moves_array[move][1])},{str(moves_array[move][2])}\n"
        return moves_array
        


class Robot():
    def __init__(self) -> None:
        self.motor = Motor()
        self.file = File()
        print("Robot Initialised")

    def execute_moves(self,moves):
        for move in moves:
            direction,speed,time = move[0],move[1],move[2]

            match direction:
                case "forward":
                    self.motor.forward(speed,time)
                case "backward":
                    self.motor.backward(speed,time)
                case "left":
                    self.motor.left(speed,time)
                case "right":
                    self.motor.right(speed,time)
            
    def run(self):
        moves = self.file.read_moves("moves.txt")
        self.execute_moves(moves)


if __name__ == "__main__":
    try:
        robot = Robot()
        robot.run()
    except Exception as error:
        print(f"Error:\n{error}")