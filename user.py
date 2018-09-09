import os
import MySQLdb
import user_ldap

def get_mysql_connection(cursor_type=1):
	host = DBHOST
	username = DBUSER
	password = DBPASSWORD
	dbname = DBNAME
	port = DBPORT
	
	try:
		conn = MySQLdb.connect(host=host,user=username,passwd=password,db=dbname,port=port)
		if cursor_type == 0:
			cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		else:
			cursor = conn.cursor()
		return cursor
	
	except Exception as e:
		print e
		exit(1)
		
def add_user(username):
	rst = user_ldap.get_dn(username)
	if rst is None:
		print 'User %s is not exists,please check it!' % username
		exit(20)
		
	t = rst.split('.')[0]
	display_name = t.split('=')[1]
	
	cur = get_mysql_connection(1)
	sql = 'select id from users where username="%s"' % username
	cur.execute(sql)
	rst = cur.fetchall()
	if rst:
		print 'User [ %s ] is already exist, Exit!' % username
		exit(10)
	sj = time.strftime('%F %T')
	display_name = display_name
	allow_login = sj
	last_login = sj
	
	sql = 'insert into users(username,display_name,allow_login,last_login) values ("%"s,"%s","%s","%s")' % (username,display_name,allow_login,last_login)
	try:
		cur.execute(sql)
		return 0
	except Exception as e:
		print e
		exit(20)
	conn.close()
	
def del_user(username):
	cur = get_mysql_connection(1)
	sql = 'delete from users where username="%s"' % username
	try:
		cur.execute(sql)
		return 0
	except Exception as e:
		print e
		return(20)
	conn.close()
	
def list_user(username):
	pass
	
def alter_user(username):
	pass
	
def users(args):
	cmdlist = ['add','del','alter','list','show']
	cmd = args[2]
	if cmd not in cmdlist:
		print 'user command %s is not unrecognized,use commands below:' % cmd
		print ' add <username>		:add a user'
		print ' del <username>		:delete a user'
		print ' alter <username> <key> <value>		:edit user property'
		print ' list 	:list users'
		print ' show <usrname> 	:show user property'
		exit(3)
		
	argnum = len(args)
	if cmd == 'add':
		if argnum == 4:
			add_user(sys.argv[3])
		else:
			print 'Args Error,command add need 1 args'
			exit(10)
	
	if cmd == 'del':
		if argnum == 4:
			del_user(sys.argv[3])
		else:
			print 'Args Error,command del need 1 args'
			exit(10)
	
	if cmd == 'show':
		if argnum == 4:
			show_user(sys.argv[3])
		else:
			print 'Args Error,command show need 1 args'
			exit(10)
	
	if cmd == 'list':
		if argnum == 3:
			list_user()
		else:
			print 'Args Error,command list not need args'
			exit(10)

	if cmd == 'alter':
		if argnum == 6:
			alter_user(sys.argv[3])
		else:
			print 'Args Error,command alter needs 3 args'
			exit(10)
