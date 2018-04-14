from flask import Flask,session,request,render_template,flash,redirect,url_for,logging,flash,abort
from flaskext.mysql import MySQL
from wtforms import Form,StringField,TextAreaField, PasswordField,validators
from passlib.hash import sha256_crypt
import csv
import helpers as h

lastOTP =""

app = Flask('__name__')
app.secret_key = "akgfkagkgafafnmbafbv20939827()_(*&*%$"


class RegistrationForm(Form):
	name = StringField('Name',[validators.Length(min = 1,max = 50)])
	username = StringField('username', [validators.Length(min = 4,max = 20)])
	email = StringField('Email', [validators.Length(min = 6,max = 50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords do not match')
		])
	confirm = PasswordField('Confirm Password')

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/register", methods = ['GET','POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		username = form.username.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))
		f = open('userdatabase.csv', 'a')
		writer = csv.writer(f)
		t = (name,username,email,password)
		writer.writerow(t)

		return (f"you are logged in as {form.username.data}")
	else:
		return render_template("register.html",form = form)


@app.route("/login",methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		d = getUsers()
		if request.form["username"] in d:
			name = request.form["username"]
			dic = {
	        	'name': request.form["username"],
		    	'password': request.form["password"],
	        	'otp': d[request.form["username"]][1],
	        }
			f = open("newuser.txt","w")
			f.write(dic['name'])
			f.close()
			return render_template("myPage.html", obj = dic)
	return render_template("login.html")

def getUsers():
    import pandas as pd
    df = pd.read_csv("Users/All_Users.csv")
    d = {}
    for i in range(df.shape[0]):
        l=[]
        for j in range(1, df.shape[1]):
            l.append(df.iloc[i,j])
        d[df.iloc[i,0]]=l
    return d

@app.route("/Otppage")
def otpProcess():
    var = h.genOTP()
    lastOTP = var
    return render_template("submitOTP.html", otp = var)

@app.route("/otpcheck", methods = ["POST"])
def otpcheck():
    var = str(request.form["otp"])
    value,otp = h.getotpvalue(var,lastOTP)
    f = open("newuser.txt","r")
    name = f.readline()
    value2 = h.getAppid(name)
    print(value)
    print(value2)

    if value == value2 :
        return render_template("valid.html")
    else:
        return render_template("invalid.html")

	# 	username = request.form['username']
	# 	cand_pass = request.form['password']
	# 	session['logged_in'] = True
	# 	session['username'] = username


	# return render_template('login.html')

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True)


