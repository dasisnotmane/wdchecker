# import requests
# from lxml import html

# session_requests = requests.session()

# login_url = "https://bitbucket.org/account/signin/?next=/"
# result = session_requests.get(login_url)

# tree = html.fromstring(result.text)
# authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

# result = session_requests.post(
# 	login_url, 
# 	data = payload, 
# 	headers = dict(referer=login_url)
# )


# url = 'https://bitbucket.org/dashboard/overview'
# result = session_requests.get(
# 	url, 
# 	headers = dict(referer = url)
# )

# account.

# tree = html.fromstring(result.content)
# bucket_names = tree.xpath("//div[@class='repo-list--repo']/a/text()")

# print(bucket_names)


# result.ok # Will tell us if the last request was ok
# result.status_code # Will give us the status from the last request


import requests, lxml.html , bs4
import parsing_dashboard
import pprint
import logging 

def initialize_session ():
	s = requests.session()

	### Here, we're getting the login page and then grabbing hidden form
	### fields.  We're probably also getting several session cookies too.
	login = s.get('https://streetsoncloud.com/login',timeout=2)
	login.raise_for_status()
		
	login_html = lxml.html.fromstring(login.text)
	# hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
	# form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
	form = {	}
	### Now that we have the hidden form fields, let's add in our 
	### username and password.
	# form['username'] = "Rmikati" # Enter an email here.  Not mine.
	# form['password'] = "Rmikati12" # I'm definitbely not telling you my password.

	form['username'] = "Staging" # Enter an email here.  Not mine.
	form['password'] = "Staging123" # I'm definitbely not telling you my password.
	response = s.post('https://streetsoncloud.com/login', data=form)

	response.raise_for_status()

	print(response.status_code)
	print(response.url)

	signs_dashboard = s.get('https://streetsoncloud.com/signs/tableview')
	response.raise_for_status()

	# with open("streetsonclouddb.html","wb") as f : 
	# 	f.write(signs_dashboard.content)

	dashboard_soup = bs4.BeautifulSoup(signs_dashboard.text,"lxml")
	return dashboard_soup


# print(dashboard_soup.find_all("div",{"class": "list-group group-name"}))
# for group_name in dashboard_soup.find_all("div",{"class": "list-group group-name"}):
# 	print(group_name.get_text())


# for row in dashboard_soup.find_all("div",{"class": "tblview-group"}):




def dashboard_parse_tables (dashboard_soup):


	group_headers = []
	data = []

	headers = dashboard_soup.find_all("div",{"class" : 'tblview-group'})

	# for each in headers: 
	# 	group_headers.append(each.get_text())

	print(group_headers)
	tables = dashboard_soup.find_all('table')



	location_list = {}

	for groups in headers : 

		header = groups.find("div",{"class":"list-group group-name"})
		# print(header.get_text()\)
		group = groups.find("tbody")
		rows = group.find_all("tr")	

		data = [row.find_all("td") for row in rows]

		print(header.get_text())
		scaped_data = []
		for each in data :
			scaped_data.append( [value.get_text() for value in each])
		print(scaped_data)
		location_list[header.get_text()] = scaped_data
		# for location in rows:
		# 	print(""+location.get_text())
			# data.append(location.get_text())


		print("===============================")
		
	return location_list

html_soup = initialize_session()
location_list = dashboard_parse_tables(html_soup)
print(location_list["DEMO"])

# for table  in tables:
# 	print(table)
# 	table_body = table.find('tbody')

# 	rows = table_body.find_all('tr')
# 	for row in rows:
# 	    cols = row.find_all('td')
# 	    # print(cols)
# 	    cols = [ele.text.strip() for ele in cols]
# 	    data.append([ele for ele in cols ]) # Get rid of empty values

# 	# for each in data : 
# 	# 	print(each)

# # 	print("=====================================")



# pprint.pprint(location_list)
# for each in in headers : 
# 	location_list[each] 

		


# for row in dashboard_soup.find_all("td"):
# 	print(row)

### How can we tell that we logged in?  Well, these worked for me:
#  response.url
# 'https://www.yelp.com/cleveland'
#  'Stephen' in response.text