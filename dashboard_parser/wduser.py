import requests, lxml.html , bs4
import parsing_dashboard
import logging 
from pprint import pprint
import json
from lxml import etree

session_logger = logging.getLogger("login")
session_logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
session_logger.addHandler(ch)


class wduser :

        def __init__(self,user,passwd,location_name):
                self.user = user
                self.passwd = passwd
                self.location_name = location_name 
                self.box_width = {

                        "Name" : 10 ,
                        "Address": 30, 
                        "Traffic Direction" : 18 ,
                        "Model" : 10 ,
                        "Serial #" :9,
                        "FW #" : 5 ,
                        "Vehicle Count" : 15 ,
                        "Avg. Speed" :12 ,
                        "85%. Speed" :12,
                        "Max. Speed" :12 ,
                        "Min. Speed" :12,
                        "Last Communication" :15,
                        "Power Supply" : 5                   
                                            

                }
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

                
                self.group_headers = []
                data = []

                table_headers = self.dashboard_soup.find_all("div",{"class" : 'tblview-group'})
                tables = self.dashboard_soup.find_all('table')
                
                table_heading = self.dashboard_soup.find("thead")
                self.column_headers = [col_head.get_text() for col_head in table_heading.find_all("th")] 
#                import pdb; pdb.set_trace() 
                for each in table_headers: 
                      self.group_headers.append(each.get_text())
#                print(self.group_headers)
                self.location_list = {}

                # cycle through each group in the dashboard
                for groups in table_headers  : 

                        # find the name of that group 
                        self.header = groups.find("div",{"class":"list-group group-name"}).get_text()
                        
                        group = groups.find("tbody")
                        rows = group.find_all("tr")     
                        # for every row make a list of the data elements 
                        data = [row.find_all("td") for row in rows]
                        id_reference = []
                        scaped_data = []
                        data_dict = {}
                        data_form = []

                        # get a list of all the reference ids (used to indicate which location)
                        for tag in group.find_all("td"):
                                if tag.has_attr("id"):
                                    if tag.get("id")[1:] not in id_reference:
                                            id_reference.append(tag.get("id")[1:])
                        # get a list of all the individual data from that row of data 
                        for each in data :
                                scaped_data.append( [value.get_text() for value in each])
                        for dat in scaped_data:

                            data_dict = dict(zip(self.column_headers,dat))
                            data_form.append(data_dict)

#                        session_logger.debug("Header : {}".format(self.header.get_text()))
                        session_logger.debug("Header : {}".format(self.header))

                        #top level of the dict - contains groupnames 
#                        self.location_list[self.header.get_text()] =  {key:value for key,value in zip(id_reference,scaped_data)}
                        self.location_list[self.header] =  {key:value for key,value in zip(id_reference,data_form)}

                    


                return self.location_list 

                # print(group_headers)
        def dashboard_update_data ( self ) :
            self.live_data = self.get_dashboard_json() 
            #pprint(self.live_data)
            
            #import pdb; pdb.set_trace()
            for key,value in self.location_list.items():
                if self.location_name == key :

#                    import pdb; pdb.set_trace()
                    print(self.location_list[key])
#                    for each in self.live_data['data']:
                    for k,v in self.live_data['data'].items():
                            if k in self.location_list[key]:

                                batt_xml = v['batt_voltage'] 
                                last_conn_xml = v['Last_connect']

                                batt_xml = etree.fromstring(batt_xml)
                                last_conn_xml = etree.fromstring(last_conn_xml)

                                self.location_list[key][k]["Vehicle Count"]=v["count"]
                                self.location_list[key][k]["Avg. Speed"]=v["avg_speed"]
                                self.location_list[key][k]["85%. Speed"]=v["avg_speed85"]
                                self.location_list[key][k]["Max. Speed"]=v["max_speed"]
                                self.location_list[key][k]["Min. Speed"]=v["min_speed"]
                                self.location_list[key][k]["Last Communication"]=last_conn_xml.text
                                self.location_list[key][k]["Power Supply"]=batt_xml.text
#


            pprint(self.location_list)                                

        def dashboard_view (self,*args):
            
            location_filter = None
            print(args[0])
            if len(args) == 1:
                location_filter = args[0]
                 
            elif len(args) > 1 :
                print("error too many arguments")
            
            for key,value in self.location_list.items():
                
                print("==========================================="*5)
                print(key)  
                print("==========================================="*5)
                for each in self.column_headers :
                     
                    print("{header_name:{width}} | ".format(header_name = each, width=self.box_width[each]),end="")
                print("\n")
                print("==========================================="*5)
                for row,row_data in value.items():
                    for attr,value in row_data.items():

                        print("{row_dat:{width}} | ".format(row_dat= value, width=self.box_width[attr]),end="")
                    print("\n")
                if key == location_filter :
                    break
                

        
                        
tl = wduser("Staging","Staging123","16666")
tl.initialize_session()
tl.login_session()
htmlfile = tl.get_dashboard_html()
dashboard_soup = tl.get_dashboard_soup(htmlfile)
location_list = tl.dashboard_parse_tables()
json_obj = tl.get_dashboard_json()
tl.dashboard_update_data()
tl.dashboard_view("16666")
#pprint(json_obj)
# pprint(json_obj['data']['1466']['Last_connect'])
#pprint(location_list)


# tl.get_dashboard_json()
# print(htmlfile)
# htmlsoup = tl.get_dashboard_soup(htmlfile)
