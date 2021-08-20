from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.before_first_request
def create_all():
    db.create_all()

#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    rollno = db.Column(db.String(100))
    classs = db.Column(db.String(100))
    def __init__(self, name, rollno, classs):
        self.name = name
        self.rollno = rollno
        self.classs = classs

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    rollno = db.Column(db.String(100))
    classs = db.Column(db.String(100))
    Status = db.Column(db.String(100))
    date = db.Column(db.String(100))
    def __init__(self, name, rollno,classs, Status,date):
        self.name = name
        self.rollno = rollno
        self.classs=classs
        self.Status = Status
        self.date = date

@app.route('/')
def Index():
    all_data = Data.query.all()
    attendnce = Attendance.query.order_by(Attendance.date).all()
    return render_template("index.html", students = all_data,attendnce=attendnce)
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        classs = request.form['class']
        my_data = Data(name=name, rollno=roll, classs=classs)
        db.session.add(my_data)
        db.session.commit()
        flash("Student Inserted Successfully")
        return redirect(url_for('Index'))

@app.route('/insertattendance', methods = ['POST'])
def insertattendance():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        classs = request.form['class']
        status = request.form['status']
        date = request.form['date']
        my_data = Attendance(name=name, rollno=roll, classs=classs,Status=status,date=date)
        db.session.add(my_data)
        db.session.commit()
        flash("Attendance Insterd")
        return redirect(url_for('Index'))


@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.rollno = request.form['roll']
        my_data.classs = request.form['class']
        db.session.commit()
        flash("Student Updated Successfully")
        return redirect(url_for('Index'))
@app.route('/updateattendance', methods = ['GET', 'POST'])
def updateattendance():
    if request.method == 'POST':
        my_data = Attendance.query.get(request.form.get('id'))
        print(my_data)
        my_data.name = request.form['name']
        my_data.rollno = request.form['roll']
        my_data.classs = request.form['class']
        my_data.Status = request.form['status']
        my_data.date = request.form['date']
        db.session.commit()
        flash("Attendance Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")
    return redirect(url_for('Index'))

@app.route('/deleteattenance/<id>/', methods = ['GET', 'POST'])
def deleteattenance(id):
    attendance =Attendance.query.get(id)
    db.session.delete(attendance)
    db.session.commit()
    flash("Student Attendance Deleted Successfully")
    return redirect(url_for('Index'))

@app.route("/search",methods=['GET'])
def search():
    key = request.values.get('key')
    refer = request.values.get("refer")
    if refer == 'name':
        data = Attendance.query.filter_by(name = key).all()
        return render_template('searchlist.html',data=data)
    elif refer == 'rollno':
        data = Attendance.query.filter_by(rollno = key).all()
        return render_template('searchlist.html',data=data)
    elif refer == 'classs':
        data = Attendance.query.filter_by(classs = key).all()
        return render_template('searchlist.html',data=data)
    elif refer == 'Status':
        data = Attendance.query.filter_by(Status = key).all()
        return render_template('searchlist.html',data=data)
    elif refer == 'date':
        data = Attendance.query.filter_by(date = key).all()
        return render_template('searchlist.html',data=data)

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)