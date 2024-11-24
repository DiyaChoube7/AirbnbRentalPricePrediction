from flask import Flask, redirect, render_template, request, session, flash, url_for
import mysql.connector
import numpy as np
import pickle
import math
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

app=Flask(__name__)
app.secret_key="airbnb"

conn=mysql.connector.connect(host="localhost", user="root", password="12345", database="airbnb")
cursor=conn.cursor()

    
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    
    cursor.execute("""SELECT * FROM `loginpage` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    
    cursor.execute("""INSERT INTO `loginpage` (`user_id`, `name`, `password`, `email`) VALUES (NULL, '{}', '{}', '{}')""".
                   format(name, password, email))
    conn.commit()
    cursor.execute("""SELECT * FROM `loginpage` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
     if request.method == "POST":
         session.permanent = True
         vals=[]
         property_type_map = {'Apartment':0,'Bed & Breakfast':1, 'Boat':2, 'Boutique hotel':3, 'Bungalow':4, 'Cabin':5, 
                        'Camper/RV':6, 'Condominium':7, 'Dorm':8, 'Guest suite':9, 'Guesthouse':10 , 'Hostel':11, 
                        'House':12, 'In-law':13,'Loft':14, 'Other':15, 'Timeshare':16,'Townhouse':17,'Villa':18 }
         room_type_map = {'Entire home/apt':0, 'Private room':1,'PrivSharedate room':2}
         bed_type_map = {'Airbed':0, 'Couch':1, 'Futon' :2, 'Pull-out Sofa':3,'Real Bed':4}
         cancellation_policy_map = {'flexible': 0, 'moderate': 1, 'strict':2}
         cleaning_fee_map = {'False':0, 'True':1}
         city_map = {'Boston':0, 'Chicago':1, 'DC':2, 'LA':3, 'NYC':4,'SF':5}
         instant_bookable_map = {'f':0, 't':1}
         
         city=request.form["city"]
         vals.append(city_map[city])
         
         ptype = request.form["ptype"]
         vals.append(property_type_map[ptype])
         
         rtype=request.form["rtype"]
         vals.append(room_type_map[rtype])
         
         accom=request.form["accom"]
         vals.append(accom)
         
         btype = request.form["btype"]
         vals.append(bed_type_map[btype])
         
         beds=request.form["beds"]
         vals.append(beds)
         
         bedrooms=request.form["bedrooms"]
         vals.append(bedrooms)
         
         bath=request.form["bath"]
         vals.append(bath)
         
         cpolicy=request.form["cpolicy"]
         vals.append(cancellation_policy_map[cpolicy])
         
         cfee=request.form["cfee"]
         vals.append(cleaning_fee_map[cfee])
         
         booking=request.form["booking"]
         vals.append(instant_bookable_map[booking])
         
         with open("my_model.pkl","rb") as f:
             model=pickle.load(f)
         with open("my_scalar.pkl","rb") as f:
             scalar=pickle.load(f)
         vals=scalar.transform([vals])
         res=model.predict(vals)
         for val in res:
             price_in_usd = math.exp(val)
             price_in_inr = price_in_usd * 75
             flash(f"The Price of the Airbnb Stay is $ {price_in_usd:.2f} and ₹ {price_in_inr:.2f}", "info")
     return render_template('predict.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
     
     
if __name__=="__main__":
    app.run(debug=True)