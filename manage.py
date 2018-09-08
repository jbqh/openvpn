#!/usr/bin/python
#coding:utf-8

import sys
import user
import route
import log

if len(sys.argv) < 3:
	print 'SyntaxError: use %s <command> [options],or type help' % sys.argv[0]
	exit(1)
	
cmdlist = ['user','route','log']
userlist = ['add','del','alter','list','show']
routelist = ['create','delete','ls','show']
loglist = ['list','show']

cmd = sys.argv[1]
if cmd not in cmdlist:
	print 'SyntaxError: use %s <command> [options],or type help' % sys.argv[0]
	print 'command perhaps is: %s' % cmdlist
	exit(2)
	
cmdopt = []
for i in range(2,len(sys.argv)):
	cmdopt.append(i)

if cmd == 'user':
	user.users(userlist,cmdopt)
	
if cmd == 'route':
	route.routes(routelist,cmdopt)
	
if cmd == 'log':
	log.logs(loglist,cmdopt)
