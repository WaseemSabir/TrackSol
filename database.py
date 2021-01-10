import sqlite3
import time
from func import *

def add_user(uid,fname,lname,pas,email,address):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT user_id FROM user")
	output=db.fetchall()
	already_exists=False
	if len(uid)<5 or len(pas)<8:
		already_exists = True
	for i in output:
		if uid==output[0]:
			already_exists=True
	if(already_exists):	
		print("user is already there!")
		return False
	else:
		with conn:
			insert_data_user_table(uid,fname,lname,pas,email,address)
			return True
	return False

def print_use():
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM user")
	output = db.fetchall()
	return output

def search_case(tab,search,attr):
	if tab == 'user':
		dic = { 'id' : 'user_id', 'fname' : 'user_fname', 'lname' : 'user_lname' , 'email' : 'user_email' , 'address' : 'user_address'}
		return search_users(dic[attr],search)
	elif tab == 'employee':
		dic = { 'id' : 'emp_id', 'fname' : 'emp_fname', 'lname' : 'emp_lname' , 'email' : 'emp_email' , 'address' : 'emp_address'}
		return search_employee(dic[attr],search)

def login_check(name,pas,role):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	if role=='Admin':
		db.execute("SELECT * FROM admin where add_id='{}' and add_pass='{}'".format(name,pas))
	elif role=='Employee':
		db.execute("SELECT * FROM employee where emp_id='{}' and emp_pass='{}'".format(name,pas))
	else:
		db.execute("SELECT * FROM user where user_id='{}' and user_pass='{}'".format(name,pas))
	output=db.fetchall()
	if(len(output)==0):
		return False
	elif len(output)!=0:
		return True

def get_rev():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""SELECT user.user_id,user.user_fname,user.user_lname,review.rev
					FROM user
					INNER JOIN review
					ON user.user_id = review.uid""")
	output = db.fetchall()
	return output

def view_sch():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""SELECT * FROM station""")
	output = db.fetchall()
	return output