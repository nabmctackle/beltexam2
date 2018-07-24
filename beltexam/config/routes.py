from beltexam import app
from beltexam.controllers.controller import Controller
from flask import render_template
controller=Controller()
@app.route("/", methods=["GET"])
def opener(): 
    return render_template("index.html")
@app.route('/register', methods=['POST'])
def register():
    return controller.register()
@app.route('/login', methods=['POST'])
def login():
    return controller.login()
@app.route('/loggedin', methods=['GET','POST'])
def loggedin():
    return controller.loggedin()
@app.route('/logout', methods=['GET','POST'])
def logout():
    return controller.logout()
@app.route("/addtrip",methods=['GET'])
def addtrip():
    return controller.addtrip()
@app.route("/addingtrip", methods=['POST'])
def addingtrip():
    return controller.addingtrip()
@app.route("/joinparty", methods=['POST'])
def joinparty():
    return controller.joinparty()
@app.route("/leaveparty", methods=['POST'])
def leaveparty():
    return controller.leaveparty()
@app.route("/canceltrip", methods=["POST"])
def canceltrip():
    return controller.canceltrip()
@app.route("/viewtrip/<y>", methods=['GET'])
def viewtrip(y):
    trip=y
    return controller.viewtrip(trip)