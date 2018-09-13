#!/usr/bin/python
#coding:utf-8

import sys
import user
import route
#import log

if len(sys.argv) == 1:
	print 'Command Error,no command to specify,use commands below:\n'
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
	print 'Command %s is unrecognized,use commands below:\n' % cmd
	print ' user	manage users'
	print ' route	manage routes'
	print ' log	list or show logs'
	exit(2)
	
if len(sys.argv) == 2:
	if cmd == 'user':
		print '%-35s %s' % (' add <username>',':add a user')
		print '%-35s %s' % (' del <username>',':delete a user')
		print '%-35s %s' % (' alter <username> <key> <value>',':edit user property')
		print '%-35s %s' % (' list',':list users')
		print '%-35s %s' % (' show <usrname>',':show user property')
		exit(3)
	if cmd == 'route':
		print '%-30s %s' % (' create <route> [commet]',':create a route')
		print '%-30s %s' % (' del <route-id>',':delete a route')
		print '%-30s %s' % (' add <route-id> <username>',':add a route to user')
		print '%-30s %s' % (' list',':list all routes')
		exit(3)

cmdopt = sys.argv
if cmd == 'user':
	user.users(cmdopt)
	cmd = args[3]
	print cmd
	
if cmd == 'route':
	route.routes(cmdopt)
	
if cmd == 'log':
	log.logs(cmdopt)
