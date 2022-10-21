
from flask import Flask, render_template, request, flash, url_for, redirect, Response, jsonify
import json
import datetime
import time
from collections import OrderedDict



app = Flask(__name__)
app.secret_key = "abc"

#? code for invoking homepage returns while updating the page
def homepage_return():
    try:
        check5 = username #? checks if page was reloaded without username
    except:
        return render_template("login.html")
    flash(username)
    return render_template("home.html")
def homepage_return_two(new_u):
    global username
    username = new_u
    flash(username)
    return render_template("home.html")


#? code for redirecting to a new page

@app.route("/water", methods = ['GET', 'POST'])
def redirect_water():
  if request.method == 'POST':
        if request.form.get('Setreminder') == 'Water Reminder':
            return render_template("waterReminder.html")

@app.route("/weighttracker", methods = ['GET', 'POST'])
def redirect_weight():
  if request.method == 'POST':
        if request.form.get('weightTrack') == 'Weight Tracker':
            return render_template("weightTracker.html")
        
@app.route("/bodyfatredirect", methods = ['GET', 'POST'])
def redirect_bodyfat():
    if request.method == 'POST':
        return render_template("bodyfat.html")
    
    

@app.route("/meditation", methods = ['GET', 'POST'])
def redirect_meditate():
    if request.method == 'POST':
        if request.form.get('Meditate'):
            return render_template("meditate.html")
        
@app.route("/exercise", methods = ['GET', 'POST'])
def redirect_exercise():
    if request.method == 'POST':
        return render_template("exercisetracker.html")
@app.route("/calorietracker", methods = ['GET', 'POST'])
def redirect_cal():
  if request.method == 'POST':
        return render_template("calorie.html")
@app.route("/sleeptracker", methods = ['GET', 'POST'])
def redirect_sleep():
  if request.method == 'POST':
        return render_template("sleepTracker.html")
@app.route("/homepage", methods = ['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        return(homepage_return())
@app.route("/userprofile", methods = ['GET', 'POST'])
def redirect_userprofile():
    if request.method == 'POST':
        return render_template("userProfile.html")
@app.route("/redirect_steps", methods = ['GET', 'POST'])
def redirect_steps():
    if request.method == 'POST':
        return render_template("stepTracker.html")
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    if request.method == 'POST':
        flash("You have successfully logged out.")
        return render_template("login.html")




#? the login page
@app.route("/", methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        if  request.form.get('Login') == 'Login': #?detects when login button is clicked
            global username
            username = request.form.get("username")
            password = request.form.get("pwd")
            if (username == "") or (password == ""): #? checks if any fields are empty
                flash("Invalid Username or Password.")

                return redirect(url_for('login'))
                
            with open("userdata.json", "r") as f:
                userdata = json.load(f)
            check2 = "check"
            try:
                check1 = userdata[username] #?checks if user exists in database
            except:
                check2 = "0"

            if (username in userdata) and (userdata[username] == password):
                print("Credentials match!")
                with open("userinfo.json", "r") as f:
                    info = json.load(f)
                try:
                    info_lib = info[username] #? checks if user's data exists
                except:
                    return render_template("userinfo.html")
                return(homepage_return())
            elif check2 != "0":
                flash("Invalid Password.")
            else:
                flash(f"Created New Account {username}.")
                userdata.__setitem__(username, password)
                with open("userdata.json", "w") as f: #? creates user data
                    json.dump(userdata, f, indent = 4)


        else:
            return render_template("login.html")
 
    return render_template("login.html") 


#? If user's data doesn't exist, this page will get more info on the user.
@app.route("/userinfo", methods = ['GET', 'POST'])
def getinfo():
    if request.method == 'POST':
        if  request.form.get('Finish') == 'Finish':#?checks if button was pressed
            try:
                check5 = username #? checks if page was reloaded without username
            except:
                return render_template("login.html")
            age = request.form.get("age")
            height = request.form.get("height")
            weight = request.form.get("weight")
            gender = request.form.get("gender")
            with open('userinfo.json', "r") as f:
                userinfo = json.load(f)
                userinfo[username] = {"age" : age, "height" : height, "weight": weight, "gender" : gender}

            dt = datetime.datetime.now()
            time = str(dt.strftime("%Y-%m-%d"))

            with open("userweight.json")as f:
                uweight = json.load(f)
            uweight[username] = {time:str(weight)}
            with open("userweight.json", "w") as f:
                json.dump(uweight, f, indent = 4)
            #?created a dictionary inside json dictionary to keep track of user's metrics
            with open('userinfo.json', "w") as f:

                json.dump(userinfo, f, indent = 4)
            return(homepage_return())
    return render_template("userinfo.html")


#? Body fat page calculations
@app.route("/bodyfat", methods = ['GET', 'POST'])
def bodyfat():
    if request.method == 'POST':
        if request.form.get('bodyfat') == 'Calculate':
            try:
                check5 = username #? checks if page was reloaded without username
            except:
                return render_template("login.html")
            with open('userinfo.json', "r") as f: #? loading previous data
                data = json.load(f)
            u = data[username]
            height = int(u["height"])
            weight = int(u["weight"])
            age = int(u["age"])

            req = request.form.get #? getting new data from the form
            if req("age") != "":
                age = request.form.get("age")
            if req("height") != "":
                height = request.form.get("height")
            if req("weight") != "":
                weight = request.form.get("weight")

            age= int(age)
            height = int(height)
            weight = int(weight)

            
            gender = u["gender"]
            data[username] = {"age" : age, "height" : height, "weight": weight, "gender" : gender}
            with open("userinfo.json", "w") as f: #? overwriting current user info 
                json.dump(data, f, indent = 4)
            with open("userweight.json")as f:
                uweight = json.load(f)
            dt = datetime.datetime.now()
            time = str(dt.strftime("%Y-%m-%d"))
            uweight[username].__setitem__(time, weight)
            with open("userweight.json", "w") as f: #? adding new user info while storing the old data on user
                json.dump(uweight, f, indent = 4)
            height = height/100
            BMI = weight/(height*height)
            if (age < 18) and (gender == 'male'):
                BFP = 1.51 * BMI - 0.70 * age - 2.2
            elif (age < 18) and  (gender == 'female'):
                BFP = 1.51 * BMI - 0.70 * age + 1.4
            elif gender == 'male':
                BFP = 1.20 * BMI + 0.23 * age - 16.2
            elif gender == 'female':
                BFP = 1.20 * BMI + 0.23 * age - 5.4

            
            flash(f"Your Current Body Fat: {round(BFP)}%")
            return render_template("bodyfat.html")
        
        
        
#? Weight Tracker code
@app.route("/trackweight", methods = ['POST'])

def weight_graph():
    if request.method == 'POST':
        try:
            check5 = username #? checks if page was reloaded without username
        except:
            return render_template("login.html")
        with open("userweight.json")as f:
            uweight = json.load(f)
        time = str(request.form.get("month"))
        
        weight = str(request.form.get("weight"))
        if (time != "") and (weight != ""):
            uweight[username].__setitem__(time, weight)
            with open("userweight.json", "w") as f: #? adding more info
                json.dump(uweight, f, indent = 4)
            

        data =uweight[username]
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0])) #? sorting the data according to dates
    
        labels = [row[0:10] for row in data]

        values = []
        for i in data:
            values.append(data[i])
        return render_template("weightTracker.html", labels=labels, values=values) #? returning values for the graph


#? Exercise Graph
@app.route("/trackexercise", methods = ['POST'])
def exercise_graph():
    if request.method == 'POST':
        try:
            check5 = username #? checks if page was reloaded without username
        except:
            return render_template("login.html")
        with open("userexercise.json")as f:
            uexercise = json.load(f)
        try:
            check3 = uexercise[username]#? checking if old user exercise data exists
        except:
            uexercise[username] = {}#? creating new dictionart if it doesn't
        time = str(request.form.get("month"))
        
        cal = str(request.form.get("calorie_burnt"))
        if (time != "") and (cal != ""):
            uexercise[username].__setitem__(time, cal)
            with open("userexercise.json", "w") as f:#? adding more info to user exercise
                json.dump(uexercise, f, indent = 4)
        try:
            check3 = uexercise[username]
        except:
            return render_template("exercisetracker.html")
        
        data =uexercise[username]
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0])) #? sorting according to dates
    
        labels = [row[0:10] for row in data]

        values = []
        for i in data:
            values.append(data[i])
        print(labels, values)
        return render_template("exercisetracker.html", labels=labels, values=values)
@app.route("/trackcalories", methods = ['GET', 'POST'])
def trackcalories():
    if request.method == 'POST':
        try:
            check5 = username #? checks if page was reloaded without username
        except:
            return render_template("login.html")
        with open('userinfo.json', "r") as f:
                data = json.load(f)
        u = data[username]
        height = int(u["height"])
        weight = int(u["weight"])
        age = int(u["age"])
        gender = u["gender"]
        if gender == 'male': #? calculating Base Metabolic Rate for the amount of calories that a user needs
            BMR = 66.47+(13.75 * weight) + (5.003 * height)-(6.755 * age)
        else:
            BMR = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
        flash(f"The Amount of Calories You Need To Eat To Maintain Weight Is: {round(BMR)}")
        with open("usercalorie.json")as f:
            ucal = json.load(f)
        try:
            check3 = ucal[username]
        except:
            ucal[username] = {}
        time = str(request.form.get("month"))
        
        cal = str(request.form.get("calorie_burnt"))
        if (time != "") and (cal != ""):
            ucal[username].__setitem__(time, cal)
            with open("usercalorie.json", "w") as f:
                json.dump(ucal, f, indent = 4)
        
        data =ucal[username]
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0])) #? sorting the keys according to dates
    
        labels = [row[0:10] for row in data]

        values = []
        for i in data:
            values.append(data[i])
        return render_template("calorie.html", labels=labels, values=values) #? returning graph values
    return render_template("calorie.html")



#? Sleep Tracker
@app.route("/tracksleep", methods = ['GET', 'POST'])
def sleep_graph():
    if request.method == 'POST':
        try:
            check5 = username #? checks if page was reloaded without username
        except:
            return render_template("login.html")
        with open("usersleep.json")as f: #? loads user sleep values
            usleep = json.load(f)
        try:
            check3 = usleep[username] #? checks if previous data exists
        except:
            usleep[username] = {}#? creates dict if data exists

        time = str(request.form.get("date"))
        wake_up = str(request.form.get("wakeuptime"))
        go_sleep = str(request.form.get("gotosleeptime"))
        wake_up = int(wake_up.replace(":", ""))
        go_sleep = int(go_sleep.replace(":", ""))
        new_time = str(go_sleep-wake_up)
        
        if int(new_time) < 0:
            new_time = str(wake_up-go_sleep)#? calculates hours slept
        elif (wake_up < 1200) and (go_sleep > 1200):
            wake_up += 2400
            new_time = str(wake_up-go_sleep)
        #? rounding off hours slept according to minutes
        print(new_time, go_sleep, wake_up, go_sleep-wake_up, wake_up-go_sleep)
        if int(new_time[:-2]) > 29:
            new_time = int(new_time[:-2]) + 100
        else:
            new_time = int(new_time[:-2])
        
            
        usleep[username].__setitem__(time, str(new_time))
        with open("usersleep.json", "w") as f: #? updating user sleep
            json.dump(usleep, f, indent = 4)
        try:
            check3 = usleep[username]
        except:
            return render_template("sleepTracker.html")
        
        data =usleep[username]
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0])) #?  sorts data according to dates
    
        labels = [row[0:10] for row in data]

        values = []
        for i in data:
            values.append(data[i])
        print(labels, values)
        return render_template("sleepTracker.html", labels=labels, values=values)#? returns graph values to website 


#? Updating user data 
@app.route("/updateuserprofile", methods = ['GET', 'POST'])
def update_user_profile():
    if request.method == 'POST':
        try:
            check5 = username #? checks if page was reloaded without username
        except:
            return render_template("login.html")
        new_username = request.form.get("new_username") #? gets the new username
        with open("userdata.json", "r") as f:
            userdata = json.load(f)
        try:
            check6 = userdata[new_username] #? checks if username is taken
            flash("That Username is Taken.")
            return render_template("userProfile.html")
        except:
            
            new_username_info = userdata[username]#? re assigns username values to new var
            userdata.pop(username, None) #? takes out username from userdata.json
            userdata[new_username] = new_username_info
            with open("userdata.json", "w") as f: #? dumps the values
                json.dump(userdata, f, indent = 4)
            jsons = ["userinfo", "usercalorie", "usersleep" ,"userexercise", "userweight"] #? all the jsons where username has to be replaced
            for i in jsons: #? for loop to replace everything one at a time
                with open(f"{i}.json", "r") as f:
                    lib = json.load(f)
                try:
                    new_username_info = lib[username]
                    lib.pop(username, None)
                    lib[new_username] = new_username_info
                    with open(f"{i}.json", "w") as f:#? dumps new data after popping old username
                        json.dump(lib, f, indent = 4)
                except:
                    pass #? if there is no username value availabe, in the case of usersleep or usersteps etc.
            return(homepage_return_two(new_username))


#? User Metrics Update 
@app.route("/infoupdate", methods = ['GET', 'POST'])
def infoupdate():
    if request.method == 'POST':
        if  request.form.get('Finish') == 'Finish':#?checks if button was pressed
            try:
                check5 = username #? checks if page was reloaded without username
            except:
                return render_template("login.html")
            age = request.form.get("age")
            height = request.form.get("height")
            weight = request.form.get("weight")
            gender = request.form.get("gender")
            with open('userinfo.json', "r") as f: 
                userinfo = json.load(f)
                userinfo[username] = {"age" : age, "height" : height, "weight": weight, "gender" : gender}

            with open("userweight.json")as f:
                uweight = json.load(f)
            dt = datetime.datetime.now()
            time = str(dt.strftime("%Y-%m-%d"))
            uweight[username].__setitem__(time, weight)
            with open("userweight.json", "w") as f: #? adds current info while keeping old data
                json.dump(uweight, f, indent = 4)

            
            with open('userinfo.json', "w") as f:#? overwrites previous info

                json.dump(userinfo, f, indent = 4)
            return(homepage_return())
    return render_template("infoupdate.html")


#? Tracks Steps 
@app.route("/tracksteps", methods = ['POST'])
def steps_graph():
    if request.method == 'POST':
        try:
            check5 = username #? checks if page was reloaded without username
        except:
            return render_template("login.html")
        with open("usersteps.json")as f:
            usteps = json.load(f)
        try:
            check3 = usteps[username] #? checks if previous user data exists 
        except:
            usteps[username] = {}#? makes a new dicionary if there's no previous data
        time = str(request.form.get("date"))
        
        steps = str(request.form.get("steps"))
        
        usteps[username].__setitem__(time, steps)
        with open("usersteps.json", "w") as f: #?adds new user data
            json.dump(usteps, f, indent = 4)
 
        
        data =usteps[username]
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0])) #? sorts data according to dates
    
        labels = [row[0:10] for row in data]

        values = []
        for i in data:
            values.append(data[i])
        return render_template("stepTracker.html", labels=labels, values=values)#? returns the values for graph


#? 404 handler
@app.errorhandler(404)
def page_not_found(e):
    flash("You went to an Invalid Page.")
    return render_template('login.html') #? redirects to login page and displays "invalid page"


if __name__ == '__main__':
    app.run(debug=True)

