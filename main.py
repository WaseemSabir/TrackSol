from flask import Flask,request,Response
import sqlite3
import database
from func import *

app = Flask(__name__)
@app.route('/',methods=['GET'])
def res():
	return read_file('frontend/login.html')

@app.route('/login',methods=['POST'])
def myuser():
	data = request.form.to_dict()
	global idd
	idd = data['User']
	pas = data['Pass']
	role = data['Role']
	log = database.login_check(idd,pas,role)
	page = read_file('frontend/login_fail.html')
	if log:
		print(role)
		if role=='Admin':
			return read_file('frontend/admin.html').format(idd,idd)
		elif role=='Employee':
			return read_file('frontend/employee.html').format(idd,idd,idd,idd)
		else:
			return read_file('frontend/user.html').format(idd,idd,idd,idd,idd,idd,idd,idd)
	else:
		return page

@app.route('/search/<admin_id>',methods=['GET'])
def search_users(admin_id):
	return read_file('frontend/search_user.html').format(admin_id,'')

@app.route('/search/<admin_id>',methods=['POST'])
def search(admin_id):
	data = request.form.to_dict()
	query = data['search']
	typ = data['table']
	atr = data['attr']
	out = database.search_case(typ,query,atr)
	string = ""

	if typ == 'user':
		string = """<tr><th>User ID</th><th>First Name</th><th>Last Name</th><th>Password</th><th>Email</th><th>Address</th></tr>"""
	else:
		string = "<tr><th>Employee ID</th><th>First Name</th><th>Last Name</th><th>Password</th><th>Gender</th><th>Age</th><th>Email</th><th>Address</th><th>Position</th></tr>"

	for i in out:
		string += """<tr>"""
		for j in i:
			string += """<th>{}</th>""".format(j)
		string += """<tr>"""
	return read_file('frontend/search_user.html').format(admin_id,string)

@app.route('/add_emp',defaults={'typ':'none'})
@app.route('/add_emp/<typ>',methods=['GET','POST'])
def add_emp(typ):
	if request.method == 'GET':
		return read_file('frontend/add_emp.html')
	elif request.method == 'POST':
		if typ == 'add':
			data = request.form.to_dict()
			for i in data:
				if len(data[i])==0:
					return read_file('frontend/add_emp.html')+"""<br> <br> <p> values can't be empty</p>"""
			if len(select_employee(data['User']))>0:
				return read_file('frontend/add_emp.html')+"""<br> <br> <p> User already exists</p>"""
			insert_data_emp_table(data['User'],data['fname'],data['lname'],data['Pass'],data['gender'],data['age'],data['email'],data['address'],data['pos'])
			return read_file('frontend/add_emp.html') + """<br><p> Added the user</p>"""
		elif typ == 'del':
			data = request.form.to_dict()
			if len(select_employee(data['User']))==0:
				return read_file('frontend/add_emp.html')+"""<br> <br> <p> No such user exists</p>"""
			delete_employee(data['User'])
			return read_file('frontend/add_emp.html') + """<br> <p> deleted the employee {}</p>""".format(data['User']) 

@app.route('/register',methods=['GET'])
def register():
	return read_file('frontend/register.html')

@app.route('/admin/profile/<admin_id>',methods=['GET','POST'])
def admin_prof(admin_id):
	if request.method == 'GET':
		my = select_admin(admin_id)
		out = my[0]
		return read_file('frontend/admin_profile.html').format(admin_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7])
	elif request.method == 'POST':
		data = request.form.to_dict()
		my = select_admin(admin_id)
		out = my[0]
		for val in data:
			if len(val)==0:
				return read_file('frontend/admin_profile.html').format(emp_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]) + """<br><br><p> Values can't be empty </p>"""
		update_adm(data['fname'],data['lname'],data['Pass'],data['gender'],data['age'],data['email'],data['address'],data['User'])
		my = select_admin(admin_id)
		out = my[0]
		return read_file('frontend/admin_profile.html').format(admin_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]) + """<br><p>Updated!</p>"""

@app.route('/user/profile/<user_id>',methods=['GET','POST'])
def user_prof(user_id):
	if request.method == 'GET':
		my = select_user(user_id)
		out = my[0]
		return read_file('frontend/user_profile.html').format(user_id,out[0],out[1],out[2],out[3],out[4],out[5])
	elif request.method == 'POST':
		data = request.form.to_dict()
		my = select_user(user_id)
		out = my[0]
		for val in data:
			if len(val)==0:
				return read_file('frontend/user_profile.html').format(emp_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]) + """<br><br><p> Values can't be empty </p>"""
		update_user(data['fname'],data['lname'],data['Pass'],data['email'],data['address'],data['User'])
		my = select_user(user_id)
		out = my[0]
		return read_file('frontend/user_profile.html').format(user_id,out[0],out[1],out[2],out[3],out[4],out[5])+"""<br><br><p> Updated the new info!</p>"""

@app.route('/emp/profile/<emp_id>',methods=['GET','POST'])
def emp_prof(emp_id):
	if request.method == 'GET':
		my = select_employee(emp_id)
		out = my[0]
		return read_file('frontend/emp_profile.html').format(emp_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7])
	elif request.method == 'POST':
		data = request.form.to_dict()
		is_empty=False
		my = select_employee(emp_id)
		out = my[0]
		for val in data:
			if len(val)==0:
				return read_file('frontend/emp_profile.html').format(emp_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]) + """<br><br><p> Values can't be empty </p>"""
		update_emp(data['fname'],data['lname'],data['Pass'],data['gender'],data['age'],data['email'],data['address'],data['User'])
		my = select_employee(emp_id)
		out = my[0]
		return read_file('frontend/emp_profile.html').format(emp_id,out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]) + """<br><p> Updated successfully </p> """

@app.route('/allusers',methods=['GET'])
def allusers():
	b = database.print_use()
	string = ''
	for i in b:
		for j in i:
			try:
				string = string + j
			except:
				string = string + str(j)
			string = string + "\t"
		string = string + '\n'
	return string

@app.route('/register',methods=['POST'])
def  regi():
	data = request.form.to_dict()
	idd = data['User']
	fname = data['fname']
	lname = data['lname']
	pas = data['Pass']
	email = data['email']
	address = data['address']

	log = database.add_user(idd,fname,lname,pas,email,address)
	if log:
		return read_file('frontend/regi_succ.html')
	else:
		return read_file('frontend/regi_fail.html')

@app.route('/reviews/<user_id>',methods=['GET','POST'])
def review(user_id):
	if request.method == 'GET':
		output = database.get_rev()
		string = """<!DOCTYPE html>
					<html>
					<body><h1 style="text-align: center;"> Reviews </h1><br><br>"""
		for i in output:
			string += """<fieldset>
			<p> User ID: {} </p>
			<p> Name : {} {} </p>
			<p> Wrote: {} </p></fieldset>""".format(i[0],i[1],i[2],i[3])
		string += """<form action="http://127.0.0.1:5000/reviews/{}" method="post">
				<p> Write a review </p>
				<input type="text" id="tex" name="tex"><br>
				<input type="submit" value="Send"></form></body></html>""".format(user_id)
		return string
	elif request.method == 'POST':
		data = request.form.to_dict()
		t = data['tex']
		insert_rev(user_id,t)
		output = database.get_rev()
		string = """<!DOCTYPE html>
					<html>
					<body><h1 style="text-align: center;"> Reviews </h1><br><br>"""
		for i in output:
			string += """<fieldset>
			<p> User ID: {} </p>
			<p> Name: {} {} </p>
			<p> Wrote: {} </p></fieldset>""".format(user_id,i[1],i[2],i[3])
		string += """<form action="http://127.0.0.1:5000/reviews/{}" method="post">
				<p> Write a review </p>
				<input type="text" id="tex" name="tex"><br>
				<input type="submit" value="Send"></form></body></html>""".format(user_id)
		return string

@app.route('/view_jobs/<emp_id>',methods=['GET'])
def view_jobs(emp_id):
	my = select_employee(emp_id)
	out = my[0]
	jobs = search_jobs(emp_id)
	string = ""
	if len(jobs)==0:
		string = "No jobs assigned to you"
	for i in jobs:
		for j in i:
			string += """<li>{}</li>""".format(j)
	return read_file('frontend/view_jobs.html').format(out[1],out[2],out[8],string)

@app.route('/assign/<typ>',methods=['GET','POST'])
def assign(typ):
	if request.method == 'GET':
		return read_file('frontend/assign_job.html').format("","","")
	elif request.method == 'POST':
		if typ == 'view':
			data = request.form.to_dict()
			eid = data['eid']
			jobs = search_jobs(eid)
			if len(jobs)==0:
				return read_file('frontend/assign_job.html').format("Employee does not exist or no jobs assigned","","")
			string = "Jobs : <br>"
			for i in jobs:
				for j in i:
					string += """<li>{}</li>""".format(j)
			return read_file('frontend/assign_job.html').format(string,"","")
		elif typ == 'asig':
			data = request.form.to_dict()
			eid = data['eid']
			job = data['job']
			inserted = insert_job(eid,job)
			if inserted:
				return read_file('frontend/assign_job.html').format("","New job inserted","")
			else:
				return read_file('frontend/assign_job.html').format("","Employee id is not correct","")
		elif typ == 'del':
			data = request.form.to_dict()
			jid = data['jid']
			deleted = delete_job(jid)
			if deleted:
				return read_file('frontend/assign_job.html').format("","","Jobs deleted")
			else:
				return read_file('frontend/assign_job.html').format("","","Job id is incorrect")
		else:
			return "error 404"

@app.route('/report/employee/<emp_id>',methods=['GET','POST'])
def report_by_emp(emp_id):
	if request.method == 'GET':
		return read_file('frontend/emp_rep.html').format(emp_id,"")
	elif request.method == 'POST':
		data = request.form.to_dict()
		a = data['reason']
		if len(a)<10:
			return read_file('frontend/user_rep.html').format(user_id,'Reason should be more than 10 characters')
		insert_report_emp(emp_id,a)
		return read_file('frontend/emp_rep.html').format(emp_id,'Reported!')

@app.route('/report/user/<user_id>',methods=['GET','POST'])
def report_by_user(user_id):
	if request.method == 'GET':
		return read_file('frontend/user_rep.html').format(user_id,"")
	elif request.method == 'POST':
		data = request.form.to_dict()
		a = data['reason']
		if len(a)<10:
			return read_file('frontend/user_rep.html').format(user_id,'Reason should be more than 10 characters')
		insert_report_user(user_id,a)
		return read_file('frontend/user_rep.html').format(user_id,'Reported!')

@app.route('/view_reports',methods=['GET'])
def view_reps():
	fine = print_fine()
	emp_rep = print_report_emp()
	user_rep = print_report_user()
	str1 = """<tr>
    <th>Fine ID</th>
    <th>Employee</th>
    <th>User</th>
    <th>Reason</th>
    <th>Amount</th>
  </tr>"""
	str2 = """<tr>
    <th>Report ID</th>
    <th>Employee</th>
    <th>Problem</th>
  </tr>"""
	str3 = """<tr>
    <th>Report ID</th>
    <th>User</th>
    <th>Problem</th>
  </tr>"""

	for i in fine:
		str1 += """<tr>"""
		for j in i:
			str1 += """<th>{}</th>""".format(j)
		str1 += """<tr>"""

	for i in emp_rep:
		str2 += """<tr>"""
		for j in i:
			str2 += """<th>{}</th>""".format(j)
		str2 += """<tr>"""

	for i in user_rep:
		str3 += """<tr>"""
		for j in i:
			str3 += """<th>{}</th>""".format(j)
		str3 += """<tr>"""

	return read_file('frontend/view_reports.html').format(str1,str2,str3)

@app.route('/balance/<user_id>/<typ>',methods=['GET','POST'])
def balance(user_id,typ):
	if request.method == 'GET':
		my = print_account(user_id)
		if len(my)==0:
			return read_file('frontend/card_details.html').format(user_id,"")
		else:
			out = my[0]
			return read_file('frontend/bal_page.html').format(out[1],out[2],out[3],out[4],user_id)
	elif request.method == 'POST':
		if typ == 'card':
			data = request.form.to_dict()
			cc = data['cc']
			ed = data['ed']
			cvc = data['cvc']
			if len(cc)!=16 or len(ed)!=5 or len(cvc)!=3:
				return read_file('frontend/card_details.html').format(user_id,"Values not entered correcelty")
			ins = insert_balance(user_id,cc,ed,cvc)
			if ins:
				my = print_account(user_id)
				out = my[0]
				return read_file('frontend/bal_page.html').format(out[1],out[2],out[3],out[4],user_id)
			else:
				return read_file('frontend/card_details.html').format(user_id,"Values not entered correcelty")
		elif typ == 'update':
			up = update_balance(user_id,0)
			if not up:
				return "error"
			my = print_account(user_id)
			out = my[0]
			return read_file('frontend/bal_page.html').format(out[1],out[2],out[3],out[4],user_id)+"""<p> Updated</p>"""

@app.route('/fine/<emp_id>',methods=['GET','POST'])
def fine_emp(emp_id):
	if request.method == 'GET':
		return read_file('frontend/emp_fine.html').format(emp_id,"")
	elif request.method == 'POST':
		data = request.form.to_dict()
		uid = data['user']
		fine = data['fine']
		reason = data['reason']
		if len(reason)==0 or len(fine)==0 or len(uid)==0:
			return read_file('frontend/emp_fine.html').format(emp_id,"Values not entered correcelty")
		try:
			amount = int(fine)
		except:
			return read_file('frontend/emp_fine.html').format(emp_id,"Fine is a number.")
		Updated = update_balance(uid,amount)
		if Updated:
			insert_fine(emp_id,uid,reason,amount)
			return read_file('frontend/emp_fine.html').format(emp_id,"Amount added to the user account")
		else:
			return read_file('frontend/emp_fine.html').format(emp_id,"user does not exist")

@app.route('/trains',methods=['GET','POST'])
def train():
	if request.method == 'GET':
		out = print_train()
		str1 = """<tr><th>Train ID</th><th>Name</th><th>Class</th></tr>"""
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """<tr>"""
		return read_file('frontend/trains.html').format(str1,"")
	elif request.method == 'POST':
		data = request.form.to_dict()
		name = data['name']
		cla = data['class']
		if len(name)==0 or len(cla)==0:
			out = print_train()
			str1 = """<tr><th>Train ID</th><th>Name</th><th>Class</th></tr>"""
			for i in out:
				str1 += """<tr>"""
				for j in i:
					str1 += """<th>{}</th>""".format(j)
				str1 += """</tr>"""
			return read_file('frontend/trains.html').format(str1,"can't be empty")

		inser_train(name,cla)
		out = print_train()
		str1 = """<tr><th>Train ID</th><th>Name</th><th>Class</th></tr>"""
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
		return read_file('frontend/trains.html').format(str1,"added")

@app.route('/stations',methods=['GET','POST'])
def stations():
	if request.method == 'GET':
		out = print_station()
		str1 = """<tr><th>Station ID</th><th>Name</th></tr>"""
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
		return read_file('frontend/stations.html').format(str1,"")
	elif request.method == 'POST':
		data = request.form.to_dict()
		name = data['name']
		if len(name)==0:
			out = print_station()
			str1 = """<tr><th>Station ID</th><th>Name</th></tr>"""
			for i in out:
				str1 += """<tr>"""
				for j in i:
					str1 += """<th>{}</th>""".format(j)
				str1 += """</tr>"""
			return read_file('frontend/stations.html').format(str1,"can't be empty")

		k = insert_staton_name(name)
		out = print_station()
		str1 = """<tr><th>Station ID</th><th>Name</th></tr>"""
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """<tr>"""
		s = "station added or already there! id is {}".format(k)
		return read_file('frontend/stations.html').format(str1,s)

@app.route('/trip',methods=['GET'])
def trip_S():
	return read_file('frontend/trip.html').format("")

@app.route('/trip/add/<typ>',methods=['GET','POST'])
def add_trip(typ):
	if request.method == 'GET':
		return read_file('frontend/trip_add1.html').format("")
	elif request.method == 'POST':
		if typ == 'add1':
			data = request.form.to_dict()
			tid = data['tid']
			n = data['num']
			cap = data['capacity']
			price = data['price']
			st = select_train(tid)
			if len(st)==0:
				return read_file('frontend/trip_add1.html').format("Invalid Train ID")
			try:
				num = int(n)
			except:
				return read_file('frontend/trip_add1.html').format("Number of stations must be a number")
			try:
				capacity = int(cap)
			except:
				return read_file('frontend/trip_add1.html').format("capacity must be integer")
			try:
				p = int(price)
			except:
				return read_file('frontend/trip_add1.html').format("price must be number")
			trip_id = insert_train_info(tid,num,capacity,p)

			count = 0
			string = ""
			for i in range(1,num+1):
				string += """<label for="s{}">Station {} ID:</label>
		<input type="text" id="s{}" name="s{}"><br>

		<label for="st1{}">Start Time {}:</label>
		<input type="text" id="st1{}" name="st1{}">
		<input type="text" id="st2{}" name="st2{}">
		<label for="sap{}">AM/PM:</label>
  		<select name="sap{}" id="sap{}">
    		<option value="A">AM</option>
    		<option value="P">PM</option>
    	</select>

		<label for="et1{}">Time to next station {} ID:</label>
		<input type="text" id="et1{}" name="et1{}">
		<input type="text" id="et2{}" name="et2{}">
		<label for="eap{}">AM/PM:</label>
  		<select name="eap{}" id="eap{}">
    		<option value="A">AM</option>
    		<option value="P">PM</option>
    	</select><br><br>""".format(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)

			return read_file('frontend/trip_add2.html').format(trip_id,num,string)
		elif typ == 'add2':
			data = request.form.to_dict()
			trip_id = data['tid']
			num = data['num']
			try:
				n = int(num)
			except:
				return "error in numer of stations"
			dic = {}
			a = []
			for i in range(1,n+1):
				st = 's{}'.format(i)
				a.append(data[st])
				st = 'st1{}'.format(i)
				a.append(data[st])
				st = 'st2{}'.format(i)
				a.append(data[st])
				st = 'sap{}'.format(i)
				a.append(data[st])
				st = 'et1{}'.format(i)
				a.append(data[st])
				st = 'et2{}'.format(i)
				a.append(data[st])
				st = 'eap{}'.format(i)
				a.append(data[st])
				dic[i]=a
				a = []
				b = []
			for i in range(1,n):
				a = dic[i]
				start = a[0]
				st1 = hour_to_min(a[1],a[2],a[3])
				et1 = hour_to_min(a[4],a[5],a[6])
				b = dic[i+1]
				end = b[0]
				insert_station(start,trip_id,end,st1,et1)
			return read_file('frontend/trip.html').format("Added the trip")

@app.route('/trip/update',methods=['GET','POST'])
def up_trip():
	if request.method == 'GET':
		return read_file('frontend/update_trip.html').format("")
	elif request.method == 'POST':
		data = request.form.to_dict()
		tid = data['tid']
		k = check_trip_id(tid)
		if len(k)==0:
			return read_file('frontend/update_trip.html').format("Invalid trip Id")
		val = data['val']
		select = data['select']
		try:
			v = int(val)
		except:
			return read_file('frontend/update_trip.html').format("value must be a number")
		if select=='price':
			update_price(tid,v)
			return read_file('frontend/update_trip.html').format("Update the price!")
		elif select=='cap':
			update_cap(tid,v)
			return read_file('frontend/update_trip.html').format("Capacity updated!")

@app.route('/view_timetable',methods=['GET'])
def view_t():
	out = database.view_sch()
	str1 = """<tr><th>Station Name</th><th>Trip Id</th><th>Train Name</th><th>Next Station</th><th>Start Time</th><th>End Time</th><th>Capacity</th><th>Price</th></tr>"""
	dic = {}
	a = []
	for i in out:
		a.append(get_station_name(i[0]))
		a.append(i[1])
		a.append(get_train_name(i[1]))
		a.append(get_station_name(i[2]))
		a.append(min_to_hour(i[3]))
		a.append(min_to_hour(i[4]))
		a.append(get_price_cap(i[1])[0])
		a.append(get_price_cap(i[1])[1])
		dic[i] = a
		a = []

	for i in dic:
		str1 += """<tr>"""
		a = dic[i]
		for j in a:
			str1 += """<th> {} </th>""".format(j)
		str1 += """</tr>"""

	return read_file('frontend/view.html').format(str1)

@app.route('/book/<user_id>/<typ>',methods=['GET','POST'])
def book_ticket(user_id,typ):
	if request.method == 'GET':
		bal = print_account(user_id)
		if len(bal)==0:
			return read_file('frontend/inserted.html').format(user_id)
		return read_file('frontend/book_ticket.html').format(user_id,"",user_id,"")
	elif request.method == 'POST':
		if typ == 'search':
			data = request.form.to_dict()
			start = data['from']
			st_id = get_staton_id(start)
			if st_id==0:
				s1 = "No train leaving from {} ".format(start)
				return read_file('frontend/book_ticket.html').format(user_id,s1,user_id,"")
			end = data['to']
			ed_id = get_staton_id(end)
			if ed_id==0:
				s1 = "No train going to {} ".format(end)
				return read_file('frontend/book_ticket.html').format(user_id,s1,user_id,"")
			t1 = data['st']
			t2 = data['st2']
			t3 = data['sap']
			time = hour_to_min(t1,t2,t3)
			route = find_route(int(st_id),int(ed_id),time)
			if len(route)==0:
				return read_file('frontend/book_ticket.html').format(user_id,"""<br>No Trains Leaving for selected route""",user_id,"")
			str1 = """<tr><th>Trip ID</th><th>FROM</th><th>TIME</th><th>TO</th><th>TIME</th><th>TRAIN NAME</th><th>CAP</th><th>Filled</th><th>Price</th></tr>"""
			a = []
			dic = {}
			for i in route:
				a.append(i)
				a.append(start)
				a.append(min_to_hour(route[i][1]))
				a.append(end)
				a.append(min_to_hour(route[i][3]))
				a.append(get_train_name(i))
				a.append(get_price_cap(i)[0])
				a.append(get_filed(i))
				a.append(get_price_cap(i)[1])
				dic[i] = a
				a = []

			s = str1
			for i in dic:
				s += """<tr>"""
				a = dic[i]
				for j in a:
					s += """<th> {} </th>""".format(j)
				s += """<tr>"""
			return read_file('frontend/book_ticket.html').format(user_id,s,user_id,"")
		if typ == 'book':
			data = request.form.to_dict()
			a = data['tid']
			f = data['from']
			t = data['to']
			if not check_trip_id(a):
				return read_file('frontend/book_ticket.html').format(user_id,"",user_id,"Trip id is invalid")
			book = for_book(f,t,a)
			if len(book) != 2:
				return read_file('frontend/book_ticket.html').format(user_id,"",user_id,"No trip exists for given entries")
			cap,price = get_price_cap(a)
			filled = get_filed(a)
			if filled<cap:
				done = update_balance(user_id,price)
				if done:
					ticket = insert_booking(a,user_id,f,book[0],t,book[1])
					s = "<br>Trip booked. Your ticket number is {}".format(ticket)
					return read_file('frontend/book_ticket.html').format(user_id,"",user_id,s)
				else:
					s = "<br>Encountered error while billing! No booking!"
					return read_file('frontend/book_ticket.html').format(user_id,"",user_id,s)
			else:
				s = "Trip is fully booked! <br>"
				return read_file('frontend/book_ticket.html').format(user_id,"",user_id,s)

@app.route('/tickets/<user_id>',methods=['GET','POST'])
def view_tic(user_id):
	if request.method == 'GET':
		str1 = """<tr><th>Ticket ID</th><th>Trip ID</th><th>User ID</th><th>FROM</th><th>TIME</th><th>TO</th><th>TIME</th></tr>"""
		out = view_ticket(user_id)
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
		return read_file('frontend/view_tickets.html').format(str1,user_id,"")
	elif request.method == 'POST':
		data = request.form.to_dict()
		tid = data['tid']
		str1 = """<tr><th>Ticket ID</th><th>Trip ID</th><th>User ID</th><th>FROM</th><th>TIME</th><th>TO</th><th>TIME</th></tr>"""
		out = view_ticket(user_id)
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
		ret = check_ticket(tid)
		if len(ret)==0:
			return read_file('frontend/view_tickets.html').format(str1,user_id,"Ticket ID is invalid")
		d = del_ticket(tid)
		str1 = """<tr><th>Ticket ID</th><th>Trip ID</th><th>User ID</th><th>FROM</th><th>TIME</th><th>TO</th><th>TIME</th></tr>"""
		out = view_ticket(user_id)
		for i in out:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
		return read_file('frontend/view_tickets.html').format(str1,user_id,"Ticket Removed!")

@app.route('/cticket',methods=['GET','POST'])
def cticker():
	if request.method == 'GET':
		return read_file('frontend/cticket.html').format("","")
	elif request.method == 'POST':
		data = request.form.to_dict()
		t = data['tid']
		a = check_ticket(t)
		if len(a)==0:
			return read_file('frontend/cticket.html').format("The Ticket number is Invalid","")
		user = a[0][2]
		out = select_user(user)
		str1 = """<tr><th>User ID</th><th>First Name</th><th>Last Name</th><th>Email</th><th>Address</th></tr>"""
		count = 0
		for i in out:
			str1 += """<tr>"""
			for j in i:
				count +=1
				if count!=4:
					str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
			count = 0
			s = "The ticket belongs to {}".format(user)
		return read_file('frontend/cticket.html').format(s,str1)

@app.route('/trip_users',methods=['GET','POST'])
def trip_users():
	if request.method == 'GET':
		return read_file('frontend/trip_user.html').format("Search Results will appear below","")
	elif request.method == 'POST':
		data = request.form.to_dict()
		d = data['tid']
		r = cticket(d)
		if len(r)==0:
			return read_file('frontend/trip_user.html').format("NO Results Found for the given trip id","")
		str1 = """<tr><th>Tickets Bought</th><th>User ID</th><th>First Name</th><th>Last Name</th></tr>"""
		for i in r:
			str1 += """<tr>"""
			for j in i:
				str1 += """<th>{}</th>""".format(j)
			str1 += """</tr>"""
		return read_file('frontend/trip_user.html').format("Users for trip",str1)

@app.route('/test',methods=['GET'])
def test():
	return read_file('frontend/panel.html')

if __name__ == '__main__':
	app.run(debug=True)