#-*- encoding: utf-8 -*-

import requests
import urlparse
import md5
from lxml import etree
from xml.etree import ElementTree
import traceback
from global_info import GlobalInfo
import threading
import os


from chaps_os_utils.utils import is_windows, is_linux, get_user

class ProxyRentalClient():
    """Implentation for using proxyrental api\

    Based on the php api.

    Attributes:
        url : The endpoint for the rest API
        user_session: saves if there is a current session with proxy rental,
            its later set by login with an response from their api
        user_token: saves the user token set by their api response with the login method
        username: the username for the proxyrental account
        password: the password for the proxyrental account, over md5
        
    """

    class NotLoggedIn(Exception):

        def __init__(self):
            Exception.__init__(self, "No User Session found try loggin in first.")
            pass

    methods = {
        "Logout": "/Logout",
        "Login": "/Login",
        "Synchronize": "/Synchronize",
        "ChangeProxy": "/ChangeProxy2",
        "GetGlobalInfo": "/GetGlobalInfo",
        "SetProxySpeedFilter": "/SetProxySpeedFilter",
        "GetServerProxy": "/GetServerProxy"
    }

    error_codes = (
        '00000000-0000-0000-0000-000000000000',
        '10000000-0000-0000-0000-000000000000',
        '20000000-0000-0000-0000-000000000000',
    	'30000000-0000-0000-0000-000000000000',
    	'40000000-0000-0000-0000-000000000000',
    	'60000000-0000-0000-0000-000000000000',            
    )

    error_codes_messages = {
        '00000000-0000-0000-0000-000000000000': "Unknown Behaviour.",
        '10000000-0000-0000-0000-000000000000': "User is out of date.",
        '20000000-0000-0000-0000-000000000000': "User has over limit.",
        '30000000-0000-0000-0000-000000000000': "Incorrect Username or Password.",
        '40000000-0000-0000-0000-000000000000': "Server under diagnostic.",
        '60000000-0000-0000-0000-000000000000': "Account Locked.",            
    }

    URL = "http://mprs.proxyrental.net:6655/ProxyRental/RestClientService"

    def __init__( self, url=""):
        """Inits the class, sets the attributes that are for response to None.\
        """
        if url != "":
            self.set_url( url )
        else:
            self.set_url( self.URL  )
        self.reset()


    def reset(self):
        """Sets all the relevant attributes to None.\
        """
        #Values setted from Login endpoint response.
        self.user_session = None
        self.user_token = None
        #Values setted from global info response.
        self.global_info = None
        self.current_ip = None
        #Values setted from get_server_proxy response.
        self.proxyserver_ip = None
        self.proxyserver_port = None
        #Values setted from 
        self.error_code = None
        pass


    def set_url(self, url):
        """Sets the url which points to the proxyrental host/port api.\
        """
        self.url = url


    def set_user(self, user):
        """Sets the user for the api credentials.\

        """
        self.user = user


    def set_password(self, password):
        """Sets the password over md5 for the api credentials.\

        """
        self.password = md5.new(password).hexdigest() 


    def append_xmlheader(self, xml_string):
        """Prepends the xml header to the string without the encoding attribute.\

        This due to the etree tostring method with kwarg xml_declaration adds the encoding by default.
        """
        return "<?xml version='1.0'?>\n" + xml_string 


    def set_sessionresponse( self, user_session=None, user_token=None, sessionresponse=None ):
        """ Sets a session response from usersession and user token values.
        """
        if sessionresponse:
            self.sessionresponse_text = sessionresponse
            #sessionresponse = ElementTree.fromstring(response.text)
        if user_session and user_token:
            self.sessionresponse_text = "<Session><UserToken>%s</UserToken><UserSession>%s</UserSession></Session>" % ( user_token, user_session, )
        
        sessionresponse = ElementTree.fromstring( self.sessionresponse_text )

        self.user_session = sessionresponse.find("UserSession").text
        self.user_token = sessionresponse.find("UserToken").text
        pass


    def build_session_xml_string( self ):
        if not self.user_session or not self.user_token:
            raise BaseException("Tokens aren't set.")
        return "<Session><UserToken>%s</UserToken><UserSession>%s</UserSession></Session>" % ( self.user_token, self.user_session, )


    def get_default_sessionfile_path( self ):
        if is_windows():
	    return os.path.join( "C:\\","Users","%s","AppData","Local","Proxy Rental","session.txt" ) % (get_user(),)
        if is_linux():
            return os.path.join("/","tmp","proxyrentalsession.txt")


    def write_session( self, path=None ):
	if not self.user_session or not self.user_token:
            raise BaseException("Tokens aren't set.") 
        if not path:
	    path = self.get_default_sessionfile_path()
	with open(path, "w") as f:
	    f.write( self.build_session_xml_string() )
        return
        pass

    def do_request(self, method, api_method_path, data=None ):
        """ Send a http request to the API Method.\
        
        Reimplement the host construction with urlparse.something...
        """
        host = self.url + api_method_path
        if method == "GET":
            response = requests.get(host)
        if method == "POST":
            #headers = {'Content-Type': 'application/xml'}
            response = requests.post(
                host,
                data = data,
            )
        return response


    def test_response(self):
        """Parse the xml api repsonse to check a successful request.
        
        The server is supposed to reply xmls on success requests.
        """
        pass


    def login(self):
        """Calls ProxyRental REST API login method and handles the response.\

        """
        if self.user_session != None:
            self.logout()

        #Build the xml data to send.
        root_element = etree.Element("User")
        user_element = etree.Element("Name")
        user_element.text = self.user
        password_element = etree.Element("Hash")
        password_element.text = self.password
        root_element.append(user_element)
        root_element.append(password_element)
        data = self.append_xmlheader(etree.tostring( root_element))
        try:
            response = self.do_request(
                    "POST",
                    self.methods["Login"],
                    data=data
            )
            self.sessionresponse = response
            self.sessionresponse_text = self.sessionresponse.text
            sessionresponse = ElementTree.fromstring(response.text)
            self.user_session = sessionresponse.find("UserSession").text
            self.user_token = sessionresponse.find("UserToken").text
        except Exception, e:
            print traceback.print_exc()
            print e
            self.last_error = e
            self.user_session = False
            return False
        if self.user_session in self.error_codes:
            self.error_code = self.user_session
            self.user_session = False
            return False
        return True


    def synchronize(self):
        """Calls the sinchronize endpoint to mantain a session with the server.\
        
        """
        if self.user_session == None:
            return False
        try:
            response = self.do_request(
                "POST",
                self.methods["Synchronize"],
                data= self.append_xmlheader(self.sessionresponse_text)
            )
            self.synchronize_response = response
            """
            ok: session synchronized,
            expired_user: user is expired,
            invalid_user: invalid user or session is expired,
            proxyIsUnavailable: proxy became unavailable

            """
        except Exception, e:
            self.last_error = e
            print e
            print traceback.print_exc()
            return False
        return True


    def thread_synchronize(self):
        """Inits recursive threading in a 25 seconds interval to refresh proxy rental session.\

        """
        threading.Timer(25, self.thread_synchronize).start()
        try:
            print "SYNCHRONIZING PROXY RENTAL..."
            self.synchronize()
        except Exception, e:
            print e
            print traceback.print_exc()
        pass
   

    def get_server_proxy(self):
        """Returns the server and port to which the user should connect to stablish a proxy connection\
        
        """
        if self.user_session == None:
            
            return False
        try:
            response = self.do_request(
                "POST",
                self.methods["GetServerProxy"],
                data= self.append_xmlheader(self.sessionresponse_text)
            )
            self.serverproxyresponse = response

            tree = ElementTree.fromstring(response.text)
            self.serverproxy_ip= tree.find("IP").text
            self.serverproxy_port = tree.find("Port").text
	    if not self.serverproxy_ip or not self.serverproxy_port:
	        raise Exception("Bad Auth server session response: %s" % ( self.serverproxyresponse.text,))
            return True
        except Exception, e:
            self.last_error = e
	    raise(e)
            return False


    def set_proxy_filter(self, speed_quality):
        """ Sends a requests to set the new speed for the proxy connection.\

        """
        if self.user_session == None:
            return False
        root_element = etree.Element("Params")
        session_element = etree.Element("Session")
        usersession_element = etree.Element("UserSession")
        user_token_element = etree.Element("UserToken")
        speed_element = etree.Element("SpeedQuality")
         
        usersession_element.text = self.user_session
        user_token_element.text = self.user_token
        session_element.append( usersession_element )
        session_element.append( user_token_element )

        speed_element.text = speed_quality

        #password_element.text = self.password
        
        root_element.append( session_element )
        root_element.append( speed_element )
        #root_element.append(password_element)
        data = self.append_xmlheader(etree.tostring( root_element))
        try:
            response = self.do_request(
                "POST",
                self.methods["SetProxySpeedFilter"],
                data=data
            )
            self.filter_response = response 
            pass
        except Exception, e:
            print e
            print traceback.print_exc()
            self.last_error = e
            return False
        return True


    def change_proxy(self):
        """Requests a new proxy from the API.\
         
        """
        if self.user_session == None:

            pass
        try:
            response = self.do_request(
                "POST",
                self.methods["ChangeProxy"],
                data = self.append_xmlheader(self.sessionresponse_text)
            )
            self.changeproxyresponse = response
            pass
        except Exception, e:
            self.last_error = e
            print e
            print traceback.print_exc()
            return False
        return True



    def get_global_info(self):
        """Requests the global info of the session from the api.\

        """
        if self.user_session == None:
            return False
        try:
            response = self.do_request(
                "POST",
                self.methods["GetGlobalInfo"],
                data = self.append_xmlheader(self.sessionresponse_text)
            )
            self.globalinforesponse = response
            self.globalinfo = GlobalInfo(response.text)
            self.proxy_ip = self.globalinfo.current_ip
        except Exception, e:
           print e
           print traceback.print_exc()
           return False
        return response


    def logout(self):
        """Logs out a current logged in account.\
        """
        if self.user_session == None:
            return False
        try:
            data =  self.append_xmlheader(self.sessionresponse_text)
            response = self.do_request( 
                    "POST",
                    self.methods["Logout"],
                    data = data
            )
            return True
        except Exception, e:
            print e 
            print traceback.print_exc()
            return False
        return True



