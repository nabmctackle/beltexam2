from flask import Flask, render_template, request, redirect, flash, session
from beltexam.models.model import Model
model=Model()
class Controller:
    def register(self):
        response=model.register(request.form)
        if response[0] == []:
            session['name']= response[1]
            session['id']=response[2]
            return redirect('/loggedin')
        else:
            for i in response[0]:
                flash(i)
            return redirect("/")
    def login(self):
        response = model.login(request.form)
        if response[0] == []:
            session['name']=response[1]
            session['id']=response[2]
            return redirect("/loggedin")
        else:
            for i in response[0]:
                flash(i)
            return redirect("/")
    def loggedin(self):
        if 'name' not in session:
            flash("You must log in first!")
            return redirect('/')
        else:
            response= model.loggedin(session['id'])

            return render_template("loggedin.html",name=session['name'],loginfo=response[1],mytripinfo=response[2])
    def logout(self):
        session.clear()
        return redirect('/')
    def addtrip(self):
        return render_template("addtrip.html")
    def addingtrip(self):
        response= model.addingtrip(request.form,session['id'])
        if response[0] == []:
            flash("successful trip scheduled")
            return redirect("/loggedin")
        else:
            for i in response[0]:
                flash(i)
            return redirect("/addtrip")
    def joinparty(self):
        response= model.joinparty(request.form,session['id'])
        for i in response[0]:
            flash(i)
        return redirect("/loggedin")
    def leaveparty(self):
        response= model.leaveparty(request.form,session['id'])
        for i in response[0]:
            flash(i)
        return redirect("/loggedin")
    def canceltrip(self):
        response= model.canceltrip(request.form,session['id'])
        for i in response[0]:
            flash(i)
        return redirect("/loggedin")
    def viewtrip(self,trip):
        y=trip
        response= model.viewtrip(y)
        if response[0] != []:
            for i in response[0]:
                flash(i)
            return redirect("/loggedin")
        else:
            return render_template("viewtrip.html", tripinfo=response[1],partyinfo=response[2])

