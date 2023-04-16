from flask import Flask, render_template, request, redirect,url_for,session

import mysql.connector


app = Flask(__name__)

app.secret_key = "lmlekolejkroejrjefji"

#creates instance db of class mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="flask"
)


@app.route('/')
def index():
   return render_template("index.html")

@app.route('/',methods=["POST","GET"])
def connect():
    #you must create a Cursor object
    #it will let you execute the needed query
    cur = db.cursor()

    error = None
    
    if request.method=="POST" :
      
      if "login" in request.form :
        #you must complete the below SQL select query
        sql = "SELECT user_id, role FROM users WHERE email=(%s) AND password=(%s)"
        val = (request.values["email"],request.values["pswd"])
        cur.execute(sql,val)

        res = cur.fetchall()

        if len(res)==0:
          error = 'Invalid username or password. Please try again!'
         
        else:
          
          session[str(res[0][0])] = request.values["email"]
        
          if str(res[0][1]) == "user" :
            return redirect(url_for("dash",flow=res[0][0]))
          
          if str(res[0][1]) == "admin":
            return redirect(url_for("admin",flow=res[0][0]))
        
      if "sign" in request.form :
        sql2 = "INSERT INTO users(email,password) SELECT * FROM (SELECT (%s),(%s)) AS new_user WHERE NOT EXISTS (SELECT email FROM users WHERE email = (%s))"
        val2 = (request.values["email"],request.values["pswd"],request.values["email"])
        cur.execute(sql2,val2)
        
        db.commit()
        
        if cur.rowcount==0:
          error = 'Sure you wanted to sign in ?'

        else:
         
          sql3 = "SELECT user_id FROM users WHERE email = (%s)"
          val3 = (request.values["email"],)
          
          cur.execute(sql3,val3)
          res3 = cur.fetchall()

          session[str(res3[0][0])] = request.values["email"]
        
          return redirect(url_for("dash",flow=res3[0][0]))
                
    
    return render_template('index.html',error=error)

@app.route('/admin')
def admin():
  user = request.args.get('flow')

  if str(user) in session:
    cur = db.cursor()
    cur.execute("SELECT role FROM users WHERE email= %s",(str(session[user]),))

    role = cur.fetchall()[0][0]

    if role=="admin" :
      #you must create a Cursor object
      #it will let you execute the needed query
      cur = db.cursor()
      #you must complete the below SQL select query
      sql = "SELECT * FROM campus;SELECT campus.campusName,StudentMail FROM mobilitywish JOIN campus ON mobilitywish.Campus_idCampus = campus.idCampus"
      
      sql = filter(None,sql.split(";"))

      res = []
      
      for i in sql:
        cur.execute(i.strip()+";")
        res.append(cur.fetchall())

      campusList = res[0]
      mobilityWish = res[1]

      return render_template("admin.html",campus=campusList,wish=mobilityWish)

  else:
    return redirect(url_for("index"))

@app.route('/admin', methods=["POST","GET"])
def adminquery():
  user = request.args.get('flow')

  if  'campus' in request.form:
    #you must create a Cursor object
    #it will let you execute the needed query
    
    cur = db.cursor()

    
    sql = "INSERT INTO campus(campusName) SELECT * FROM (SELECT (%s)) AS new_wish WHERE NOT EXISTS (SELECT campusName FROM campus WHERE campusName = (%s))"
    
    val = (request.values['campus'],request.values['campus'])
    #we execute an insert query
    cur.execute(sql, val)
  
    #commit = save changes in database
    db.commit()
  
    session.modified = True
  return redirect(url_for("admin",flow=user))



@app.route('/dash')
def dash():
  user = request.args.get('flow')

  if str(user) in session:
    cur = db.cursor()
    cur.execute("SELECT role FROM users WHERE email= %s",(str(session[user]),))
    
    role = cur.fetchall()[0][0]

    if role=="user" :
      #you must create a Cursor object
      #it will let you execute the needed query
      cur = db.cursor()
      #you must complete the below SQL select query
      sql = "SELECT * FROM campus;SELECT campus.campusName,Campus_idCampus FROM mobilitywish JOIN campus ON mobilitywish.Campus_idCampus = campus.idCampus WHERE studentMail='"+str(session[user])+"'"
      
      sql = filter(None,sql.split(";"))

      res = []
      
      for i in sql:
        cur.execute(i.strip()+";")
        res.append(cur.fetchall())

      campusList = res[0]
      mobilityWish = res[1]

      return render_template("dash.html",campus=campusList,wish=mobilityWish)
    
    else : 
      return redirect(url_for("index"))

  else:
    return redirect(url_for("index"))


@app.route('/dash', methods=["POST","GET"])
def dashquery():
  user = request.args.get('flow')

  if  'choice' in request.form:
    #you must create a Cursor object
    #it will let you execute the needed query
    
    cur = db.cursor()
    
    #MobilityWish is the table
    #Campus_idCampus and studentMail are the fields in the table
    sql = "INSERT INTO mobilitywish(studentMail, Campus_idCampus) SELECT * FROM (SELECT (%s), (%s)) AS new_wish WHERE NOT EXISTS (SELECT studentMail FROM mobilityWish WHERE studentMail = (%s) AND Campus_idCampus = (%s))"
    #request.values['choice'] and request.values['student'] are input from the form by user
    val = (session[user], request.values['choice'],session[user],request.values['choice'])
    #we execute an insert query
    cur.execute(sql, val)
  
    #commit = save changes in database
    db.commit()
  
    session.modified = True
  
  if 'change_campus' in request.form:
    #you must create a Cursor object
    #it will let you execute the needed query
    
    cur = db.cursor()
    
    #MobilityWish is the table
    #Campus_idCampus and studentMail are the fields in the table
    sql = "SELECT idCampus FROM campus WHERE campusName=(%s)"

    val = (request.values['change_campus'],)
    #we execute an insert query
    cur.execute(sql, val)
    res = cur.fetchall()


    sql2 = "UPDATE mobilitywish SET Campus_idCampus = (%s) WHERE Campus_idCampus=(%s) AND studentMail = (%s)"

    val2 = (res[0][0],request.values['change'],session[user])

    cur.execute(sql2, val2)
    res2 = cur.fetchall()

    #commit = save changes in database
    db.commit()
  
    session.modified = True

  if 'del' in request.form:
    #you must create a Cursor object
    #it will let you execute the needed query
    
    cur = db.cursor()
    
    #MobilityWish is the table
    #Campus_idCampus and studentMail are the fields in the table
    #SQL syntax is INSERT INTO table(field1, field2) VALUES('value1', 'value2')  
    sql = "DELETE FROM mobilitywish WHERE studentMail=(%s) AND Campus_idCampus=(%s)"

    val = (session[user], request.values['del'])
    #we execute an insert query
    cur.execute(sql, val)
  
    #commit = save changes in database
    db.commit()
  
    session.modified = True
  

  return redirect(url_for("dash",flow=user))


@app.route('/logout')
def logout():
  # remove the username from the session if it is there
  session.pop('username', None)

  return redirect(url_for("index"))

if __name__ == '__main__':
   app.run(debug = True)
