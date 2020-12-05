import sqlite3 as sql
import requests
import pandas as pd
from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)

app.secret_key = "sample secret key"

# login route
@app.route('/')
def hello():
    return render_template('login.html')

# registration route
@app.route('/register', methods=['GET','POST'])
def register():
  if request.method == 'GET':
    return render_template('registration.html')
  else:
    with sql.connect("database.db") as conn:
      form = {
        "name" : request.form['username'],
        "password": request.form['password'],
        "email" : request.form['email']
      }
      c = conn.cursor()
      try:
        c.execute(f"insert into user_info(name,password,email) values('{form['name']}', '{form['password']}', '{form['email']}')")
        flash('acoount created successfuly!', 'success')
        return render_template('login.html')
      except:
        flash('username already exists!', 'danger')
        return redirect(request.url)
  

# login route
@app.route('/login', methods=['POST'])
def login():
  with sql.connect("database.db") as conn:
    form = {
      "name" : request.form['username'],
      "password": request.form['password']
    }
    try:
      c = conn.cursor()
      c.execute(f"select password from user_info where name='{form['name']}'")
      result = c.fetchone()[0]
      
      if result == form['password']:
        return render_template('index.html')
      else:
        flash("password or username is incorrect!", "danger")
        return render_template('login.html')
    
    except:
      flash("user doesn't exists!", "danger")
      return redirect('/')

def find_dist_idx(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

@app.route('/covidbd-data')
def get_covid_data():
  df = pd.read_csv('district/district.csv')
  dist_data = df.to_dict(orient='records')

  res = requests.get("https://corona-bd.herokuapp.com/district")
  res_data = res.json() 
  data = res_data["data"]

  for dist in data:
    try:
      idx = find_dist_idx(dist_data, "Name", dist["name"])
      dist["lat"] = dist_data[idx]["Latitude"]
      dist["lon"] = dist_data[idx]["Longitude"]

    except ValueError as err:
      pass

  return res_data

# bdcorona route
@app.route('/bdcorona')
def bdcorona():
    get_covid_data()
    return render_template('bdcorona.html')

# map route
@app.route('/map')
def map():
  return render_template('map.html')

# contact route
@app.route('/contact', methods=['POST'])
def hadnle_form():
  with sql.connect("database.db") as conn:
    form = {
      "email": request.form['email'],
      "username": request.form['username'],
      "coronasym": request.form.getlist('coronasym'),
      "msg": request.form['msg']
    }
    symptoms = ""
    for i in form['coronasym']:
      symptoms = symptoms + f"{i},"
    c = conn.cursor()
    c.execute(f"INSERT INTO contact(name,email,symptoms,msg) VALUES('{form['username']}', '{form['email']}','{symptoms}','{form['msg']}')")
    
    return "Submitted by " + form.get('username')

if __name__ == '__main__':
    app.run(debug=True)