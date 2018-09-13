#coding:utf-8
#route.py

import MySQLdb
import user_ldap

def route_create(route,comment):
	pass	

def route_del(route_id):
	pass

def route_list(ls_tag):
	pass

def route_add(username,route_id):
	pass

def get_mysql_connection(cursor_type):
	host = '172.16.172.100'
	username = 'openvpn'
	dbname = 'openvpn'
	password = 'vdin1234'
	port = 3306

	try:
		conn = MySQLdb.connect(host=host,user=username,passwd=password,db=dbname,port=port,use_unicode=True, charset="utf8")
		if cursor_type == 0:
			cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		else:
			cursor = conn.cursor()
		return cursor,conn
	
	except Exception as e:
		print e
		exit(1)

def routes(args):
	routelist = ['create','del','add','list','show']
	cmd = args[2]
	if cmd not in routelist:
		print '命令 [ %s ] 未被识别，请尝试以下命令：' % cmd
		print '%-30s %s' % (' create <route> [commet]',':创建虚拟路由')
		print '%-30s %s' % (' del <route-id>',':删除虚拟路由')
		print '%-30s %s' % (' add <route-id> <username>',':用户路由绑定')
		print '%-30s %s' % (' list',':显示所有虚拟路由')
		exit(3)
	argnum = len(args)
	if cmd == 'create':
		if argnum == 4:
			route_create(args[3],'0')
		elif argnum == 5:
			route_create(args[3],args[4])
		else:
			print 'Error,use route create <route> [comment]'
			exit(10)
	if cmd == 'del':
		if argnum == 4:
			route_del(args[3])
		else:
			print 'Error,use route del <route-id>'
			exit(30)
	if cmd == 'add':
		if argnum == 5:
			route_add(args[3],args[4])
		else:
			print 'Error,use route add <username> <route-id>'
			exit(3)
	if cmd == 'list':
		if argnum == 3:
			route_list('0')
		elif argnum == 4:
			route_list(args[3])
		else:
			print 'Error,use route list or route list <username>'
			exit(3)

def check_ip(ip):
	pass 
