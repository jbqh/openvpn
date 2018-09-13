#!/usr/bin/python
#coding:utf-8

import sys
import user
import route
#import log

if len(sys.argv) == 1:
	print '没有指定任何命令，使用以下命令：'
	print ' user'
	print ' route'
	print ' log'
	exit(1)
	
cmdlist = ['user','route','log']
#userlist = ['add','del','alter','list','show']
routelist = ['create','del','add','ls','show']
loglist = ['list','show']

cmd = sys.argv[1]
if cmd not in cmdlist:
	print '未被识别的命令 [ %s ]，请使用以下命令：' % cmd  
	print '%-10s %s' % (' user',':用户管理') 
	print '%-10s %s' % (' route',':路由管理')
	print '%-10s %s' % (' log',':日志管理')
	exit(2)
	
if len(sys.argv) == 2:
	if cmd == 'user':
		print '%-35s %s' % (' add <username>',':添加用户')
		print '%-35s %s' % (' del <username>',':删除用户')
		print '%-35s %s' % (' alter <username> <key> <value>',':修改用户属性')
		print '%-35s %s' % (' list',':列出所有用户')
		print '%-35s %s' % (' show <usrname>',':显示用户详细信息')
		exit(3)
	if cmd == 'route':
		print '%-30s %s' % (' create <route> [commet]',':创建路由')
		print '%-30s %s' % (' del <route-id>',':删除路由')
		print '%-30s %s' % (' add <route-id> <username>',':添加用户路由')
        print '%-30s %s' % (' show <username>',':显示用户路由')
        print '%-30s %s' % (' list',':列出所有路由')
        exit(3)

cmdopt = sys.argv
if cmd == 'user':
	user.users(cmdopt)
	#cmd = args[3]
	#print cmd
	
if cmd == 'route':
	route.routes(cmdopt)
	
if cmd == 'log':
	log.logs(cmdopt)
