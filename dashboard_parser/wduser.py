import requests, lxml.html , bs4
import parsing_dashboard
import pprint
import logging 

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

		signs_dashboard = self.session.get('https://streetsoncloud.com/signs/tableview')
		response.raise_for_status()
		session_logger.info("dashboard page status : {}".format(signs_dashboard.status_code))
		session_logger.info("Moving to dashboard page : {}".format(signs_dashboard.url))	
		# with open("streetsonclouddb.html","wb") as f : 
		# 	f.write(signs_dashboard.content)
		dashboard_soup = bs4.BeautifulSoup(signs_dashboard.text,"lxml")
		return dashboard_soup


tl = wduser("Staging","Staging123")
tl.initialize_session()
tl.login_session()