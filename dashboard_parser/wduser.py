import requests, lxml.html , bs4
import parsing_dashboard
import logging 
from pprint import pprint
import json

session_logger = logging.getLogger("login")
session_logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
session_logger.addHandler(ch)


class wduser :

        def __init__(self,user,passwd):
                self.user = user
                self.passwd = passwd
                self.dashboard_header = {

                        'Host': 'streetsoncloud.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': 'https://streetsoncloud.com/signs/tableview'

                }

        def initialize_session (self):

                # get a session , makes it easier since it retains cookies thus makes it more eff
                # for continuous requests
                self.session = requests.session()
                # here we make a request for the login page
                login = self.session.get('https://streetsoncloud.com/login',timeout=2)
                # check status code of request(ok 200) 
                # stop the program is error 404
                login.raise_for_status()
                session_logger.info("Successfully reached login page {}".format(login.status_code))
                return self.session


        def login_session (self): 

                form = {}

                form['username'] = self.user 
                form['password'] = self.passwd
                response = self.session.post('https://streetsoncloud.com/login', data=form)

                response.raise_for_status()
                session_logger.info("login status{}".format(response.status_code))
                session_logger.info("Current Page : {}".format(response.url))

        def get_dashboard_html (self):
                headers = {
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br'
                }
                signs_dashboard = self.session.get('https://streetsoncloud.com/signs/tableview',headers=headers)
                signs_dashboard.raise_for_status()
                session_logger.info("dashboard page status : {}".format(signs_dashboard.status_code))
                session_logger.info("Moving to dashboard page : {}".format(signs_dashboard.url))        
                # with open("streetsonclouddb.html","wb") as f : 
                #       f.write(signs_dashboard.content)
                return signs_dashboard.text


        def get_dashboard_soup(self,html_file):

                self.dashboard_soup = bs4.BeautifulSoup(html_file,"lxml")

                return self.dashboard_soup

        def get_dashboard_json ( self):

                data = self.session.post('https://streetsoncloud.com/signs/tableview/getdata', headers = self.dashboard_header)
                live_data = data.json()
                return live_data
        def dashboard_parse_tables (self):

                
                group_headers = []
                data = []

                headers = self.dashboard_soup.find_all("div",{"class" : 'tblview-group'})
                tables = self.dashboard_soup.find_all('table')


                location_list = {}

                # cycle through each group in the dashboard
                for groups in headers : 

                        # find the name of that group 
                        header = groups.find("div",{"class":"list-group group-name"})
                        
                        group = groups.find("tbody")
                        rows = group.find_all("tr")     
                        # for every row make a list of the data elements 
                        data = [row.find_all("td") for row in rows]
                        id_reference = []
                        scaped_data = []

                        # get a list of all the reference ids (used to indicate which location)
                        for tag in group.find_all("td"):
                                if tag.has_attr("id"):
                                    if tag.get("id")[1:] not in id_reference:
                                            id_reference.append(tag.get("id")[1:])
                        # get a list of all the individual data from that row of data 
                        for each in data :
                                scaped_data.append( [value.get_text() for value in each])
                        session_logger.debug("Header : {}".format(header.get_text()))

                        #top level of the dict - contains groupnames 
                        location_list[header.get_text()] =  {key:value for key,value in zip(id_reference,scaped_data)}

                    


                        #print("===============================")
                #location_list = {key:value for key,value in zip(id_reference,scaped_data)}
                #session_logger.debug("data reference key: {}".format(id_reference))
                #session_logger.debug(" data : {}".format(scaped_data))       
                return location_list 




                        
tl = wduser("Staging","Staging123")
tl.initialize_session()
tl.login_session()
htmlfile = tl.get_dashboard_html()
dashboard_soup = tl.get_dashboard_soup(htmlfile)
location_list = tl.dashboard_parse_tables()
#json_obj = tl.get_dashboard_json()
# pprint(json_obj)
# pprint(json_obj['data']['1466']['Last_connect'])
pprint(location_list)


# tl.get_dashboard_json()
# print(htmlfile)
# htmlsoup = tl.get_dashboard_soup(htmlfile)
