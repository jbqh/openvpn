#!/usr/bin/python
#coding:utf-8

import sys
import user
import route
import log

if len(sys.argv) == 1:
	print 'Command Error,no command to specify,use commands below:'
	print ' user'
	print ' route'
	print ' log'
	exit(1)
	
cmdlist = ['user','route','log']
userlist = ['add','del','alter','list','show']
routelist = ['create','delete','ls','show']
loglist = ['list','show']

cmd = sys.argv[1]
if cmd not in cmdlist:
	print 'Command %s is unrecognized,use commands below' % cmd
	print ' user	manage users'
	print ' route	manage routes'
	print 'log	list or show logs'
	exit(2)
	
if len(sys.argv) == 2:
	print 'Too few args,command %s must need 1 arg' % cmd
	exit(3)

cmdopt = sys.argv
if cmd == 'user':
	user.users(cmdopt)
	
if cmd == 'route':
	route.routes(cmdopt)
	
if cmd == 'log':
	log.logs(cmdopt)
