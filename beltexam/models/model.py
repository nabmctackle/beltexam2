import re
from beltexam.config.mysqlconnection import connectToMySQL
from beltexam import app
from flask_bcrypt import Bcrypt
app.secret_key = "theMostSecret"
mysql = connectToMySQL('mydb2')
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Model:
    def register(self, form):
        flasharr = []
        responsearr=[]
        if len(form["f_name"]) < 1:
            flasharr.append["Name can't be blank!"]
        if form['f_name'].isalpha() == False:
            flasharr.append["Name must be alpha!"]
        if len(form["l_name"]) < 1:
            flasharr.append["Last Name can't be blank!"]
        if form['l_name'].isalpha() == False:
            flasharr.append["Last Name can't be alpha!"]
        if len(form['email'])< 1:
            flasharr.append["Email cant be blank"]
        if not EMAIL_REGEX.match(form['email']):
            flasharr.append['Invalid Email Format']
        if len(form["pw"]) < 8:
            flasharr.append["Password must be 8 characters!"]
        if form["pw"] != form['pwc']:
            flasharr.append["Passwords must match!"]
        query = "SELECT * FROM users where email = %(email)s;"
        data = {'email': form['email']}
        all_users = mysql.query_db(query, data)
        if len(all_users) > 0:
            flasharr.append["Email already registered!"]
        if flasharr!=[]:
            responsearr.append(flasharr)
            return responsearr
        elif flasharr==[]:
            username= form['f_name']+" "+form['l_name']
            query = "INSERT INTO users (f_name,l_name,email,password) VALUES (%(f_name)s,%(l_name)s,%(email)s,%(password)s);"
            data = {
                    'f_name': form['f_name'],
                    'l_name': form['l_name'],
                    'email': form['email'],
                    'password': bcrypt.generate_password_hash(form['pw'])
                }
            newuserid = mysql.query_db(query, data)
            responsearr.append(flasharr)
            responsearr.append(username)
            responsearr.append(newuserid)
            return responsearr
    def login(self,form):
        flasharr=[]
        responsearr=[]

        if len(form['liemail'])< 1:
            flasharr.append("email cannot be blank!")
        if not EMAIL_REGEX.match(form['liemail']):
            flasharr.append("email not valid")
        if len(form["lipw"]) < 8:
            flasharr.append("password minimum length is 8 characters")
        if flasharr != []:
            responsearr.append(flasharr)
            return responsearr
        elif flasharr== []:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                    'email': form['liemail']
                }
            usercheck = mysql.query_db(query,data)
            if len(usercheck)>0:
                if bcrypt.check_password_hash(usercheck[0]['password'], form['lipw'])==True:
                    username = usercheck[0]['f_name']+" "+usercheck[0]['l_name']
                    userid= usercheck[0]["id"]
                    responsearr.append(flasharr)
                    responsearr.append(username)
                    responsearr.append(userid)
                    return responsearr
                else:
                    flasharr.append("you could not be logged in")
                    responsearr.append(flasharr)
                    return responsearr
            else:
                flasharr.append("Youre not signed up!")
                responsearr.append(flasharr)
                return responsearr
    def addingtrip(self,form,x):
        flasharr=[]
        responsearr=[]
        planner = x
        if len(form['desc']) < 1:
            flasharr.append("description cannot be blank!")
        if len(form['plan']) < 1:
            flasharr.append("plan cannot be blank")
        if not 0< int(form['ts1']) < 12:
            flasharr.append("invalid start month")
        if not 0< int(form['ts2']) < 32:
            flasharr.append("invalid start day")
        if not 2018<= int(form['ts3']):
            flasharr.append("Must start in future")
        if not 0< int(form['te1']) < 12:
            flasharr.append("invalid end month")
        if not 0< int(form['te2']) < 32:
            flasharr.append("invalid end day")
        if not 2018<= int(form['te3']):
            flasharr.append("Must end in future")
        if int(str(form['ts3'])+str(form['ts1'])+str(form['ts2'])) > int(str(form['te3'])+str(form['te1'])+str(form['te2'])):
            flasharr.append("must end after starting")
        
        if flasharr != []:
            responsearr.append(flasharr)
            return responsearr
        else:
            travelstart = int(str(form['ts3'])+str(form['ts1'])+str(form['ts2']))
            travelend = int(str(form['te3'])+str(form['te1'])+str(form['te2']))
            query = "INSERT INTO trips (description,plan,ts,te,user_id) VALUES (%(1)s,%(2)s,%(3)s,%(4)s,%(5)s);"
            data = {
                    '1': form['desc'],
                    '2': form['plan'],
                    '3': travelstart,
                    '4': travelend,
                    '5': planner
                }
            newtripid = mysql.query_db(query, data)
            query = "INSERT INTO party (trip_id,user_id) VALUES (%(1)s,%(2)s) "
            data = {"1": newtripid, "2":x}
            joinedparty = mysql.query_db(query,data)
            responsearr.append(flasharr)
            return responsearr
    def loggedin(self,x):
        flasharr=[]
        responsearr=[]
        query = "select trips.id, trips.description, trips.ts, trips.te, trips.user_id as tuid, party.user_id as puid from trips join party on trips.id=party.trip_id where party.user_id !=%(id)s and trips.user_id!=%(id)s;"
        data = {"id": x}
        loginfo = mysql.query_db(query,data)
        query="SELECT trips.id as tripid,party.id as pid, trips.plan, trips.ts, trips.te, trips.description, trips.user_id as planner, party.user_id as member  from party join trips on party.trip_id = trips.id where party.user_id=%(x)s;"
        data = {"x": x}
        mytripinfo = mysql.query_db(query,data)
        responsearr.append(flasharr)
        responsearr.append(loginfo)
        responsearr.append(mytripinfo)
        return responsearr
    def joinparty(self,form,x):
        flasharr=[]
        responsearr=[]
        query = "SELECT * FROM TRIPS WHERE id =%(id)s "
        data = {"id": form['tripid']}
        tripinfo = mysql.query_db(query,data)
        if len(tripinfo) < 1:
            flasharr.append("trip does not exist")
            responsearr.append(flasharr)
            return responsearr
        else:
            query= "select * from party where trip_id=%(id)s and user_id=%(2)s;"
            data = {"id": form['tripid'],"2": x}
            nomultiparty=mysql.query_db(query,data)
            if len(nomultiparty) > 0:
                flasharr.append("already joined this party")
                responsearr.append(flasharr)
                return responsearr
            else:
                query = "INSERT INTO party (trip_id,user_id) VALUES (%(1)s,%(2)s) "
                data = {"1": form['tripid'], "2":x}
                joinedparty = mysql.query_db(query,data)
                responsearr.append(flasharr)
                return responsearr
    def leaveparty(self,form,x):
        flasharr=[]
        responsearr=[]
        query="SELECT * FROM party WHERE id =%(id)s"
        data = {'id': form['partyid']}
        validate=mysql.query_db(query,data)
        if validate[0]['user_id'] != x:
            flasharr.append("error in leaving party")
            responsearr.append(flasharr)
            return responsearr
        else:
            query = "DELETE FROM party where id=%(1)s"
            data= {"1":form['partyid']}
            deletedparty=mysql.query_db(query,data)
            flasharr.append("left party successfully")
            responsearr.append(flasharr)
            return responsearr
    def canceltrip(self,form,x):
        flasharr=[]
        responsearr=[]
        query="SELECT * FROM trips WHERE id =%(id)s"
        data = {'id': form['tripid']}
        validate=mysql.query_db(query,data)
        if validate[0]['user_id'] != x:
            flasharr.append("error in cancelling trip")
            responsearr.append(flasharr)
            return responsearr
        else:
            query = "DELETE FROM trips where id=%(1)s"
            data= {"1":form['tripid']}
            deletedtrip=mysql.query_db(query,data)
            flasharr.append("cancelled trip successfully")
            responsearr.append(flasharr)
            return responsearr
    def viewtrip(self,y):
        flasharr=[]
        responsearr=[]
        query = "select * from trips join users on users.id=trips.user_id where trips.id =%(id)s; "
        data = {"id": y}
        tripinfo= mysql.query_db(query,data)
        if len(tripinfo) < 1:
            flasharr.append("trip not found")
            responsearr.append(flasharr)
            return responsearr
        else:
            query = "select * from party join users on users.id=party.user_id where party.trip_id=%(tripid)s and party.user_id != %(id)s;"
            data = {"id": tripinfo[0]['user_id'],"tripid":y}
            partyinfo= mysql.query_db(query,data)
            responsearr.append(flasharr)
            responsearr.append(tripinfo)
            responsearr.append(partyinfo)
            return responsearr


