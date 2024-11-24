from flask import Flask,render_template,redirect,url_for,request,session,flash
import math
import pickle
import numpy as np

app=Flask(__name__)
app.secret_key="airbnb"

@app.route("/")
def home():
        return render_template("home.html")
    
@app.route('/predict',methods=['POST'])
def predict():
     if request.method == "POST":
         session.permanent = True
         vals=[]
         property_type_map = {'Apartment':0,'Bed & Breakfast':1, 'Boat':2, 'Boutique hotel':3, 'Bungalow':4, 'Cabin':5, 
                        'Camper/RV':6, 'Condominium':7, 'Dorm':8, 'Guest suite':9, 'Guesthouse':10 , 'Hostel':11, 
                        'House':12, 'In-law':13,'Loft':14, 'Other':15, 'Timeshare':16,'Townhouse':17,'Villa':18 }
         room_type_map = {'Entire home/apt':0, 'Private room':1,'Shared room':2}
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
         
         bedrooms=request.form["bedrooms"]
         vals.append(bedrooms)
         
         accom=request.form["accom"]
         vals.append(accom)
         
         btype = request.form["btype"]
         vals.append(bed_type_map[btype])
         
         beds=request.form["beds"]
         vals.append(beds)
         
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
             flash(f"The Price of the Airbnb Stay is around $ {math.exp(val):.2f}","info")
         return render_template("index.html");
     
     
if __name__=="__main__":
    app.run(debug=True)