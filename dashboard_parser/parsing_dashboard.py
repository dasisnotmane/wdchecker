


import requests, lxml.html , bs4

with open("streetsonclouddb.html") as f : 
	dashboard_soup = bs4.BeautifulSoup(f,"lxml")


# for body in dashboard_soup.find_all('tbody'):
# 	print(body.contents)



def get_tables (dashboard_soup):
	data = []


	tables = dashboard_soup.find_all('table')

	for table  in tables:

		table_body = table.find('tbody')

		rows = table_body.find_all('tr')
		for row in rows:
		    cols = row.find_all('td')

		    cols = [ele.text.strip() for ele in cols]
		    data.append([ele for ele in cols if ele]) # Get rid of empty values

		for each in data : 
			print(each)


		print("=================================")
# for group_name in dashboard_soup.find_all("div",{"class": "tblview-group"}):
# 	# for each in group_name.descendants:
# 	# 	print(each.find_all))	
# 	# print(group_name.div.contents[3].get_text())
# 	# print(group_name.contents[3].table.tbody)
# 	for each in group_name.contents[3].table.tbody.children:
		
# 	print("======================================")

	