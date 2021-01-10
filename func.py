import sqlite3

def read_file(filename):
	read = open(filename,mode='r')
	file = read.read()
	read.close()
	return file

def insert_data_user_table(u_id,u_fn,u_ln,u_p,u_e,u_add):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("INSERT INTO user VALUES(?,?,?,?,?,?)",(u_id,u_fn,u_ln,u_p,u_e,u_add))

def insert_data_admin_table(u_id,u_fn,u_ln,u_p,u_g,u_a,u_e,u_add,pos):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("INSERT INTO admin VALUES(?,?,?,?,?,?,?,?,?)",(u_id,u_fn,u_ln,u_p,u_g,u_a,u_e,u_add,pos))

def insert_data_emp_table(u_id,u_fn,u_ln,u_p,u_g,u_a,u_e,u_add,pos):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("INSERT INTO employee VALUES(?,?,?,?,?,?,?,?,?)",(u_id,u_fn,u_ln,u_p,u_g,u_a,u_e,u_add,pos))

def search_users(typ,search_query):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""SELECT * FROM user where {} like '%{}%' """.format(typ,search_query))
	output = db.fetchall()
	return output

def search_employee(typ,search_query):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM employee where {} like '%{}%'".format(typ,search_query))
	output = db.fetchall()
	return output

def update_user(fname,lname,pas,email,address,uid):
	con=sqlite3.connect("database/tracksol.db")
	c=con.cursor()
	c.execute(("""UPDATE user SET user_fname=?, user_lname=?,user_pass=?,user_email=?,user_address=? WHERE user_id=?"""),(fname,lname,pas,email,address,uid))
	con.commit()
	con.close()

def update_emp(fname,lname,pas,gender,age,email,address,uid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute(("""UPDATE employee SET emp_fname=?, emp_lname=?,emp_pass=?,emp_gender=?,emp_age=?,emp_email=?,emp_address=? WHERE emp_id=?"""),(fname,lname,pas,gender,age,email,address,uid))
	conn.commit()
	conn.close()

def update_adm(fname,lname,pas,gender,age,email,address,uid):
	con=sqlite3.connect("database/tracksol.db")
	c=con.cursor()
	c.execute(("""UPDATE admin SET add_fname=?, add_lname=?,add_pass=?,add_gender=?,add_age=?,add_email=?,add_address=? WHERE add_id=?"""),(fname,lname,pas,gender,age,email,address,uid))
	con.commit()
	con.close()

def select_user(uid):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""SELECT * FROM user where user_id = '{}' """.format(uid))
	output = db.fetchall()
	return output

def select_employee(uid):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""SELECT * FROM employee where emp_id = '{}'""".format(uid))
	output = db.fetchall()
	return output

def delete_employee(uid):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""DELETE FROM employee where emp_id = '{}'""".format(uid))

def select_admin(uid):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""SELECT * FROM admin where add_id = '{}'""".format(uid))
	output = db.fetchall()
	return output

def insert_rev(uid,tex):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("INSERT INTO review VALUES(?,?)",(uid,tex))

def insert_station(station_name,station_id,trip_id,next_station,stat_time,end_time):
	conn=sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("INSERT INTO station VALUES(?,?,?,?,?,?)",(station_name,station_id,trip_id,next_station,stat_time,end_time))
	conn.commit()
	conn.close()

def route():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM station")
	output = db.fetchall()
	return output

def find_route(s_id,e_id,t):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM station where station_id='{}' and stat_time>'{}' GROUP BY trip_id ORDER BY stat_time".format(s_id,t))
	l=db.fetchall()
	arr = {}
	for i in l:
		temp = route_in_trip(s_id,e_id,i[1])
		if temp:
			arr[i[1]] = route_for_front(s_id,e_id,i[1])
	return arr

def for_book(start,end,tid):
	con=sqlite3.connect("database/tracksol.db")
	c=con.cursor()
	i1 = get_staton_id(start)
	i2 = get_staton_id(end)
	a = []
	if i1==0 or i2==0:
		return a
	c.execute("SELECT * FROM station where trip_id='{}'".format(tid))
	l=c.fetchall()
	for i in l:
		if i[0]== i1:
			m = min_to_hour(i[3])
			a.append(m)
		if i[2]== i2:
			m = min_to_hour(i[4])
			a.append(m)
	return a

def route_in_trip(start_id,end_id,tid):
	con=sqlite3.connect("database/tracksol.db")
	c=con.cursor()
	c.execute("SELECT * FROM station where station_id='{}' and trip_id='{}'".format(start_id,tid))
	l=c.fetchall()
	for i in l:
		if i[2]==end_id:
			return i
		else:
			return route_in_trip(i[2],end_id,tid)

def route_for_front(start,end,trip):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM station where trip_id='{}' ORDER BY stat_time".format(trip))
	out = db.fetchall()
	a = []
	for i in out:
		if i[0] == start:
			a.append(i[0])
			a.append(i[3])
			if (i[2] == end):
				a.append(i[2])
				a.append(i[4])
		elif i[2] == end:
			a.append(i[2])
			a.append(i[4])
	return a

def insert_job(uid,job):
	l=select_employee(uid)
	if(len(l)==0):
		return False
	else:
		conn = sqlite3.connect("database/tracksol.db")
		db = conn.cursor()
		db.execute("INSERT INTO jobs (emp_id,job) VALUES(?,?)",(uid,job))
		conn.commit()
		conn.close()
		return True

def search_jobs(uid):
	l=select_employee(uid)
	if len(l)==0:
		return l
	else:
		conn = sqlite3.connect("database/tracksol.db")
		db = conn.cursor()
		db.execute("SELECT job FROM jobs WHERE emp_id='{}'".format(uid))
		output = db.fetchall()
		return output

def delete_job(j_id):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM jobs WHERE job_id='{}'".format(j_id))
	output = db.fetchall()
	if len(output)==0:
		return False
	else:
		db.execute("""DELETE FROM jobs where job_id = '{}'""".format(j_id))
		return True

def min_to_hour(k):
	l=k%60
	n=k//60
	if n>=12:
		return str(n-12)+":"+str(l)+" P"
	else:
		return str(n)+":"+str(l)+" A"

def hour_to_min(hour,min,ty):
	if(ty=='P'):
		return int(hour)*60+int(min)+12*60
	else:
		return int(hour)*60+int(min)

def insert_balance(uid,cnum,exp,c):
	l=select_user(uid)
	if len(l)==0:
		return False
	else:
		conn = sqlite3.connect("database/tracksol.db")
		db = conn.cursor()
		db.execute("INSERT INTO  balance (user_id,card_num,expiry,cvc) VALUES(?,?,?,?)",(uid,cnum,exp,c))
		conn.commit()
		conn.close()
		return True

def update_balance(uid,mon):
	l=select_user(uid)
	if len(uid)==0:
		return False
	else:
		conn = sqlite3.connect("database/tracksol.db")
		db = conn.cursor()
		if mon==0:
			with conn:
				db.execute("""UPDATE balance SET user_balnce='{}'""".format(mon))
				return True
			return False
		db.execute("SELECT user_balnce FROM balance WHERE user_id='{}'".format(uid))
		l=db.fetchall()
		b=l[0][0]
		b=b+mon
		with conn:
			db.execute("""UPDATE balance SET user_balnce={}""".format(b))
			return True
		return False

def print_account(uid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()	
	db.execute("SELECT * FROM balance where user_id='{}'".format(uid))
	out = db.fetchall()
	return out

def insert_station(sid,tid,nexid,st,et):
 	conn = sqlite3.connect("database/tracksol.db")
 	db = conn.cursor()
 	db.execute("INSERT INTO  station (station_id,trip_id,next_station_id,stat_time,end_time) VALUES(?,?,?,?,?)",(sid,tid,nexid,st,et))
 	conn.commit()
 	conn.close()

def insert_staton_name(sname):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	sname = sname.capitalize()
	db.execute("SELECT name FROM names where name='{}'".format(sname))
	l=db.fetchall()
	if len(l)==0:
		db.execute("INSERT INTO names (name) VALUES (?)",(sname,))
		conn.commit()
		db.execute("SELECT stat_id FROM names where name='{}'".format(sname))
		p=db.fetchall()
		return p[0][0]
	else:
		db.execute("SELECT stat_id FROM names where name='{}'".format(sname))
		p=db.fetchall()
		return p[0][0]

def get_station_name(sid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT stat_id FROM names where stat_id='{}'".format(sid))
	l=db.fetchall()
	if len(l)==0:
		return l[0][0]
	else:
		db.execute("SELECT name FROM names where stat_id='{}'".format(sid))
		p=db.fetchall()
		return p[0][0]

def inser_train(n,c):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("INSERT INTO train (name,class) VALUES(?,?)",(n,c))	
	conn.commit()
	conn.close()

def insert_fine(eid,u,r,am):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("INSERT INTO fine (emp_id,user,reason,amount) VALUES(?,?,?,?)",(eid,u,r,am))
	conn.commit()
	conn.close()

def print_fine():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM fine")
	output = db.fetchall()
	return output

def print_station():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM names")
	output = db.fetchall()
	return output

def print_train():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM train")
	output = db.fetchall()
	return output

def select_train(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM train where train_id = '{}'".format(tid))
	output = db.fetchall()
	return output

def insert_report_emp(eid,u):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("INSERT INTO  emp_report (emp_id,problem) VALUES(?,?)",(eid,u))
	conn.commit()
	conn.close()

def print_report_emp():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM emp_report")
	output = db.fetchall()
	return output

def insert_report_user(eid,u):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("INSERT INTO  user_report (user_id,problem) VALUES(?,?)",(eid,u))
	conn.commit()
	conn.close()

def print_report_user():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM user_report")
	output = db.fetchall()
	conn.commit()
	conn.close()
	return output

def insert_train_info(tr_id,ns,c,p):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("INSERT INTO trips (train_id,num_stations,capcity,price) VALUES(?,?,?,?)",(tr_id,ns,c,p))
	conn.commit()
	db.execute("SELECT trip_id FROM trips WHERE train_id='{}' and num_stations='{}' and capcity='{}' and price='{}' ".format(tr_id,ns,c,p))
	output = db.fetchall()
	conn.commit()
	conn.close()
	return output[0][0]

def insert_booking(u,t,s,st,e,et):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("INSERT INTO booking (user_id,trip_id,start,stime,ends,etime) VALUES(?,?,?,?,?,?)",(u,t,s,st,e,et))
	db.execute("""SELECT last_insert_rowid()""")
	out = db.fetchall()
	return out[0][0]

def get_train_name(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""SELECT train_id FROM trips where trip_id={}""".format(tid))
	out = db.fetchall()
	tr_id = out[0][0]
	with conn:
		db.execute("""SELECT name FROM train where train_id={}""".format(tr_id))
	out2 = db.fetchall()
	return out2[0][0]

def get_price_cap(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""SELECT capcity,price FROM trips where trip_id={}""".format(tid))
	out = db.fetchall()
	return out[0]

def get_filed(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""SELECT filled FROM trips where trip_id={}""".format(tid))
	out = db.fetchall()
	return out[0][0]

def get_staton_id(sname):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	sn = sname.capitalize()
	db.execute("SELECT stat_id FROM names where name='{}'".format(sn))
	l=db.fetchall()
	if len(l)==0:
		print(0)
		return 0
	return l[0][0]

def check_trip_id(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("SELECT * FROM trips where trip_id ='{}'".format(tid))
	l = db.fetchall()
	return l

def del_trip(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("DELETE FROM trips where trip_id ='{}'".format(tid))
		return True
	return False

def filled_min(tripid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	fil = get_filed(tripid)
	f = fil-1
	with conn:
		db.execute("UPDATE trips SET filled ='{}' where trip_id='{}'".format(f,tripid))

def del_ticket(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	c = check_ticket(tid)
	tripid = c[0][1]
	filled_min(tripid)
	with conn:
		db.execute("DELETE FROM booking where ticket_id ='{}'".format(tid))
		return True
	return False

def view_ticket(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("SELECT * FROM booking where trip_id = '{}'".format(tid))
	l = db.fetchall()
	return l

def check_ticket(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("SELECT * FROM booking where ticket_id ='{}'".format(tid))
	l = db.fetchall()
	return l

def cticket(tid):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("SELECT DISTINCT trip_id FROM booking where user_id ='{}'".format(tid))
	out = db.fetchall()
	if len(out)==0:
		return out
	a = []
	for i in out:
		b = []
		db.execute("SELECT COUNT(trip_id) FROM booking where user_id ='{}' and trip_id = '{}'".format(tid,i[0]))
		temp = db.fetchall()
		b.append(temp[0][0])
		c = select_user(i[0])
		for j in c:
			count = 0
			for k in j:
				if count<3:
					b.append(j[count])
				count+=1
		a.append(b)
	return a

def update_price(tid,value):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("UPDATE trips SET price ='{}' where trip_id ='{}'".format(value,tid))

def update_cap(tid,value):
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("UPDATE trips SET capcity ='{}' where trip_id ='{}'".format(value,tid))