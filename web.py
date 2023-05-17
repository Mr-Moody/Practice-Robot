from flask import Flask, redirect, url_for, render_template, request, session, Request, jsonify
from robot import Robot

app = Flask(__name__)
app.secret_key = "supersecretkey"
robot = Robot()

@app.route("/")
def home():
    return redirect("/robot/")


@app.route("/robot/")
def main_page():
    return render_template("robot.html")


@app.route("/robot-forward", methods=["POST"])
def robot_forward():
    speed = request.json["speed"]
    time = request.json["time"]

    if speed != "" and time != "":
        print("moving forward",speed,time)
        robot.motor.forward(float(speed),float(time))

    return jsonify({"response":"moving forward"})


@app.route("/robot-backward", methods=["POST"])
def robot_backward():
    speed = request.json["speed"]
    time = request.json["time"]

    if speed != "" and time != "":
        print("moving backward",speed,time)
        robot.motor.backward(float(speed),float(time))

    return jsonify({"response":"moving backward"})


@app.route("/robot-left", methods=["POST"])
def robot_left():
    speed = request.json["speed"]
    time = request.json["time"]

    if speed != "" and time != "":
        print("moving left",speed,time)
        robot.motor.left(float(speed),float(time))

    return jsonify({"response":"moving left"})


@app.route("/robot-right", methods=["POST"])
def robot_right():
    speed = request.json["speed"]
    time = request.json["time"]

    if speed != "" and time != "":
        print("moving right",speed,time)
        robot.motor.right(float(speed),float(time))

    return jsonify({"response":"moving right"})

@app.route("/receive-moves-list", methods=["POST"])
def receive_moves_list():
    moves = request.json["moves"]
    file = request.json["file"]

    robot.file.store_moves(file, moves)

    return jsonify({"response":"storing moves into file {file}"})

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")