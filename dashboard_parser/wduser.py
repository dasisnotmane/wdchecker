import requests, lxml.html , bs4
import parsing_dashboard
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

	def get_dashboard_html (self):
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br'
		}
		signs_dashboard = self.session.get('https://streetsoncloud.com/signs/tableview',headers=headers)
		signs_dashboard.raise_for_status()
		session_logger.info("dashboard page status : {}".format(signs_dashboard.status_code))
		session_logger.info("Moving to dashboard page : {}".format(signs_dashboard.url))	
		# with open("streetsonclouddb.html","wb") as f : 
		# 	f.write(signs_dashboard.content)
		return signs_dashboard.text


	def get_dashboard_soup(self,html_file):

		dashboard_soup = bs4.BeautifulSoup(html_file,"lxml")
		return dashboard_soup



tl = wduser("Staging","Staging123")
tl.initialize_session()
tl.login_session()
htmlfile = tl.get_dashboard_html()
print(htmlfile)
# htmlsoup = tl.get_dashboard_soup(htmlfile)
