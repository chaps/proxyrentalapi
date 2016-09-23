

"""
#PROXYRENTAL API

		Remember always to logout once donw with a successful login.

"""

---Requirements---
requests

API using requests package for making http requests with the 
	ProxyRental REST API


--- example ---

from proxyrental.client import ProxyRentalClient
#SET THE URL OF THE SERVICE (IN CASE IT CHANGES...)
the_url = "http://mprs.proxyrental.net:6655/ProxyRental/RestClientService"
the_user = "someuser"
the_passwd = "somepassword"
client = ProxyRentalClient()
client.set_url(the_url)
client.set_user(the_user)
client.set_password(the_passwd)
#Returns bool to check wether 
if client.login():
	client.change_proxy()
	client.get_global_info()
	client.get_server_proxy()
	print client.globalinforesponse.text
	print client.changeproxyresponse.text
	print client.serverproxy_ip, client.serverproxy_port
	client.logout()
else:
	print client.error_code



