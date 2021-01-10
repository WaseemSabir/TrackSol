import sqlite3
from func import *

def create_user_table():
	conn =sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE user(
		user_id text,
		user_fname text,
		user_lname text,
		user_pass text,
		user_email text,
		user_address text,
		PRIMARY KEY(user_id)
		)
		""")
	conn.commit()
	conn.close()

def create_admin_table():
	conn =sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE admin(
		add_id text,
		add_fname text,
		add_lname text,
		add_pass text,
		add_gender text,
		add_age text,
		add_email text,
		add_address text,
		add_pos text,
		PRIMARY KEY(add_id)
		)
		""")
	conn.commit()
	conn.close()


def create_emp_table():
	conn =sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE employee(
		emp_id text,
		emp_fname text,
		emp_lname text,
		emp_pass text,
		emp_gender text,
		emp_age text,
		emp_email text,
		emp_address text,
		emp_pos text,
		PRIMARY KEY(emp_id)
		)
		""")
	conn.commit()
	conn.close()

def create_balance_table():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE balance(
		user_id text,
		card_num text,
		expiry text,
		cvc text,
		user_balnce INTEGER DEFAULT 0,
		FOREIGN KEY (user_id) REFERENCES user (user_id)
		)""")
	conn.commit()
	conn.close()

def review():
	conn =sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE review(
		uid text,
		rev text)""")
	conn.commit()
	conn.close()


def jobs_table():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE jobs(
		job_id INTEGER PRIMARY KEY AUTOINCREMENT,
		emp_id text,
		job text)""")
	conn.commit()
	conn.close()

def station_table():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE station(
			station_id INTEGER,
			trip_id INTEGER,
			next_station_id INTEGER,
			stat_time INTEGER,
			end_time INTEGER,
			FOREIGN KEY (trip_id) REFERENCES trips (trip_id)
			)
			""")
	conn.commit()
	conn.close()

def booking_info():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE booking(
			ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id text,
			trip_id text
			)
			""")
	conn.commit()
	conn.close()

def trip_info():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE trips(
			trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
			train_id text NOT NULL,
			num_stations INTEGER NOT NULL,
			capcity INTEGER DEFAULT 20,
			filled INTEGER DEFAULT 0,
			price INTEGER NOT NULL,
			FOREIGN KEY (train_id) REFERENCES train (train_id)
			)
			""")
	conn.commit()
	conn.close()

def station_names():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE names(
			stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
			name text NOT NULL
			)
			""")
	conn.commit()
	conn.close()

def train():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE train (
			train_id INTEGER PRIMARY KEY AUTOINCREMENT,
			name text NOT NULL,
			class text
			)
			""")
	conn.commit()
	conn.close()

def fine_his():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE fine (
			fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
			emp_id text,
			user text,
			reason text
			)
			""")
	conn.commit()
	conn.close()

def report_emp():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE emp_report (
			rep_id INTEGER PRIMARY KEY AUTOINCREMENT,
			emp_id text,
			problem text
			)
			""")
	conn.commit()
	conn.close()

def report_user():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	db.execute("""CREATE TABLE user_report (
			rep_id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id text,
			problem text
			)
			""")
	conn.commit()
	conn.close()

def alter_fine():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""ALTER TABLE fine ADD amount INTEGER""")

def alter_ticket():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""ALTER TABLE booking ADD start text""")
		db.execute("""ALTER TABLE booking ADD stime text""")
		db.execute("""ALTER TABLE booking ADD ends text""")
		db.execute("""ALTER TABLE booking ADD etime text""")

def alter_book():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""DELETE FROM booking where ticket_id=1""")

def select_ticket():
	conn = sqlite3.connect("database/tracksol.db")
	db = conn.cursor()
	with conn:
		db.execute("""PRAGMA table_info(booking);""")
	return db.fetchall()

if __name__ == '__main__':
	#To create tables
	#create_user_table()
	#create_admin_table()
	#create_emp_table()
	#review()
	#jobs_table()
	#station_table()
	#create_balance_table()
	#booking_info()
	#station_names()
	#trip_info()
	#train()
	#insert_data_admin_table('waseem12','Waseem','Sabir','ws123','male','20','waseem@tracksol.com','Lums, dha phase 5, Lahore','exective')
	#insert_data_emp_table('alihas12','Ali','Hassan','ali123','male','20','alihassan@tracksol.com','Lums, dha , lahore','Station Master')
	#insert_data_user_table('tayyab12','tayyab','Hussian','12345678','tayyab@gmail.com','Multan gali number 2')
	#fine_his()
	#report_emp()
	#report_user()
	#alter_fine()
	#alter_ticket()
	#print(select_ticket())
	print('ok')