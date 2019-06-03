#!/usr/bin/python
# coding:utf-8

import sys
import os
import ldap

ldapServer = 'IP:389'
baseDN = 'dc=,dc='
bindDN = 'cn=,ou=,dc=,dc='
bindPassword = ''
searchFilter = '(sAMAccountName=%s)'
ldap.set_option(ldap.OPT_REFERRALS,0)

def ldapConnect():
	try:
		conn = ldap.initialize(ldapServer)
		conn.simple_bind_s(bindDN,bindPassword)
	except:
		exit(1)
	return conn

def searchUser(username):
	conn = ldapConnect()
	filterStr = searchFilter % username
	try:
		ldap_results = conn.search(baseDN,ldap.SCOPE_SUBTREE,filterStr)
		results_type,results=conn.result(ldap_results,0)
	except ldap.LDAPError as e:
		print e
		return []
	#return results_type,results
	return _process_results(results)

def validUser(username,password):
	user_dn = get_dn(username)
	if user_dn is None:
		return 1
	try:
		connection = ldap.initialize(ldapServer)
		connection.set_option(ldap.OPT_REFERRALS, 0)
		connection.simple_bind_s(user_dn.encode('utf-8'), password)
		cmd='echo sucessful > /tmp/s' 
		os.popen(cmd)
		return 0
	except:
		os.popen('echo failed > /tmp/f')
		return 1

def get_dn(username):
	results = searchUser(username)
	if (results is not None) and (len(results) == 1):
		(user_dn, user_attrs) = next(iter(results))
	else:
		user_dn = None
	return user_dn


def _process_results(results):
	results = [r for r in results if r[0] is not None]
	results = _DeepStringCoder('utf-8').decode(results)
	results = [(r[0].lower(), r[1]) for r in results]
	result_dns = [result[0] for result in results]
	return results


####
class _DeepStringCoder(object):
	def __init__(self, encoding):
		self.encoding = encoding

	def decode(self, value):
		try:
			if isinstance(value, bytes):
				value = value.decode(self.encoding)
			elif isinstance(value, list):
				value = self._decode_list(value)
			elif isinstance(value, tuple):
				value = tuple(self._decode_list(value))
			elif isinstance(value, dict):
				value = self._decode_dict(value)
		except UnicodeDecodeError:
			pass
		return value

	def _decode_list(self, value):
		return [self.decode(v) for v in value]
	
	def _decode_dict(self, value):
		decoded = ldap.cidict.cidict()
		for k, v in value.items():
			decoded[self.decode(k)] = self.decode(v)
		return decoded

'''
#username=os.environ.get("username",'vdin')
#password=os.environ.get("password",'vdin')
#cmd='echo username=%s, password=%s > /tmp/122' % (username,password)
#os.popen(cmd)


rst=validUser(username,password)
if rst==0:
	print 0
	exit(0)
else:
	print 1
	exit(1)
#exit(a)


if __name__ == '__main__':
	username=sys.argv[1]
	#password=sys.argv[2]
	#r=searchUser(username)
	#r=validUser(username,password)
	r = get_dn(username)
	print r
	dl=r.split(',')[0]
	dl1=dl.split('=')[1]
	print dl1
	if r==0:
		print 'valid user successful!'
	else:
		print 'user is not exsits or password is wrong'
'''
