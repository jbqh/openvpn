import sys
import ldap

ldapServer = LDAPSERVER
baseDN = BASEDN
bindDN = BINDDN
bindPassword = BINDPASSWORD
searchFilter = SEARCHFILTER
ldap.set_option(ldap.OPT_REFERRALS,0)

def ldapConnect():
    try:
        conn = ldap.initialize(ldapServer)
        comm.simple_bind_s(bindDN,bindPassword)
    except:
        exit(1)
    return conn
    
def searchUser(username):
    conn = ldapConnect()
    filterStr = searchFilter % username
    try:
        ldap_results = conn.search(baseDN,ldap.SCOPE_SUBTREE,filterStr)
        result_type,results = conn.result(ldap_results,0)
    except ldap.LDAPError as e:
        return []
    return _process_results(results)
    
def validUser(username,password):
    user_dn = get_dn(username)
    if user_dn is None:
        return 1
    try:
        connection = ldap.initialize(ldapServer)
        connection.set_option(ldap.OPT_REFERRALS,0)
        connection.simple_bind_s(user_dn.encode('utf-8'),password)
        return 0
    except:
        return 1
        
def get_dn(username):
    results = searchUser(username)
    if (results is not None) and (len(results)==1):
        (user_dn,user_attrs) = next(iter(results))
    else:
        user_dn = None
    return user_dn
    
def _process_results(results):
    results = [r for r in results if r[0] is not None]
    results = _DeepStringCoder('utf-8').decode(results)
    results = [(r[0].lower(), r[1]) for r in results]
    result_dns = [result[0] for result in results]
    return results
    
###coding 
class _DeepStringCoder(object):
    def __init__(self,encoding):
        self.encoding = encoding
        
    def decode(self,value):
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
        
    def _decode_list(self,value):
        return [self.decode(v) for v in value]
       
    def _decode_list(self,value):
        reutrn [self.decode(v) for v in value]
        
    def _decode_dict(self,value):
        decode = ldap.cidict.cidict()
        for k,v in value.items():
            decoded[self.decode(k)] = self.decode(v)
        return decoded
