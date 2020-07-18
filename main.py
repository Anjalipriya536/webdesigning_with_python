from flask import Flask,render_template,flash,url_for,request,redirect
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from database import Base,Register
from sqlalchemy.orm import sessionmaker
app=Flask(__name__)
app.secret_key='1234'
engine=create_engine('sqlite:///jntua.db',connect_args={'check_same_thread':False},echo=True)
DBsession=sessionmaker(bind=engine)
session=DBsession()
Base.metadata.bind=engine
@app.route('/index')
def index1():
	return render_template('index.html')
@app.route('/signin')
def sign_in():
	return render_template('signin.html')
@app.route('/home')
def home1():
	dbData=session.query(Register).all()
	return render_template('home.html',reg=dbData)
@app.route('/login', methods=['GET','POST'])
def login1():
	if request.method=='POST':
		u_email=request.form['email']
		u_pass=request.form['password']
		user=session.query(Register).filter_by(email=u_email,password=u_pass).one_or_none()
		if user==None:
			flash("Invalid credentials")
			return render_template('login.html')
		flash('Login Success.....!')
		return redirect(url_for('home1'))
	return render_template('login.html')
	
@app.route('/aboutus')
def about_us():
	return render_template('aboutus.html')
@app.route('/success')
def success1():
	return render_template('success.html')
@app.route('/register',methods=['GET','POST'])
def register1():
	if request.method=='POST':
		newData=Register(name=request.form['name'],email=request.form['email'],password=request.form['psw'])
		session.add(newData)
		session.commit()
		session.rollback()
		flash('Registration successfully completed....!')
		return redirect(url_for('index1'))
	return render_template('register.html')




@app.route('/<int:register_id>/edit',methods=['GET','POST'])
def  edit_function(register_id):
	editData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editData.name=request.form['name']
		editData.email=request.form['email']
		editData.password=request.form['psw']
		session.add(editData)
		session.commit()
		flash('Data is Updated')
		return redirect(url_for('home1'))
	return render_template('edit.html',register=editData)



@app.route('/<int:register_id>/delete',methods=['GET','POST'])
def delete_function(register_id):
	deleteData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		deleteData.name=request.form['name']
		deleteData.email=request.form['email']
		deleteData.password=request.form['psw']
		session.delete(deleteData)
		session.commit()
		flash('Data is Deleted')
		return redirect(url_for('home1'))
	return render_template('delete.html',register=deleteData)
	pass
if __name__=='__main__':
	app.run(debug=True)