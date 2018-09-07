# manage users
# add,delete,alter

import MySQLdb

def add_user(username,displayname);
	cur = get_mysql_connection(1)
	sql = 'select id from users where username=%s' % username
	cur.execute(sql)
	rst = cur.fetchall()
	if rst:
		print 'User %s is already exist, Exit!'
		exit(10)
	sj = time.strftime('%F %T')
	display_name = display_name
	allow_login = sj
	last_login = sj
	
	sql = 'insert into users(username,display_name,allow_login,last_login) values (%s %s %s %s)' % (username,display_name,allow_login,last_login)
	try:
		cur.execute(sql)
		return 0
	except Exception as e
		print e
		exit(20)
	conn.close()
	
def del_user(username):
	cur = get_mysql_connection(1)
	sql = 'delete from users where username=%s' % username
	try:
		cur.execute(sql)
		return 0
	except Exception as e:
		print e
		return(20)
	conn.close()
	
def alt_user(username,**args):
	pass

def get_mysql_connection(cursor_type=1):
	host = '172.16.172.100'
	username = 'openvpn'
	password = 'vdin1234'
	port = 3306
	
	try:
		conn = MySQLdb.connect(host=host,user=username,passwd=password,db=dbname,port=port)
		if cursor_type == 1:
			cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		else:
			cursor = conn.cursor()
		return cursor
	
	except Exception as e:
		print e
		exit(1)
	
