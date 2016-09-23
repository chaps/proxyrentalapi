
from lxml import etree
from xml.etree import ElementTree
import traceback



class GlobalInfo():
    """A class for storing the attributes from the global info api response,\
    
    """

    def __init__(self, string=None):
        """Initializaes the class with optional xml string.\

        """
        if string:
            try:
                self.fromstring(string)
            except Exception, e:
                print e
                print traceback.print_exc()
                self.setToNone()
                pass
        else:
            self.setToNone()
        pass


    def setToNone(self):
        """Sets all relevant attributes to None.\ """
        self.xmltree = None
        self.nearest_infos = None
        self.persistence = None
        self.health = None
        self.current_ip = None
        self.city = None
        self.city_code = None
        self.country_name = None
        self.state = None
        self.latitude = None
        self.longitude = None
        self.isp = None
        self.postal_code = None
        self.cl_time = None
        self.cl_time_actuality = None
        self.cl_uri = None
        self.time_zone_id = None
        pass


    def fromstring(self, string):
        """Receives an xml string and tries to parse all relevant elements.

        """
        self.xmltree = ElementTree.fromstring(string)
        self.nearest_infos = self.xmltree.find("nearestInfos").text
        self.persistence = self.xmltree.find("Persistence").text
        self.health = self.xmltree.find("Health").text
        self.current_ip = self.xmltree.find("CurrentIP").text
        self.city = self.xmltree.find("City").text
        self.city_code = self.xmltree.find("CityCode").text
        self.country_name = self.xmltree.find("CountryName").text
        self.state = self.xmltree.find("State").text
        self.latitude = self.xmltree.find("Latitude").text
        self.longitude = self.xmltree.find("Longitude").text
        self.isp = self.xmltree.find("ISP").text
        self.postal_code = self.xmltree.find("PostalCode").text
        self.cl_time = self.xmltree.find("CLTime").text
        self.cl_time_actuality = self.xmltree.find("CLTimeActuality").text
        self.cl_uri = self.xmltree.find("CLUri").text
        self.time_zone_id = self.xmltree.find("TimeZoneID").text


        pass


    pass
