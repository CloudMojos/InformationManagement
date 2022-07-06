from crypt import methods
from operator import ne
from types import MethodDescriptorType
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)

app.secret_key = "annabetweentwohs"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Students(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  # College info
  camp = db.Column(db.String(10), nullable = False)
  dept = db.Column(db.String(50), nullable = False)
  course = db.Column(db.String(50), nullable = False)
  # Name
  fname = db.Column(db.String(50), nullable = False)
  mname = db.Column(db.String(50))
  lname = db.Column(db.String(50), nullable = False)
  ename = db.Column(db.String(3))
  # Contact and email
  email = db.Column(db.String(50))
  cpnum = db.Column(db.String(11))
  llnum = db.Column(db.String(8))
  fburl = db.Column(db.String(50))
  lrn = db.Column(db.String(20), nullable = False)
  # Demographics
  bday = db.Column(db.String(10), nullable = False)
  gender = db.Column(db.String(15))
  citizenship = db.Column(db.String(20))
  birthplace = db.Column(db.String(50))
  religion = db.Column(db.String(20))
  cstatus = db.Column(db.String(20))
  fsupport = db.Column(db.String(40))
  height = db.Column(db.String(5))
  weight = db.Column(db.String(5))
  # Location
  unum = db.Column(db.String(10))
  snum = db.Column(db.String(20))
  brgy = db.Column(db.String(30))
  zip = db.Column(db.String(5))
  province = db.Column(db.String(20))

  pfp = db.Column(db.LargeBinary, nullable = False)

  # def __repr__(self):
  #   return self.email


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/register', methods = ["GET", "POST"])
def register():
  if request.method == "POST":

    camp = request.form["camp"]
    dept = request.form["dept"]
    course = request.form["course"]

    fname = request.form["fname"]
    mname = request.form["mname"]
    lname = request.form["lname"]
    ename = request.form["ename"]

    email = request.form["email"]
    cpnum = request.form["cpnum"]
    llnum = request.form["llnum"]
    fburl = request.form["fburl"]
    lrn = request.form["lrn"]

    bday = request.form["bday"]
    gender = request.form["gender"]
    citizenship = request.form["citizenship"]
    birthplace = request.form["birthplace"]
    religion = request.form["religion"]
    cstatus = request.form["cstatus"]
    fsupport = request.form["fsupport"]
    height = request.form["height"]
    weight = request.form["weight"]

    unum = request.form["unum"]
    snum = request.form["snum"]
    brgy = request.form["brgy"]
    zip = request.form["zip"]
    province = request.form["province"]

    pfp = request.files["pfp"]

    # Student Object to be inserted into the Student model (table)
    new_student = Students(
      camp = camp,
      dept = dept,
      course = course,
      fname = fname,
      mname = mname,
      lname = lname,
      ename = ename,
      email = email,
      cpnum = cpnum,
      llnum = llnum,
      fburl = fburl,
      lrn = lrn,
      bday = bday,
      gender = gender,
      citizenship = citizenship,
      birthplace = birthplace,
      religion = religion,
      cstatus = cstatus,
      fsupport = fsupport,
      height = height,
      weight = weight,
      unum = unum,
      snum = snum,
      brgy = brgy,
      zip = zip,
      province = province,
      pfp = pfp.read())

    found_email = Students.query.filter_by(email = new_student.email).first()
    if found_email:
       return redirect('/')
    else:
      db.session.add(new_student)
      db.session.commit()

    return redirect('/')

  else:
    return render_template("register.html")

@app.route('/change_course', methods = ["GET", "POST"])
def change_course():
  student = Students.query.filter_by(email = session["email"]).first()
  if request.method == "POST":
    student.course = request.form["course"]
    student.dept = request.form["dept"]
    db.session.commit()
    return redirect('/')
  else:
    return render_template('change.html', name = student.fname)

@app.route('/login', methods = ["GET", "POST"])
def login():
  if request.method == 'POST':
    email = request.form['email']
    try:
      stdnt_email = Students.query.filter_by(email = email).first().email
      if student:
        session.permanent = True
        session["email"] = stdnt_email
        return redirect(url_for('student'))
    except:
       return render_template("login.html")

  else:
    return render_template("login.html")

@app.route("/student", methods = ["GET", "POST"])
def student():
  if request.method == "POST":
    student = Students.query.filter_by(email = session["email"]).delete()
    db.session.commit()
    return redirect('/')
  else:
    student = Students.query.filter_by(email = session["email"]).first()
    students = Students.query.all()
    return render_template("student.html", s = student, std = students)

@app.route('/logout')
def logout():
  session.pop("email", None)

  return (redirect(url_for("index")))

if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)
