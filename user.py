#coding:utf-8

import os
import sys
import time
import MySQLdb
import hashlib
import user_ldap
from datetime import *

def get_mysql_connection(cursor_type=1):
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
		
def add_user(username):
	rst = user_ldap.get_dn(username)
	if rst is None:
		print '用户 [ %s ] 不存在，添加用户失败!' % username
		exit(20)
		
	t = rst.split(',')[0]
	display_name = t.split('=')[1]
	(cur,conn) = get_mysql_connection(1)
	sql = 'select id from users where username="%s"' % username
	cur.execute(sql)
	rst = cur.fetchall()
	if rst:
		print '用户 [ %s ] 已存在，添加用户失败' % username
		exit(10)
	sj = time.strftime('%F %T')
	display_name = display_name
	allow_login = sj
	last_login = sj
	
	sql = 'insert into users(username,display_name,allow_login,last_login) values ("%s","%s","%s","%s")' % (username,display_name,allow_login,last_login)
	try:
		cur.execute(sql)
		conn.commit()
		print '添加用户 [ %s ] 成功' % username
		return 0
	except Exception as e:
		print e
		conn.rollback()
		exit(20)
	conn.close()
	
def del_user(username):
	(cur,conn) = get_mysql_connection(1)
	sql = 'delete from users where username="%s"' % username
	try:
		rst = cur.execute(sql)
		if rst != 0:
			print '删除用户 [ %s ] 成功' % username
			conn.commit()
		else:
			print '用户 [ %s ] 不存在，删除失败' % username
		return 0
	except Exception as e:
		print e
		conn.rollback()
		return(20)
	conn.close()
	
def list_user():
	(cur,conn) = get_mysql_connection(0)
	sql = 'select display_name,deration,received,sent,locked,last_login from users;'
	cur.execute(sql)
	rst = cur.fetchall()
	if rst is None:
		print '没有任何用户.'
		exit(5)
	sep = 110
	gap = 10
	print '-' * sep
	print '用户' + ' '* gap + '连接时长' + ' ' * gap + '接收字节' + ' ' * gap + '发送字节'+ ' ' * gap + '是否锁定' + ' ' * gap + '最后登录时间'
	print '-' * sep
	for i in rst:
		if i['locked'] == '0':
			locked = 'False'
		else:
			locked = 'True'
		deration = get_deration(i['deration'])
		received = get_traffic(i['received'])
		sent = get_traffic(i['sent'])
		if len(i['display_name']) == 2:
			print '%-11s %-17s %-17s %-17s %-17s %-16s' % (i['display_name'],deration,received,sent,locked,i['last_login']) 
		else:
			print '%-10s %-17s %-17s %-17s %-17s %-16s' % (i['display_name'],deration,received,sent,locked,i['last_login'    ]) 
		print '-' * sep
	conn.close()
	exit(0)
	
def show_user(username):
	(cur,conn) = get_mysql_connection(0)
	sql = 'select * from users where username="%s"' % username
	cur.execute(sql)
	rst = cur.fetchone()
	if rst is None:
		print '用户 [ %s ] 不存在' % username
		exit(10)
	sep = 45
	gap = 10
	print '-' * sep
	print '%-19s| %-23s-' % ('ID:',rst['id'])
	print '-' * sep
	print '%-17s| %-23s-' % (u'帐号:',rst['username'])
	print '-' * sep
	#print len(rst['display_name'])
	if len(rst['display_name']) == 2:
		print '%-17s| %-21s-' % (u'姓名:',rst['display_name'])
	else:
		print '%-17s| %-20s-' % (u'姓名:',rst['display_name'])
	print '-' * sep
	print '%-15s| %-23s-' % (u'登录次数:',rst['logins'])
	print '-' * sep
	if rst['locked'] == '0':
		locked = 'False'
	else:
		locked = 'True'
	print '%-15s| %-23s-' % (u'是否锁定:',locked)
	print '-' * sep
	print '%-13s| %-23s-' % (u'允许登录时间:',rst['allow_login'])
	print '-' * sep
	print '%-15s| %-23s-' % (u'连接时长:',rst['deration'])
	print '-' * sep
	print '%-15s| %-23s-' % (u'接收字节(KB):',rst['received'])
	print '-' * sep
	print '%-15s| %-23s-' % (u'发送字节(KB):',rst['sent'])
	print '-' * sep
	print '%-13s| %-23s-' % (u'最后登录时间:',rst['last_login'])
	print '-' * sep
	print '%-15s| %-23s-' % (u'最后登录IP:',rst['last_ip'])
	print '-' * sep
	print '%-15s| %-23s-' % (u'流量配额:',rst['quota'])
	print '-' * sep
	cur.close()
	conn.close()
	exit(0)

def alter_user(username,k,v):
	altlist = ['password','logins','locked','allow_login','deration','received','sent','quota']
	'''
	prolist = ['%-15s','%-15s','%-15s','%-15s','%-15s','%-15s','%-15s','%-15s'] % (
			':change user password',
			':change user login times',
			':lock or unlock user account',
			':allow user login after this allow_login',
			':total use time, unit: s',
			':total received bytes,unit: kb',
			':total sent bytes,unit: kb',
			':quota a month,unit: kb')
	'''
	if k not in altlist:
		print '属性 [ %s ] 不被支持，请尝试以下 :\n' % k
		print '%-15s:修改用户密码' % altlist[0]
		print '%-15s:修改登录次数' % altlist[1]
		print '%-15s:锁定或解锁帐号' % altlist[2]
		print '%-15s:设置用户允许登录时间，只有此时间之后才可以登录' % altlist[3]
		print '%-15s:修改用户在线时间，单位：秒' % altlist[4]
		print '%-15s:修改用户总接收字节数，单位：kb' % altlist[5]
		print '%-15s:修改用户总发送字节数，单位：kb' % altlist[6]
		print '%-15s:修改用户配额，单位：kb' % altlist[7]
		exit(10)

	(cur,conn) = get_mysql_connection(1)
	sql = 'select id from users where username="%s"' % username
	cur.execute(sql)
	rst = cur.fetchone()
	if rst is None:
		print '用户 [ %s ] 不存在，修改失败 ' % username
		cur.close()
		conn.close()
		exit(10)
	try:
		if k == 'password':
			password = get_password(v)
			sql = 'update users set password="%s" where username="%s"' % (password,username) 
			#cur.execute(sql)
			#conn.commit()
			print '用户 [ %s ] 密码修改成功' % username
			exit(0)
		if k == 'logins':
			if v.isdigit():
				sql = 'update users set logins=%d where username="%s"' % (int(v),username)
				print '用户 [ %s ] 登录次数已修改为 [ %s ]' % (username,v)
			else:
				print '登录次数必须为整数，修改失败'
				exit(11)
		if k == 'locked':
			if v == 'yes'or v == 'true':
				sql = 'update users set update="1" where username="%s"' % (username)
				print '[ %s ] 已被锁定' % username
			elif v == 'no' or v == 'false':
				sql = 'update users set update="0" where username="%s"' % (username)
				print '[ %s ] 已解锁' % username
			else:
				print '锁定解锁必须是 yes|no|true|false'
				exit(11)
		if k == 'allow_login':
			timetag = '%Y-%m-%d %H:%M:%S'
			try:
				sj1 = datetime.strptime(v,timetag)
				sql = 'update users set allow_login="%s" where username="%s"' % (v,username)
				print '已设置登录时间为 [ %s ],必须晚于此时间才可以登录'  % (v)
			except:
				print "时间格式必须是：YYYY-MM-DD HH:MM:SS"
				exit(11)
		if k == 'deration':
			if v.isdigit():
				sql = 'update users set deration=%d where username="%s"' % (int(v),username)
				print '用户[ %s ]的持续时间已设置为[ %s ]' % (username,v)
			else:
				print '持续时间必须为整数'
				exit(11)
		if k == 'received':
			if v.isdigit():
				sql = 'update users set received=%d where username="%s"' % (int(v),username)
				print '用户 [ %s ] 的接收字节数已设置为 [ %s ]' % (username,v)
			else:
				print '接收字节数必须为整数'
				exit(11)
		if k == 'sent':
			if v.isdigit():
				sql = 'update users set sent=%d where username="%s"' % (int(v),username)
				print '用户 [ %s ] 的发送字节数已设置为 [ %s ]' %  (username,v)
			else:
				print '接收字节数必须为整数'
				exit(11)
		if k == 'quota':
			if v.isdigit():
				sql = 'update users set quota=%d where username="%s"' % (int(v),username)
				print '用户 [ %s ] 的配额已设置为 [ %s ]' % (username,v)
			else:
				print '用户配额必须为整数'
				exit(11)
		cur.execute(sql)
		conn.commit()
	except Exception as e:
		print e

def users(args):
	cmdlist = ['add','del','alter','list','show']
	cmd = args[2]
	if cmd not in cmdlist:
		print ' 命令 [ %s ] 未被识别，请尝试以下命令：' % cmd
		print '%-35s %s' % (' add <username>',':添加用户')
		print '%-35s %s' % (' del <username>',':删除用户')
		print '%-35s %s' % (' alter <username> <key> <value>',':修改用户属性')
		print '%-35s %s' % (' list',':显示所有用户')
		print '%-35s %s' % (' show <usrname>',':显示用户属性')
		exit(3)
		
	argnum = len(args)
	if cmd == 'add':
		if argnum == 4:
			add_user(sys.argv[3])
		else:
			print 'add 命令需要一个参数，参考 user add <username>'
			exit(10)
	
	if cmd == 'del':
		if argnum == 4:
			del_user(sys.argv[3])
		else:
			print 'del 命令需要一个参数，参考 user del <username>'
			exit(10)
	
	if cmd == 'show':
		if argnum == 4:
			show_user(sys.argv[3])
		else:
			print 'show 命令需要一个参数，参考 user show <username>'
			exit(10)
	
	if cmd == 'list':
		if argnum == 3:
			list_user()
		else:
			print 'list 命令不需要参数，参考 user list'
			exit(10)

	if cmd == 'alter':
		if argnum == 6:
			alter_user(sys.argv[3],sys.argv[4],sys.argv[5])
		else:
			print 'alter 命令需要3个参数，参考 user alter <username> <properties> <values>'
			exit(10)

def get_traffic(traffic):
	if traffic < 1024:
		s=str(traffic)+'KB'
		return s
			
	m = traffic / 1024
	k = traffic % 1024
	if m > 1024:
		g = m / 1024
		m = m % 1024
		s = str(g)+'GB'+str(m)+'MB'+str(k)+'KB'
	else:
		s = str(m)+'MB'+str(k)+'KB'
	return s
																
def get_deration(deration):
	if deration <= 60 :
		return str(deration)+'S'
	m = deration / 60
	s = deration % 60
	s1 = str(m)+'M'+str(s)+'S'
	if m >= 60:
		h = m / 60
		m1 = m % 60
		s1 = str(h)+'H'+str(m1)+'M'+str(s)+'S'
		if h >= 24:
			d = h /24
			d1 = h % 24
			s1 =str(d)+'D'+str(d1)+'H'+str(m1)+'M'+str(s)+'S'
	return s1

def get_password(s):
	t = hashlib.md5()
	t.update(s)
	return t.hexdigest()

