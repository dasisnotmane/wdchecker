


import requests, lxml.html , bs4
import parsing_dashboard
import logging 
import time
import sys 
import pprint

def initialize_session ():
	# get a session , makes it easier since it retains cookies thus makes it more eff
	# for continuous requests
	s = requests.session()

	# here we make a request for the login page
	login = s.get('https://streetsoncloud.com/login',timeout=2)
	# check status code of request(ok 200) 
	# stop the program is error 404
	login.raise_for_status()
	

	form = {	}

	form['username'] = "Staging" 
	form['password'] = "Staging123" 
	response = s.post('https://streetsoncloud.com/login', data=form)

	response.raise_for_status()

	print(response.status_code)
	print(response.url)

	signs_dashboard = s.get('https://streetsoncloud.com/signs/tableview')
	print(signs_dashboard.text.encode("utf-8"))
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

	# print(group_headers)
	tables = dashboard_soup.find_all('table')



	location_list = {}

	for groups in headers : 

		header = groups.find("div",{"class":"list-group group-name"})
		# print(header.get_text()\)
		group = groups.find("tbody")
		rows = group.find_all("tr")	

		data = [row.find_all("td") for row in rows]

		# print(header.get_text())
		scaped_data = []
		for each in data :
			scaped_data.append( [value.get_text() for value in each])
<<<<<<< HEAD
			
=======
>>>>>>> origin/json_parsing
		# print(scaped_data)
		location_list[header.get_text()] = scaped_data
		# for location in rows:
		# 	print(""+location.get_text())
			# data.append(location.get_text())


		print("===============================")

	return location_list


# def dasboard_check_batt ():
# def dasbaord_check_serial ():
# def dashboard_check_time ():
# def dashboard_check_location():
# def dashboard_check_model():
# def dashboard_check_group():



html_soup = initialize_session()
location_list = dashboard_parse_tables(html_soup)
<<<<<<< HEAD
print(location_list["16666"])

=======
# print(location_list["16666"])
time.sleep(2)
>>>>>>> origin/json_parsing


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
